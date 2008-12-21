# -*- encoding: utf-8 -*-                                                      
# (C) Copyright 2008 Tarek Ziadé <tarek@ziade.org>                             
# 
from setuptools import setup, find_packages
import os
from os.path import join
from distutils.core import Extension 

version = '0.2.0'

long_description = open("README.txt").read()

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
                                       "delicious = atomisator.filters.followers:DeliciousFollower",
                                       "guesslang = atomisator.filters:GuessLang"]}

ext_levenshtein = Extension('Levenshtein', 
        sources = [join('atomisator', 'filters', 'levenshtein', 'Levenshtein.c')]) 

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
      ext_modules=[ext_levenshtein]
)
