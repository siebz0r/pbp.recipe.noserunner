# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
"""
Core module. contains processor.
"""
import socket
import os

from multiprocessing import Pool
from multiprocessing import TimeoutError

from atomisator.main.config import log
from atomisator.main.config import dotlog
from atomisator.main.config import AtomisatorConfig

from atomisator.main import FILTERS
from atomisator.main import OUTPUTS
from atomisator.main import ENHANCERS
from atomisator.main import READERS
from atomisator.main import load_plugin

from atomisator.db.session import create_session
from atomisator.db.core import create_entry
from atomisator.db.core import get_entries
from atomisator.db.core import purge_entries

#
# internal APIs called by multiprocessing
#
def _select_enhancers(enhancers_selected):
    """Gets the selected enhancers."""
    res = []
    for name, args in enhancers_selected:
        if name in ENHANCERS:
            res.append((ENHANCERS[name], args))
    return res

def _select_outputs(outputs_selected):
    """Gets the selected outputs."""
    res = []
    for name, args in outputs_selected:
        if name in OUTPUTS:
            res.append((OUTPUTS[name], args))
    return res

def _apply_filters(entry, entries, selected_filters):
    """Applies all selected filters to an entry"""
    for filterer, args in selected_filters:
        entry = filterer(entry, entries, *args)
        if entry is None:
            return None
    return entry

def _process_source(reader_name, reader, reader_args):
    """processing one source. callable through
    a process"""
    try:
        log('\tRetrieving from %s - %s' %  (reader_name, str(reader_args)))
        return reader(*reader_args)
    except TimeoutError:
        log('\tTIMEOUT on %s - %s' % (reader_name, str(reader_args)))
        return []

def _enhance(entry, selected_enhancers):
    """Enhances an entry"""
    for enhancer, args in selected_enhancers:
        dotlog('.')
        entry = enhancer(entry, *args)
        if entry is None:
            return None
    return entry

def _prepare_enhancer(enhancer, entries):
    """prepare the enhancer"""
    if hasattr(enhancer, 'prepare'):
        dotlog('.')
        enhancer.prepare(entries)
    return enhancer

#
# class that processes data
#
class DataProcessor(object):
    """Atomisator processor

    Knows how to load datas and generate outputs.
    """

    def __init__(self, conf):
        self.parser = AtomisatorConfig(conf)
        self.existing_entries = []
        self.filter_chain = None
        create_session(self.parser.database)

    def load_data(self):
        """Fetches data"""
        dotlog('Loading existing data.')
        old_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(self.parser.timeout)
        try:
            self._load_data()
        finally:
            socket.setdefaulttimeout(old_timeout)

    def _cleanup_entries(self):
        """removes old entries"""
        purge_entries(self.parser.max_age)

    def _load_data(self):
        """Loads the data"""
        # remove the temp db if it exists
        if os.path.exists('_temp_.db'):
            os.remove('_temp_.db')

        # cleanup old entries
        dotlog('\tRemoving old entries.')
        self._cleanup_entries()

        # initial entries, see if this call is optimal
        dotlog('\tReading existing entries.')
        self.existing_entries = get_entries().all()

        # building filtering chain once.
        filter_names = [f[0] for f in self.parser.filters]
        dotlog('Loading filters plugins : %s' % ', '.join(filter_names))
        self.filter_chain = set([(load_plugin(name, FILTERS), args)
                                 for name, args in self.parser.filters
                                 if name in FILTERS])

        # building source chain once.
        source_names = [s[0] for s in self.parser.sources]
        dotlog('Loading source plugins : %s' % ', '.join(source_names))
        sources = [(reader_name, load_plugin(reader_name, READERS), args)
                   for reader_name, args in self.parser.sources]

        processes = self.parser.processes
        dotlog('Reading sources.')

        if processes == 1:
            dotlog('\tWorking in the same process')
            for source in sources:
                entries = _process_source(*source)
                self._process_entries(entries)
        else:
            # creating a processing pool
            pool = Pool(self.parser.processes)
            for source in sources:
                dotlog('\tLaunching worker for %s - %s' % (source[0], source[-1]))
                pool.apply_async(_process_source, source,
                                 callback=self._process_entries)

            pool.close()
            pool.join()
        dotlog('\n')

    def _process_entries(self, entries):
        """callback called by the worker"""
        # now lets apply filters, then store entries
        psession = create_session(self.parser.database,
                                  global_=False)
        for entry in entries:
            dotlog('.')
            entry = _apply_filters(entry, self.existing_entries,
                                   self.filter_chain)
            if entry is None:
                continue
            new_entry = create_entry(entry, commit=False,
                                     session=psession)
            self.existing_entries.append(new_entry[1])
        psession.commit()

    def generate_data(self):
        """Generates the output"""
        selected_enhancers = _select_enhancers(self.parser.enhancers)
        selected_outputs = _select_outputs(self.parser.outputs)
        processes = self.parser.processes

        # XXX TODO: limit the size of the data
        # processed, by number of items, or by date
        entries = get_entries().all()
        if selected_enhancers != []:
            # Enhancement is a two-phase process.
            # 1. Preparing entries for enhancement
            dotlog('Preparing enhancers.')
            if processes == 1:
                class Wrap(object):
                    def __init__(self, res):
                        self.res = res
                    def get(self):
                        return self.res

                results = [Wrap(e) for e in
                           [_prepare_enhancer(enhancer, entries)
                           for enhancer, args in selected_enhancers]]
            else:
                pool = Pool(self.parser.processes)
                results = [pool.apply_async(_prepare_enhancer,
                                            (enhancer, entries))
                       for enhancer, args in selected_enhancers]
                pool.close()
                pool.join()

            # pushing back into the ENHANCERS list (not the same process)
            # and selected_enhancers
            # XXX maybe the multiprocess has something cleaner for this
            for result in results:
                enhancer = result.get()
                enhancer_type = type(enhancer)
                for name, ob in ENHANCERS.items():
                    if type(ob) == enhancer_type:
                        ENHANCERS[name] = enhancer

                def _replace(s, args, new):
                    if type(s) == type(new):
                        s = new
                    return s, args

                selected_enhancers = [_replace(s, args, enhancer)
                                      for s, args in selected_enhancers]

            dotlog('\n')

            # 2. Now enhancing them
            dotlog('Enhancing: %s' % ', '.join([e for e, args
                                            in self.parser.enhancers]))

            if processes == 1:
                results = [e for e in [_enhance(entry, selected_enhancers)
                           for entry in entries] if e is not None]
            else:
                # creating a processing pool
                pool = Pool(self.parser.processes)
                results = [pool.apply_async(_enhance,
                           (entry, selected_enhancers))
                           for entry in entries]

                pool.close()
                pool.join()
                entries = [r for r in [result.get() for result in results]
                           if r is not None]
            dotlog('\n')

        if selected_outputs != []:
            dotlog('Writing outputs.')
            dotlog('Rendering: %s' % ', '.join([output[0] for output
                                             in self.parser.outputs]))
            for output, args in selected_outputs:
                dotlog('.')
                output(entries, args)
            dotlog('\n')

            dotlog('Output ready.')

