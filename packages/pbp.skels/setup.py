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
This module contains the tool of pbp.skels
"""
import os
from setuptools import setup, find_packages

version = '0.1.0'

README = os.path.join(os.path.dirname(__file__),
                      'pbp', 'skels', 'docs', 'README.txt')

long_description = open(README).read() + '\n\n'
tests_require = ['zope.testing',]

setup(name='pbp.skels',
      version=version,
      description="Skeletons for Python Best Practice bool",
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
      #test_suite = "pbp.skels.tests.test_skelsdocs.test_suite",
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'PasteScript',
          'Cheetah'
      ],
      entry_points="""
      # -*- Entry points: -*-
      [paste.paster_create_template]
      pbp_recipe_doc = pbp.skels.templates:Recipe
      pbp_design_doc = pbp.skels.templates:Design
      pbp_tutorial_doc = pbp.skels.templates:Tutorial
      pbp_module_doc = pbp.skels.templates:Module
      pbp_package = pbp.skels.templates:Package
      """,
      )

