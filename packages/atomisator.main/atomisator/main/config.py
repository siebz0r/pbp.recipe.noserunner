import os
import sys
from os.path import join
from ConfigParser import ConfigParser
import re

DEFAULT_CONFIG_FILE = 'atomisator.cfg'

class AtomisatorConfig(object):

    def __init__(self, cfg=None):
        
        self._parser = ConfigParser()
        if cfg is None:
            cfg = DEFAULT_CONFIG_FILE
        if not os.path.exists(cfg):
            raise ValueError('Could not read configuration (%s)' % cfg)
        self._file = cfg
        self._parser.read([cfg])

    #
    # basic APIs
    #
    def _get_simple_field(self, field, default=None):
        if not self._parser.has_option('atomisator', field):
            return default
        return self._parser.get('atomisator', field).strip()
    
    def _set_simple_field(self, field, value):
        self._parser.set('atomisator', field, value)    


    def _set_multiline_value(self, name, value):

        def _quote(value):
            if ' ' in value:
                value = value.replace('"', "'")
                return '"%s"' % value
            return value

        def _line(entry):
            main = entry[0]
            params = [_quote(e) for e in entry[1]]
            return '%s %s' % (main, ' '.join(params))
        
        values = '\n'.join([_line(v) for v in value])
        self._parser.set('atomisator', name, values)

    def _get_multiline_value(self, name):
        v = self._parser.get('atomisator', name).split('\n')
        # crappy pattern matching
        def _rep(match):
            return match.groups()[0].replace(' ', ':::')
        def _args(p):
            p = re.sub(r'"(.*?)"', _rep, p)
            p = [e.replace(':::', ' ') 
                 for e in p.split() if e != '']
            return p[0].strip(), tuple([p.strip() 
                                        for p in p[1:]])
        return [_args(s) for s in v if s.strip() != '']

    # 
    # properties and public APIs
    #
    def write(self):
        f = open(self._file, 'w')
        try:
            self._parser.write(f)
        except:
            f.close()

    def get_reader(self, name):
        if not self._parser.has_section('readers'):
            return None
        if not self._parser.has_option('readers', name):
            return None
        return self._parser.get('readers', name)

    def _get_sources(self):
        return self._get_multiline_value('sources')
    def _set_sources(self, sources):
        self._set_multiline_value('sources', sources)
    sources = property(_get_sources, _set_sources)

    def _get_outputs(self):
        return self._get_multiline_value('outputs') 
    def _set_outputs(self, outputs):
        self._set_multiline_value('outputs', outputs)
    outputs = property(_get_outputs, _set_outputs)

    def _get_filters(self):
        return self._get_multiline_value('filters') 
    def _set_filters(self, filters):
        self._set_multiline_value('filters', filters)
    filters = property(_get_filters, _set_filters)

    def _get_enhancers(self):
        return self._get_multiline_value('enhancers')
    def _set_enhancers(self, value):
        self._set_multiline_value('enhancers', value)
    enhancers = property(_get_enhancers, _set_enhancers)

    def _get_database(self):
        return self._get_simple_field('database')
    def _set_database(self, value):
        self._set_simple_field('database', value)
    database = property(_get_database, _set_database)

    def _get_timeout(self):
        return self._get_simple_field('timeout', '5')
    def _set_timeout(self, value):
        self._set_simple_field('timeout', value)
    timeout = property(_get_timeout, _set_timeout)

