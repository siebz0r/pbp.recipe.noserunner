import sys
from nose.tools import with_setup, assert_equals
from atomisator.main import atomisator, _parse_options

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

