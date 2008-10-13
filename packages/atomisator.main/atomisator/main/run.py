import sys
import os
import socket

from optparse import OptionParser
from optparse import OptionValueError
from itertools import chain

from processing import Pool
from processing import cpuCount

from setuptools.package_index import iter_entry_points

from atomisator.main.config import logger
from atomisator.main.config import AtomisatorConfig
from atomisator.main import __version__ as VERSION

from atomisator.db.session import create_session
from atomisator.db.core import create_entry
from atomisator.db.core import get_entries
from atomisator.db.session import commit

# we'll use two processes per CPU
PROCESSES = cpuCount() * 2

# logging

def _log(msg):
    logger.info(msg)

# see how this can be done with logging
def _dot_log(msg):      
    sys.stdout.write('.')
    sys.stdout.flush()


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

outputs =
    rss atomisator.xml http://atomisator.ziade.org/example meta Automatic feed created by Atomisator. 

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

_os = iter_entry_points('atomisator.outputs')
_outputs = dict([(o.name, o.load()()) for o in _os])

def _apply_filters(entry, entries, filters):
    for f, args in filters:
        entry = f(entry, entries, *args)
        if entry is None:
            return None
    return entry

def _process_source(args):
    reader_name, reader, reader_args = args
    try:
        _log('Retrieving from %s - %s' %  (reader_name, str(reader_args)))
        return reader()(*reader_args)
    except TimeoutError:
        _log('TIMEOUT on %s - %s' % (reader_name, str(reader_args)))
        return []

def load_data(conf):
    """Fetches data."""
    _log('Reading data.')

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
    
    # first, check if all readers are available
    def _load_reader(reader_name):
        pl = _get_reader(reader_name)
        if pl is None:
            raise ValueError('%s reader not found' % name)
        return pl

    sources = [(reader_name, _load_reader(reader_name), args) 
               for reader_name, args in parser.sources]

    # create a processing pool
    pool = Pool(PROCESSES)
    
    # let's call in parallel all the readers
    entries = chain(*pool.imapUnordered(_process_source, sources))

    _log('Now processing entries')
    for pos, entry in enumerate(entries):
        _dot_log('.')
        entry = _apply_filters(entry, existing_entries, filter_chain)
        if entry is None:
            continue
        id_, new_entry = create_entry(entry, commit=False)
        existing_entries.append(new_entry)

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

def _select_outputs(outputs):
    res = []
    for name, args in outputs:
        if name in _outputs:
            res.append((_outputs[name], args))
    return res

def generate_data(conf):
    """Creates the meta-feed."""
    _log('Writing outputs.')
    if conf is None:
        conf = _get_opt()
    parser = AtomisatorConfig(conf)
    create_session(parser.database)

    enhancers = _select_enhancers(parser.enhancers)
    outputs = _select_outputs(parser.outputs)

    entries = get_entries().all()
   
    for output, args in outputs:
        output(entries, enhancers, args)

    _log('Data ready.')

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

def list_outputs():
    for key, ob in _outputs.items():
        print '%s: %s' % (key, ob.__doc__)
           
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
        load_data(options.config)
    if options.generate:
        generate_data(options.config)

