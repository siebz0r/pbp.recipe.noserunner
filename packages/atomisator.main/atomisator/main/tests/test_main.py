import sys
import os

from nose.tools import with_setup, assert_equals

from atomisator.main.run import atomisator, _parse_options
from atomisator.main.run import CONF_TMPL, _get_reader 
from atomisator.main.config import AtomisatorConfig
from atomisator.main.run import generate_config 
from atomisator.main.run import load_feeds, generate_feed
from atomisator.main.run import _enhancers, _filters

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

def gen_init():
    if os.path.exists('here.cfg'):
        os.remove('here.cfg')

@with_setup(setup=gen_init, teardown=gen_init)
def test_generation():
    # Let's try a generation
    generate_config('here.cfg')
    assert_equals(open('here.cfg').read(), CONF_TMPL)

test_dir = os.path.dirname(__file__)
package_dir = os.path.split(test_dir)[0]
test_conf = os.path.join(test_dir, 'atomisator.cfg')

def set_conf():
    template = open(os.path.join(test_dir, 'atomisator.cfg_tmpl')).read()
    cfg = template % {'test_dir': test_dir}
    f = open(test_conf, 'w')
    f.write(cfg)
    f.close()

def tear_conf():
    if os.path.exists(test_conf):
        os.remove(test_conf)
    xml = os.path.join(test_dir, 'atomisator.xml')
    if os.path.exists(xml):
        os.remove(xml)

@with_setup(set_conf, tear_conf)
def test_load_feeds():
    load_feeds(test_conf)

@with_setup(set_conf, tear_conf)
def test_generate_feed():
    generate_feed(test_conf)

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
    
    assert_equals(_get_reader('xxxx'), None)
    assert_equals(_get_reader('rss'), Parser)

def test_filters():
    assert 'doublons' in _filters

def test_enhancers():
    assert 'digg' in _enhancers

