import sys
import os
import socket
from os.path import join
from os.path import dirname

from itertools import chain

from processing import Pool
from processing import cpuCount
from processing import TimeoutError

from atomisator.main.config import log
from atomisator.main.config import dotlog
from atomisator.main.config import generate_config
from atomisator.main.config import AtomisatorConfig
from atomisator.main import __version__ as VERSION
from atomisator.main import filters
from atomisator.main import outputs
from atomisator.main import enhancers
from atomisator.main import readers
from atomisator.db.session import create_session
from atomisator.db.core import create_entry
from atomisator.db.core import get_entries
from atomisator.db.session import commit

# we'll use two processes per CPU
PROCESSES = cpuCount() * 2

class DataProcessor(object):
    """Atomisator processor
    
    Knows how to load datas and generate outputs.
    """

    def __init__(self, conf):
        self.parser = AtomisatorConfig(conf) 
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
    
    def _load_plugin(self, name, kind):
            if name not in kind:
                raise ValueError('Could not load %s plugin.' % name)
            return kind[name]

    def _load_data(self):
        log('Reading data.')
        count = 0
        # initial entries, see if this call is optimal
        existing_entries = get_entries().all()

        # building filtering chain once.
        filter_chain = set([(self._load_plugin(name, filters), args) 
                            for name, args in self.parser.filters 
                            if name in filters])
        
        # building source chain once.
        sources = [(reader_name, self._load_plugin(reader_name, readers), args) 
                   for reader_name, args in self.parser.sources]

        # creating a processing pool
        pool = Pool(PROCESSES)
        
        # let's call in parallel all the readers
        entries = chain(*[f for f in 
                          pool.imapUnordered(self._process_source, sources)])

        # now lets apply filters, then store entries
        log('Now processing entries')
        for pos, entry in enumerate(entries):
            dotlog('.')
            entry = self._apply_filters(entry, existing_entries, filter_chain)
            if entry is None:
                continue
            id_, new_entry = create_entry(entry, commit=False)
            existing_entries.append(new_entry)

        # all done, let's commit
        commit()   

    def generate_data(self):
        """Generates the output"""
        log('Writing outputs.')
        enhancers = self._select_enhancers(self.parser.enhancers)
        outputs = self._select_outputs(self.parser.outputs)
        entries = get_entries().all()
    
        for output, args in outputs:
            output(entries, enhancers, args)
        log('Data ready.')

    def _apply_filters(self, entry, entries, filters):
        """Applies all selected filters to an entry"""
        for f, args in filters:
            entry = f(entry, entries, *args)
            if entry is None:
                return None
        return entry

    def _process_source(self, args):
        """processing one source. callable through 
        a process"""
        reader_name, reader, reader_args = args
        try:
            log('Retrieving from %s - %s' %  (reader_name, str(reader_args)))
            return reader(*reader_args)
        except TimeoutError:
            log('TIMEOUT on %s - %s' % (reader_name, str(reader_args)))
            return []

    def _select_enhancers(self, enhancers_selected):
        res = []
        for name, args in enhancers_selected:
            if name in enhancers:
                res.append((enhancers[name], args))
        return res

    def _select_outputs(self, outputs_selected):
        res = []
        for name, args in outputs_selected:
            if name in outputs:
                res.append((outputs[name], args))
        return res

