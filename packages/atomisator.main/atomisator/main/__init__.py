# -*- encoding: utf-8 -*-
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>
"""Main module, loads entry points
"""
__version__ = '0.5.3'

from setuptools.package_index import iter_entry_points

def _load_entry_point(name):
    """Loads an atomisator entry point."""
    entry_points = iter_entry_points(name)
    return dict([(e.name, e.load()()) for e in entry_points])

FILTERS = _load_entry_point('atomisator.filters')
OUTPUTS = _load_entry_point('atomisator.outputs')
ENHANCERS = _load_entry_point('atomisator.enhancers')
READERS = _load_entry_point('atomisator.readers')

