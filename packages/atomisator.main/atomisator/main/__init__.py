# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
"""Main module, loads entry points
"""
__version__ = '0.5.2'

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

