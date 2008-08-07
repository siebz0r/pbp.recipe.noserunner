import sys
import os

from nose.tools import with_setup, assert_equals
from atomisator.main import atomisator, _parse_options
from atomisator.main import CONF_TMPL 

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
    from atomisator.main import generate_config 
    generate_config('here.cfg')

    assert_equals(open('here.cfg').read(), CONF_TMPL)

