import sys

from atomisator.main.config import AtomisatorConfig
from atomisator.parser import parse 
from atomisator.db import config
from atomisator.db import create_entry
from atomisator.feed import generate

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

def atomisator():
    """Calling both."""
    load_feeds()
    generate_feed()

