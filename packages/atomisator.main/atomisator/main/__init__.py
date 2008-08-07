import sys
import os

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

CONF_TMPL = """\
[atomisator]

# put here the feeds you wish to parse
sites = 
    http://tarekziade.wordpress.com/atom

# put here the database location
database = sqlite:///atomisator.db

# this is the file that will be generated
file = atomisator.xml

# infos that will appear in the generated feed. 
title = meta
description = Automatic feed created by Atomisator.
link =  http://atomisator.ziade.org/example
"""

def generate_config(path):
    """creates a default config file"""
    if os.path.exists(path):
        raise ValueError('%s already exists.' % path)
    f = open(path, 'w')
    try:
        f.write(CONF_TMPL)
    finally:
        f.close()
    _log('Default config generated at "%s."' % path)

def load_feeds(conf):
    """Fetches feeds."""
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

def generate_feed(conf):
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

    parser.add_option("-c", "--create-config", dest="create",
                      action="store",
                      help="Creates a default config file",
                      metavar="CONFIG_FILE") 

    parser.add_option("-r", "--read", dest="read",
                      action="store_true",
                      help="Reads sources.", default=True)
   
    parser.add_option("-g", "--generate", dest="generate",
                      action="store_true",
                      help="Generates feed.", default=True)
        
    parser.add_option("-f", "--config-file", dest="config",
                      help="Points to the configuration file.",
                      metavar="CONFIG_FILE") 
    
    
    options, args = parser.parse_args()

    if options.create is not None:
        options.read = False
        options.generate = False
    else:
        if options.config is None:
            if len(args) > 0:
                options.config = args[0]
            else:
                options.config = 'atomisator.cfg'

        if options.read is False and options.generate is False:
            options.read = True
            options.generate = True

    return options

def atomisator():
    options = _parse_options()
    if options.create is not None:
        generate_config(options.create)
        sys.exit(0)
    
    if options.read:
        load_feeds(options.config)
    if options.generate:
        generate_feed(options.config)

