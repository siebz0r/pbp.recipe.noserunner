#!/usr/bin/env python

from setuptools import setup, find_packages

TracMercurial = 'http://trac.edgewall.org/wiki/TracMercurial',

setup(name='TracMercurial',
      install_requires='Trac >=0.11dev, ==0.11b1',
      description='Mercurial plugin for Trac 0.11',
      keywords='trac scm plugin mercurial hg',
      version='0.11.0.2',
      url=TracMercurial,
      license='GPL',
      author='Christian Boos',
      author_email='cboos@neuf.fr',
      long_description="""
      This plugin for Trac 0.11 provides support for the Mercurial SCM.
      
      See %s for more details.
      """ % TracMercurial,
      packages=['tracext', 'tracext.hg'],
      data_files=['COPYING', 'README'],
      entry_points={'trac.plugins': 'hg = tracext.hg.backend'})
