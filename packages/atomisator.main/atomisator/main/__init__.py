import sys
from optparse import OptionParser
from optparse import OptionValueError

from atomisator.main.config import AtomisatorConfig
from atomisator.parser import parse 
from atomisator.db import config
from atomisator.db import create_entry
from atomisator.feed import generate

__version__ = '0.2.0'

def _log(msg):
    print msg

def _get_opt():
    if len(sys.argv) == 2:
        return sys.argv[1]
    return None

def load_feeds(conf=None):
    """Fetches feeds."""
    if conf is None:
        # trying to get sys.argv
        conf = _get_opt()
    parser = AtomisatorConfig(conf)
    count = 0
    for feed in parser.feeds:
        _log('Parsing feed %s' % feed)
        scount = 0
        for entry in parse(feed):
            create_entry(entry)
            count += 1
            scount += 1
        _log('%d entries read.' % scount)
    _log('%d total.' % count)

def generate_feed(conf=None):
    """Creates the meta-feed."""
    if conf is None:
        conf = _get_opt()
    parser = AtomisatorConfig(conf)
    _log('Writing feed in %s' % parser.file) 
    feed = generate(parser.title, parser.description, parser.link)
    
    f = open(parser.file, 'w')
    try:
        f.write(feed)
    finally:
        f.close()
    _log('Feed ready.')

def _parse_options():
    """Calling both."""
    parser = OptionParser(usage='usage: %prog [options]',
                          version='%%prog %s' % __version__)

    parser.add_option("-r", "--read", dest="read",
                      action="store_false",
                      help="Reads sources.", default=True)
   
    parser.add_option("-g", "--generate", dest="generate",
                      action="store_false",
                      help="Generates feed.", default=True)

    parser.add_option("-c", "--create-config", dest="create",
                      help="Creates a default config file") 
    
    parser.add_option("-f", "--config-file", dest="config",
                      help="Points to the configuration file",
                      default="atomisator.cfg") 
    
    
    return parser.parse_args()[0]

def atomisator():
    options, args = _parse_options()
    load_feeds()
    generate_feed()

