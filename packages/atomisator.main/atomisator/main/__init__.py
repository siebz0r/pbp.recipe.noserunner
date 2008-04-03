from atomisator.main.config import parser
from atomisator.parser import parse 
from atomisator.db import config
from atomisator.db import create_entry
from atomisator.feed import generate

config.SQLURI = parser.database

def _log(msg):
    print msg

def load_feeds():
    """Fetches feeds."""
    count = 0
    def _count():
        count += 1
    for feed in parser.feeds:
        _log('Parsing feed %s' % feed)
        for entry in parse(feed):
            _count()
            create_entry(entry)
    _log('%d entries read.' % count)

def generate_feed():
    """Creates the meta-feed."""
    _log('Writing feed in %s' % parser.file) 
    feed = generate(parser.title, parser.description, parser.link) 
    open(parser.file, 'w').write(feed)
    _log('Feed ready.')

def atomisator():
    """Calling both."""
    load_feeds()
    generate_feed()

