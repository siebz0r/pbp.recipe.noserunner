import os
import sys
from os.path import join
from ConfigParser import ConfigParser

DEFAULT_CONFIG_FILE = 'atomisator.cfg'

class AtomisatorConfig(object):

    def __init__(self, cfg=None):
        
        self._parser = ConfigParser()
        if cfg is None:
            cfg = DEFAULT_CONFIG_FILE
        if not os.path.exists(cfg):
            raise ValueError('Could not read configuration (%s)' % cfg)
        self._parser.read([cfg])

    def _set_multiline_value(self, name, value):

        def _line(entry):
            return '%s %s' % (entry[0], ' '.join(entry[1]))
        values = '\n'.join([_line(v) for v in value])
        self._parser.set('atomisator', name, values)

    def get_reader(self, name):
        if not self._parser.has_section('readers'):
            return None
        if not self._parser.has_option('readers', name):
            return None
        return self._parser.get('readers', name)

    def _get_sources(self):
        sources = self._parser.get('atomisator', 'sources').split('\n')
        def _args(p):
            p = p.split()
            return p[0].strip(), tuple([p.strip() 
                                        for p in p[1:]])
        return [_args(s) for s in sources if s.strip() != '']

    def _set_sources(self, sources):
        self._set_multiline_value('sources', sources)

    sources = property(_get_sources, _set_sources)

    def _get_filters(self):
        if not self._parser.has_option('atomisator', 'filters'):
            return []
        filters = self._parser.get('atomisator', 'filters').split('\n')
        def _args(p):
            p = p.split()
            return p[0].strip(), tuple([p.strip() 
                                        for p in p[1:]])
        return [_args(s) for s in filters if s.strip() != '']

    def _set_filters(self, filters):
        self._set_multiline_value('filters', filters)

    filters = property(_get_filters, _set_filters)

    def _get_enhancers(self):
        if not self._parser.has_option('atomisator', 'enhancers'):
            return []
        enhancers = self._parser.get('atomisator', 'enhancers').split('\n')
        def _args(p):
            p = p.split()
            return p[0].strip(), tuple([p.strip() 
                                        for p in p[1:]])
        return [_args(e) for e in enhancers if e.strip() != '']
    
    def _set_enhancers(self, value):
        self._set_multiline_value('enhancers', value)

    enhancers = property(_get_enhancers, _set_enhancers)

    def _get_simple_field(self, field, default=None):
        if not self._parser.has_option('atomisator', field):
            return default
        return self._parser.get('atomisator', field).strip()
    
    def _set_simple_field(self, field, value):
        self._parser.set('atomisator', field, value)    

    def _get_database(self):
        return self._get_simple_field('database')

    def _set_database(self, value):
        self._set_simple_field('database', value)

    database = property(_get_database, _set_database)

    def _get_title(self):
        return self._get_simple_field('title')
    
    def _set_title(self, value):
        self._set_simple_field('title', value)

    title = property(_get_title, _set_title)

    def _get_description(self):
        return self._get_simple_field('description')

    def _set_description(self, value):
        self._set_simple_field('description', value) 

    description = property(_get_description, _set_description)

    def _get_timeout(self):
        return self._get_simple_field('timeout', '5')
    
    def _set_timeout(self, value):
        self._set_simple_field('timeout', value)

    timeout = property(_get_timeout, _set_timeout)

    def _get_link(self):
        return self._get_simple_field('link')
    
    def _set_link(self, value):
        self._set_simple_field('link', value)

    link = property(_get_link, _set_link)

    def _get_file(self):
        return self._get_simple_field('file')

    def _set_file(self, value):
        self._set_simple_field('file', value)   

    file = property(_get_file, _set_file)

