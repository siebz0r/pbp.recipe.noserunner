import sys
import os
import socket

from optparse import OptionParser
from optparse import OptionValueError
from setuptools.package_index import iter_entry_points

from atomisator.main.config import AtomisatorConfig
from atomisator.main import __version__ as VERSION

from atomisator.db.session import create_session
from atomisator.db.core import create_entry
from atomisator.db.core import get_entries
from atomisator.feed import generate
from atomisator.db.session import commit

def _log(msg):
    print msg

CONF_TMPL = """\
[atomisator]

# put here the sources you wish to process
# the first parameter is the type of source
# and the following parameters are the arguments
# passed to the reader
sources = 
    rss http://tarekziade.wordpress.com/atom 
    rss http://digg.com/rss/index.xml

# put here the filters you want to use
filters =
    doublons

# put here the enhancers you want to use
enhancers =

# put here the database location
database = sqlite:///atomisator.db

# this is the filename that will be generated
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


def _get_reader(name):
    readers = list(iter_entry_points('atomisator.readers', name))
    if len(readers) == 0:
        # not found, let's try to get it
        # not implemented yet
        return None
    return readers[0].load()

_fs = iter_entry_points('atomisator.filters')
_filters = dict([(f.name, f.load()()) for f in _fs])

def _apply_filters(entry, entries, filters):
    for f, args in filters:
        entry = f(entry, entries, *args)
        if entry is None:
            return None
    return entry

def load_feeds(conf):
    """Fetches feeds."""
    parser = AtomisatorConfig(conf)
    old_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(float(parser.timeout))

    create_session(parser.database)
    count = 0

    # initial entries, see if this call is optimal
    existing_entries = get_entries().all()

    filter_chain = set([(_filters[name], args) 
                        for name, args in parser.filters 
                        if name in _filters])
    for reader, args in parser.sources:
        # check if the readers is available
        pl = _get_reader(reader)

        if pl is None:
            raise ValueError('%s reader not found for %s' \
                        % (pl, ' '.join(args))) 
            
        _log('Reading source %s' % ' '.join(args))
        scount = 0

        for entry in pl()(*args):
            entry = _apply_filters(entry, existing_entries, filter_chain)
            if entry is None:
                continue
            id_, new_entry = create_entry(entry, commit=False)
            count += 1
            scount += 1
            existing_entries.append(new_entry)
        _log('%d entries read.' % scount)
    _log('%d total.' % count)
    commit()    # final commit
    socket.setdefaulttimeout(old_timeout)

_es = iter_entry_points('atomisator.enhancers')
_enhancers = dict([(e.name, e.load()()) for e in _es])

def _select_enhancers(enhancers):
    res = []
    for name, args in enhancers:
        if name in _enhancers:
            res.append((_enhancers[name], args))
    return res

def generate_feed(conf):
    """Creates the meta-feed."""
    if conf is None:
        conf = _get_opt()
    parser = AtomisatorConfig(conf)
    create_session(parser.database)
    _log('Writing feed in %s' % parser.file)
    enhancers = _select_enhancers(parser.enhancers)
    feed = generate(parser.title, parser.description, parser.link, enhancers)
    
    f = open(parser.file, 'w')
    try:
        f.write(feed)
    finally:
        f.close()
    _log('Feed ready.')

def _parse_options():
    """Calling both."""
    parser = OptionParser(usage='usage: %prog [options]',
                          version='%%prog %s' % VERSION)

    parser.add_option("-c", "--create-config", dest="create",
                      action="store",
                      help="Creates a default config file.",
                      metavar="CONFIG_FILE") 

    parser.add_option("-r", "--read", dest="read",
                      action="store_true",
                      help="Reads sources.", default=False)
 
    parser.add_option("-l", "--list-filters", dest="filters",
                      action="store_true",
                      help="List all filters.", default=False)
   
    parser.add_option("-p", "--list-readers", dest="readers",
                      action="store_true",
                      help="List all readers.", default=False)

    parser.add_option("-e", "--list-enhancers", dest="enhancers",
                      action="store_true",
                      help="List all enhancers.", default=False)

    parser.add_option("-g", "--generate", dest="generate",
                      action="store_true",
                      help="Generates feed.", default=False)
        
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

def list_readers():
    for p in iter_entry_points('atomisator.readers'):
        print p.name
        d = p.load().__doc__
        if d is not None:
            print d
            
def list_filters():
    for key, ob in _filters.items():
        print '%s: %s' % (key, ob.__doc__)

def list_enhancers():
    for key, ob in _enhancers.items():
        print '%s: %s' % (key, ob.__doc__)

def atomisator():
    options = _parse_options()
    if options.filters:
        list_filters()
        sys.exit(0)

    if options.readers:
        list_readers()
        sys.exit(0)

    if options.enhancers:
        list_enhancers()
        sys.exit(0)

    if options.create is not None:
        generate_config(options.create)
        sys.exit(0)
    
    if options.read:
        load_feeds(options.config)
    if options.generate:
        generate_feed(options.config)

