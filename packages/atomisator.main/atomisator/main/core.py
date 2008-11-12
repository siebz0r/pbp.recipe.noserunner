# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
""" 
Core module. contains processor.
"""
import socket
import os

from multiprocessing import Pool
from multiprocessing import cpu_count
from multiprocessing import TimeoutError
from multiprocessing import Queue

from atomisator.main.config import log
from atomisator.main.config import dotlog
from atomisator.main.config import AtomisatorConfig
from atomisator.main import FILTERS
from atomisator.main import OUTPUTS
from atomisator.main import ENHANCERS
from atomisator.main import READERS
from atomisator.db.session import create_session
from atomisator.db.core import create_entry
from atomisator.db.core import get_entries
from atomisator.db.core import purge_entries

# we'll use two processes per CPU
PROCESSES = cpu_count() * 2

def _load_plugin(name, kind):
    """returns a registered plugin.
    
    Will raise an error if the plugin does not exists"""
    if name not in kind:
        raise ValueError('Could not load %s plugin.' % name)
    return kind[name]

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
    return entry

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
        log('Loading existing data.')
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
        log('\tRemoving old entries.')
        self._cleanup_entries()

        # initial entries, see if this call is optimal
        log('\tReading existing entries.')
        self.existing_entries = get_entries().all()

        # building filtering chain once.
        filter_names = [f[0] for f in self.parser.filters]
        log('Loading filters plugins : %s' % ', '.join(filter_names))
        self.filter_chain = set([(_load_plugin(name, FILTERS), args) 
                                 for name, args in self.parser.filters 
                                 if name in FILTERS])
        
        # building source chain once.
        source_names = [s[0] for s in self.parser.sources]
        log('Loading source plugins : %s' % ', '.join(source_names))
        sources = [(reader_name, _load_plugin(reader_name, READERS), args) 
                   for reader_name, args in self.parser.sources]

        # creating a processing pool
        pool = Pool(PROCESSES)
        
        # let's call in parallel all the readers
        log('Reading sources.')
        for source in sources:
            log('\tLaunching worker for %s - %s' % (source[0], source[-1]))
            pool.apply_async(_process_source, source, 
                             callback=self._process_entries)

        pool.close()
        pool.join()
        dotlog('\n')

    def _process_entries(self, entries):
        """callback called by the worker"""
        # now lets apply filters, then store entries
        psession = create_session(self.parser.database, 
                                  global_session=False) 
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
        
        # XXX TODO: limit the size of the data 
        # processed, by number of items, or by date
        entries = get_entries().all()
        
        if selected_enhancers != []:
            # Enhancement is a two-phase process.
            # 1. Preparing entries for enhancement
            log('Preparing enhancers.')
            for enhancer, args in selected_enhancers:
                if hasattr(enhancer, 'prepare'):
                    dotlog('.')
                    enhancer.prepare(entries)
            dotlog('\n')

            # 2. Now enhancing them
            log('Enhancing: %s' % ', '.join([e for e, args 
                                            in self.parser.enhancers]))

            # creating a processing pool
            pool = Pool(PROCESSES)
            results = [pool.apply_async(_enhance, (entry, selected_enhancers))
                       for entry in entries]

            pool.close()
            pool.join()
            entries = [result.get() for result in results]
            dotlog('\n')

        if selected_outputs != []:
            log('Writing outputs.')
            log('Rendering: %s' % ', '.join([output[0] for output 
                                             in self.parser.outputs]))
            for output, args in selected_outputs:
                dotlog('.')
                output(entries, args)
            dotlog('\n')

            log('Output ready.')

