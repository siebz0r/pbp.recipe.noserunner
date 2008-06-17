#!/usr/bin/env python

from setuptools import setup, find_packages

TracMercurial = 'http://trac.edgewall.org/wiki/TracMercurial',

setup(name='TracMercurial',
      description='Mercurial plugin for Trac 0.10',
      keywords='trac scm plugin mercurial hg',
      version='0.10.0.2',
      url=TracMercurial,
      license='GPL',
      author='Christian Boos',
      author_email='cboos@neuf.fr',
      long_description="""
      This plugin for Trac 0.10 provides support for the Mercurial SCM.
      
      See %s for more details.
      """ % TracMercurial,
      packages=['tracvc', 'tracvc.hg'],
      data_files=['COPYING', 'README'],
      entry_points={'trac.plugins': 'hg = tracvc.hg.backend'})
