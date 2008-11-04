import sys
import os

from nose.tools import *

from atomisator.main.commands import atomisator, _parse_options
from atomisator.main.commands import readers
from atomisator.main.config import AtomisatorConfig
from atomisator.main.config import ConfigurationError
from atomisator.main.core import DataProcessor
from atomisator.main.commands import enhancers, filters

from atomisator.main.tests.base import set_conf, tear_conf

saved = None

def setup():
    global saved
    saved = sys.argv

def teardown():
    sys.argv = saved

@with_setup(setup, teardown)
def test_options():
    # making sure we know how to parse options
    sys.argv = ['atomisator']
    options = _parse_options()
    assert_equals(options.read, True)
    assert_equals(options.generate, True)
    assert_equals(options.create, None)
    assert_equals(options.config, 'atomisator.cfg')

    sys.argv = ['atomisator', '-c', 'myfile.cfg']
    options = _parse_options()
    assert_equals(options.create, 'myfile.cfg')
    assert_equals(options.read, False)
    assert_equals(options.generate, False)

    sys.argv = ['atomisator', '-r', '-g', '-f', 'here.cfg']
    options = _parse_options()
    assert_equals(options.create, None)
    assert_equals(options.read, True)
    assert_equals(options.generate, True)
    assert_equals(options.config, 'here.cfg')

    sys.argv = ['atomisator', 'here.cfg']
    options = _parse_options()
    assert_equals(options.create, None)
    assert_equals(options.read, True)
    assert_equals(options.generate, True)
    assert_equals(options.config, 'here.cfg')

    sys.argv = ['atomisator', 'here.cfg', '-g']
    options = _parse_options()
    assert_equals(options.create, None)
    assert_equals(options.read, False)
    assert_equals(options.generate, True)
    assert_equals(options.config, 'here.cfg')

test_dir = os.path.dirname(__file__)
test_conf = os.path.join(test_dir, 'atomisator.cfg')

@with_setup(set_conf, tear_conf)
def test_load_data():

    DataProcessor(test_conf).load_data()

@with_setup(set_conf, tear_conf)
def test_generate_data():
    DataProcessor(test_conf).generate_data()

@with_setup(set_conf, tear_conf)
def test_config():
    parser = AtomisatorConfig(test_conf)
    sources = parser.sources
    sources.sort()
    dir = os.path.dirname(test_conf)
    wanted = [('rss', ('%s/digg.xml' % dir,)), 
              ('rss', ('%s/digg.xml' % dir,)), 
              ('rss', ('%s/pp.xml' % dir,)), 
              ('rss', ('%s/pp.xml' % dir,)), 
              ('rss', ('%s/tarek.xml' % dir,)),
              ('rss', ('%s/tarek.xml' % dir,))]


    assert_equals(sources, wanted)
    wanted = os.path.join(dir, 'atomisator.db')
    assert_equals(parser.database, 'sqlite:///%s' % wanted)

    # getting readers
    assert_equals(parser.get_reader('xxx'), None)
    assert_equals(parser.get_reader('xml'), 
                  'atomisator.reader.xml')

    f = [f[0] for f in parser.filters]
    f.sort()
    assert_equals(f, ['autotags', 'buzzwords', 'doublons', 'spam', 'stopwords'])

def test_get_readers():
    # see if we get the rss and atom plugin
    from atomisator.parser import Parser
   
    assert 'xxxx' not in readers
    assert isinstance(readers['rss'], Parser)

def test_filters():
    assert 'doublons' in filters

def test_enhancers():
    assert 'digg' in enhancers

@with_setup(set_conf, tear_conf)
def test_no_storage():
    proc = DataProcessor(test_conf)
    proc.parser.store_entries = False
   
    proc.load_data()
    proc.generate_data()   
       
    # as usual but in memory
    assert_equals(len(proc.existing_entries), 23)

