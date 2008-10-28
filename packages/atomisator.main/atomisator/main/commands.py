import sys
from optparse import OptionParser

from atomisator.main.core import DataProcessor
from atomisator.main.config import generate_config

from atomisator.main import __version__ as VERSION
from atomisator.main import filters
from atomisator.main import outputs
from atomisator.main import enhancers
from atomisator.main import readers

def _parse_options():
    """parses Atomisator args options"""
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
    """List out readers plugins."""
    for reader_name, reader in readers.items():
        print reader_name
        doc = reader.__doc__
        if doc is not None:
            print doc

def list_outputs():
    """List out output plugins."""
    for output_name, output in outputs.items():
        print '%s: %s' % (output_name, output.__doc__)
           
def list_filters():
    """List out filter plugins."""
    for filter_name, filter_ in filters.items():
        print '%s: %s' % (filter_name, filter_.__doc__)

def list_enhancers():
    """List out enhancers plugins."""
    for enhancer_name, enhancer in enhancers.items():
        print '%s: %s' % (enhancer_name, enhancer.__doc__)

def atomisator():
    """Main function."""
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
   
    if options.read or options.generate:
        processor = DataProcessor(options.config)

    if options.read:
        processor.load_data()

    if options.generate:
        processor.generate_data()

