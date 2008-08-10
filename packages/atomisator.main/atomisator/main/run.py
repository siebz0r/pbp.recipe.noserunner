import sys
import os

from optparse import OptionParser
from optparse import OptionValueError
from setuptools.package_index import iter_entry_points

from atomisator.main.config import AtomisatorConfig
from atomisator.main import __version__ as VERSION

from atomisator.db.session import create_session
from atomisator.db.core import create_entry
from atomisator.db.core import get_entries
from atomisator.feed import generate

def _log(msg):
    print msg

CONF_TMPL = """\
[atomisator]

# put here the sources you wish to process
# the first parameter is the type of source
# and the following parameters are the arguments
# passed to the plugin
sources = 
    rss http://tarekziade.wordpress.com/atom 

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


def _get_plugin(name):
    plugins = list(iter_entry_points('atomisator.plugins', name))
    if len(plugins) == 0:
        # not found, let's try to get it
        # not implemented yet
        return None
    return plugins[0].load()

_fs = iter_entry_points('atomisator.filters')
_filters = dict([(f.name, f.load()()) for f in _fs])

def _apply_filters(filters, entries, entry):
    for name, args in filters:
        if name not in _filters:
            # XXX do discovery here
            continue
        entry = _filters[name](entry, entries, *args)
        if entry is None:
            return None
    return entry

def load_feeds(conf):
    """Fetches feeds."""
    parser = AtomisatorConfig(conf)
    create_session(parser.database)
    count = 0
    for plugin, args in parser.sources:
        # check if the plugin is available
        pl = _get_plugin(plugin)

        if pl is None:
            raise ValueError('%s plugin not found' % pl) 
            
        _log('Reading source %s' % ' '.join(args))
        scount = 0
        for entry in pl()(*args):
            entry = _apply_filters(parser.filters, get_entries(), entry)
            if entry is None:
                continue
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
    create_session(parser.database)
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
                          version='%%prog %s' % VERSION)

    parser.add_option("-c", "--create-config", dest="create",
                      action="store",
                      help="Creates a default config file",
                      metavar="CONFIG_FILE") 

    parser.add_option("-r", "--read", dest="read",
                      action="store_true",
                      help="Reads sources.", default=False)
   
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

def atomisator():
    options = _parse_options()
    if options.create is not None:
        generate_config(options.create)
        sys.exit(0)
    
    if options.read:
        load_feeds(options.config)
    if options.generate:
        generate_feed(options.config)

