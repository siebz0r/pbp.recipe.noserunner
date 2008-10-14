__version__ = '0.5.0'
from setuptools.package_index import iter_entry_points

def _load_entry_point(name):
    """Loads an atomisator entry point."""
    it = iter_entry_points(name)
    return dict([(e.name, e.load()()) 
                 for e in it])

filters = _load_entry_point('atomisator.filters')
outputs = _load_entry_point('atomisator.outputs')
enhancers = _load_entry_point('atomisator.enhancers')
readers = _load_entry_point('atomisator.readers')

