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

from atomisator.main.config import log
from atomisator.main.config import dotlog
from atomisator.main.config import AtomisatorConfig
from atomisator.main import filters
from atomisator.main import outputs
from atomisator.main import enhancers
from atomisator.main import readers
from atomisator.db.session import create_session
from atomisator.db.core import create_entry
from atomisator.db.core import get_entries

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
        if name in enhancers:
            res.append((enhancers[name], args))
    return res

def _select_outputs(outputs_selected):
    """Gets the selected outputs."""
    res = []
    for name, args in outputs_selected:
        if name in outputs:
            res.append((outputs[name], args))
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
        log('Retrieving from %s - %s' %  (reader_name, str(reader_args)))
        return reader(*reader_args)
    except TimeoutError:
        log('TIMEOUT on %s - %s' % (reader_name, str(reader_args)))
        return []

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
        log('Reading data.')
        old_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(float(self.parser.timeout))
        try:
            self._load_data()
        finally:
            socket.setdefaulttimeout(old_timeout)
    
    def _load_data(self):
        """Loads the data"""
        # remove the temp db if it exists
        if os.path.exists('_temp_.db'):
            os.remove('_temp_.db')
        
        # initial entries, see if this call is optimal
        self.existing_entries = get_entries().all()

        # building filtering chain once.
        self.filter_chain = set([(_load_plugin(name, filters), args) 
                                 for name, args in self.parser.filters 
                                 if name in filters])
        
        # building source chain once.
        sources = [(reader_name, _load_plugin(reader_name, readers), args) 
                   for reader_name, args in self.parser.sources]

        # creating a processing pool
        pool = Pool(PROCESSES)
        
        # let's call in parallel all the readers
        for source in sources:
            log('Launching worker for %s - %s' % (source[0], source[-1]))
            pool.apply_async(_process_source, source, 
                             callback=self._process_entries)

        pool.close()
        pool.join()
         
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
            id_, new_entry = create_entry(entry, commit=False,
                                          session=psession)
            self.existing_entries.append(new_entry)
        psession.commit()

    def generate_data(self):
        """Generates the output"""
        log('Writing outputs.')
        selected_enhancers = _select_enhancers(self.parser.enhancers)
        selected_outputs = _select_outputs(self.parser.outputs)
        
        # XXX TODO: limit the size of the data 
        # processed, by number of items, or by date
        entries = get_entries().all()
        # Enhancement is a two-phase process.
        # 1. Preparing entries for enhancement
        for e, args in selected_enhancers:
            if hasattr(e, 'prepare'):
                e.prepare(entries)

        # 2. Now enhancing them
        def _enhance(entry):
            for e, args in selected_enhancers:
                entry = e(entry, *args)
            return entry
       
        entries = [_enhance(e) for e in entries]

        for output, args in selected_outputs:
            output(entries, args)

        log('Data ready.')

