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

    def _get_feeds(self):
        return [site.strip() for site in 
                self.get('atomisator', 'sites').split('\n')
                if site.strip() != '']
    feeds = property(_get_feeds)

    def _get_simple_field(self, field):
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

    def _get_link(self):
        return self._get_simple_field('link')
    link = property(_get_link)

    def _get_file(self):
        return self._get_simple_field('file')
    file = property(_get_file)

