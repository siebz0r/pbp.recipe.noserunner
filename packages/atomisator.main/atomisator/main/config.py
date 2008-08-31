import os
import sys
from os.path import join
from ConfigParser import ConfigParser

DEFAULT_CONFIG_FILE = 'atomisator.cfg'

class AtomisatorConfig(ConfigParser):
    def __init__(self, cfg=None):
        ConfigParser.__init__(self)
        if cfg is None:
            cfg = DEFAULT_CONFIG_FILE
        if not os.path.exists(cfg):
            raise ValueError('Could not read configuration (%s)' % cfg)
        self.read([cfg])

    def get_reader(self, name):
        if not self.has_section('readers'):
            return None
        if not self.has_option('readers', name):
            return None
        return self.get('readers', name)

    def _get_sources(self):
        sources = self.get('atomisator', 'sources').split('\n')
        def _args(p):
            p = p.split()
            return p[0].strip(), tuple([p.strip() 
                                        for p in p[1:]])
        return [_args(s) for s in sources if s.strip() != '']
    sources = property(_get_sources)

    def _get_filters(self):
        if not self.has_option('atomisator', 'filters'):
            return []
        filters = self.get('atomisator', 'filters').split('\n')
        def _args(p):
            p = p.split()
            return p[0].strip(), tuple([p.strip() 
                                        for p in p[1:]])
        return [_args(s) for s in filters if s.strip() != '']
    filters = property(_get_filters)

    def _get_enhancers(self):
        if not self.has_option('atomisator', 'enhancers'):
            return []
        enhancers = self.get('atomisator', 'enhancers').split('\n')
        def _args(p):
            p = p.split()
            return p[0].strip(), tuple([p.strip() 
                                        for p in p[1:]])
        return [_args(e) for e in enhancers if e.strip() != '']
    enhancers = property(_get_enhancers)

    def _get_simple_field(self, field, default=None):
        if not self.has_option('atomisator', field):
            return default
        return self.get('atomisator', field).strip()

    def _get_database(self):
        return self._get_simple_field('database')
    database = property(_get_database)

    def _get_title(self):
        return self._get_simple_field('title')
    title = property(_get_title)

    def _get_description(self):
        return self._get_simple_field('description')
    description = property(_get_description)

    def _get_timeout(self):
        return self._get_simple_field('timeout', '5')
    timeout = property(_get_timeout)

    def _get_link(self):
        return self._get_simple_field('link')
    link = property(_get_link)

    def _get_file(self):
        return self._get_simple_field('file')
    file = property(_get_file)

