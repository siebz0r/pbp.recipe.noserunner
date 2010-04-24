# -*- coding: utf-8 -*-
"""
This module contains the tool of pbp.recipe.trac
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.2.3'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('pbp', 'recipe', 'trac', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )
entry_point = 'pbp.recipe.trac:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

tests_require=['zope.testing', 'zc.buildout']

setup(name='pbp.recipe.trac',
      version=version,
      description="Expert Python Programming - ZC Buildout recipe that installs and configures a Trac server.",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='trac pbp',
      author='Tarek Ziade',
      author_email='tarek@ziade.org',
      url='http://atomisator.ziade.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pbp', 'pbp.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout',
                        'zc.recipe.egg',
                        'Trac >=0.11dev, ==0.11b1',
                        'TracMercurial',
                        'pysqlite',
                        'NavAdd',
                        'timingandestimationplugin'
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'pbp.recipe.trac.tests.test_docs.test_suite',
      entry_points=entry_points,
      dependency_links=['http://trac-hacks.org/svn/navaddplugin/0.9#egg=NavAdd',
                        'http://trac-hacks.org/svn/timingandestimationplugin/branches/trac0.11#egg=timingandestimationplugin',
                        'http://svn.edgewall.org/repos/trac/plugins/0.11/mercurial-plugin#egg=TracMercurial']
      )

