# -*- encoding: utf-8 -*-                                                      
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>                             
# 
from setuptools import setup, find_packages
import os
from os.path import join
from distutils.core import Extension 

version = '0.1.8'

long_description = open("README.txt").read()

includes = [join('probstat', 'include'), 
             join('probstat', 'python')]
libraries = [] 

files = [
         join('probstat', 'base', 'cartesian_base.c'),
         join('probstat', 'base', 'permutation_base.c'),
         join('probstat', 'base', 'combination_base.c'),
         join('probstat', 'base', 'pqueue_base.c'),
         join('probstat', 'python', 'cartesian.c'),
         join('probstat', 'python', 'permutation.c'),
         join('probstat', 'python', 'combination.c'),
         join('probstat', 'python', 'pqueue.c'),
         join('probstat', 'python', 'stats_module.c'),
        ]


classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]

entry_points = {"atomisator.filters": ["stopwords = atomisator.filters:StopWords",
                                       "buzzwords = atomisator.filters:BuzzWords",
                                       "doublons = atomisator.filters:Doublons",
                                       "spam = atomisator.filters:Spam",
                                       "replace = atomisator.filters:ReplaceWords",
                                       "autotag = atomisator.filters:AutoTag",
                                       "reddit = atomisator.filters.followers:RedditFollower",
                                       "delicious = atomisator.filters.followers:DeliciousFollower"]}

setup(name='atomisator.filters',
      version=version,
      description="Expert Python Programming - Filters",
      long_description=long_description,
      classifiers=classifiers,
      keywords='python best practices',
      author='Tarek Ziade',
      author_email='tarek@ziade.org',
      url='http://atomisator.ziade.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['atomisator'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'BeautifulSoup',
      ],
      entry_points=entry_points,
      #ext_modules = [Extension("probstat", files,
      #                         libraries = libraries,
      #                         include_dirs =  includes,
      #                        )
      #              ],

      )
