# -*- coding: utf-8 -*-
# Copyright (c) 2008 'Tarek Ziadé'

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
This module contains the tool of pbp.buildbotenv
"""
import os
from setuptools import setup, find_packages

version = '0.2.0'

README = os.path.join(os.path.dirname(__file__),
                      'README.txt')

long_description = open(README).read() + '\n\n'
tests_require = ['zope.testing',]

setup(name='pbp.buildbotenv',
      version=version,
      description="Expert Python Programming - Buildbot environment",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Tarek Ziadé',
      author_email='tarek@ziade.org',
      url='http://atomisator.ziade.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pbp'],
      include_package_data=True,
      zip_safe=False,
      # uncomment this to be able to run tests with setup.py
      #test_suite = "pbp.buildbotenv.tests.test_buildbotenvdocs.test_suite",
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Twisted',
          'buildbot'
      ],
    )

