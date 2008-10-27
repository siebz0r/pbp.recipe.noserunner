import os
from nose.tools import *

from atomisator.main.config import AtomisatorConfig
from atomisator.main.config import generate_config 
from atomisator.main.config import CONF_TMPL

cfg = os.path.join(os.path.dirname(__file__), 'test.cfg')

def gen_init():
    if os.path.exists('here.cfg'):
        os.remove('here.cfg')

@with_setup(setup=gen_init, teardown=gen_init)
def test_generation():
    # Let's try a generation
    generate_config('here.cfg')
    assert_equals(open('here.cfg').read(), CONF_TMPL)


def test_config():
    parser = AtomisatorConfig(cfg)
    s = parser.sources 
    waited = [('rss', ('gdigg.xml',)), ('rss', ('gtarek.xml',)), 
              ('rss', ('gpp.xml',)), ('rss', ('gdigg.xml',)), 
              ('rss', ('gtarek.xml',)), ('rss', ('gpp.xml',))]

    assert_equals(s, waited)
    parser.sources = (('rss', ('ok.xml',)),)
    assert_equals(parser.sources, [('rss', ('ok.xml',))])

    assert_equals(parser.database, 'sqlite:///gatomisator.db') 
    parser.database = 'sqlite://here'
    assert_equals(parser.database, 'sqlite://here')    

    assert_equals(parser.timeout, '5') 
    parser.timeout = '7'
    assert_equals(parser.timeout, '7')

    assert_equals(parser.store_entries, True) 
    parser.store_entries = False
    assert_equals(parser.store_entries, False)

    old = open(cfg).read()
    parser.write()
    new = open(cfg).read()
    assert new != old

    open(cfg, 'w').write(old)

def test_quotes():
    parser = AtomisatorConfig(cfg)
    rss = ('rss', ('output.xml',  'http://link.xml', 
             'This is the output', 
             'This is the description'))
    parser.outputs = [rss]

    assert_equals(parser.outputs, [rss])

