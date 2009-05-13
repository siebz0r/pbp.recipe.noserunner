# -*- coding: utf-8 -*-
"""
This module contains the tool of pbp.recipe.noserunner
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.2.6'

long_description = (
    read('README.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('pbp', 'recipe', 'noserunner', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

entry_point = 'pbp.recipe.noserunner:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}
tests_require=['nose', 'zc.buildout', 'zc.recipe.egg']

setup(name='pbp.recipe.noserunner',
      version=version,
      description="Expert Python Programming - ZC Buildout runner for nose",
      long_description=long_description,
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Zope Public License',
        ],
      keywords='',
      author='Tarek Ziade',
      author_email='tarek@ziade.org',
      url='http://atomisator.ziade.org',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pbp', 'pbp.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout',
                        'nose',
                        'zc.recipe.egg'
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'pbp.recipe.noserunner.tests.test_docs.test_suite',
      entry_points=entry_points,
      )
