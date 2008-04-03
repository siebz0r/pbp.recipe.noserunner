import os
import sys
from os.path import join
from ConfigParser import ConfigParser

CONFIG_FILE = 'atomisator.cfg'

places = [join(os.path.dirname(__file__), CONFIG_FILE),
          join(os.path.expanduser('~'), CONFIG_FILE)]

if sys.platform != 'win32':
    places.insert(0, '/etc/%s'+CONFIG_FILE)

conf = None
for place in places:
    if os.path.exists(place):
        conf = place
        break

if conf is None:
    raise ValueError('Could not find %s' % CONFIG_FILE)

class AtomisatorConfig(ConfigParser):

    def __init__(self, cfg):
        ConfigParser.__init__(self)
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

parser = AtomisatorConfig(conf)

