# -*- encoding: utf-8 -*-                                                      
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>                             
# 
from setuptools import setup, find_packages
import os
from os.path import join
from distutils.core import Extension 

version = '0.1.0'

long_description = open("README.txt").read()

classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Python Software Foundation License",

        ]

entry_points = {"atomisator.filters": ["indexer = atomisator.indexer:Indexer"]}

setup(name='atomisator.indexer',
      version=version,
      description="Atomisator - Indexing",
      long_description=long_description,
      classifiers=classifiers,
      keywords='atomisator indexer xapian',
      author='Tarek Ziade',
      author_email='tarek@ziade.org',
      url='http://atomisator.ziade.org',
      license='Python',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['atomisator'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'afpy.xap',
      ],
      entry_points=entry_points,
      )

