from setuptools import setup, find_packages
import os

from atomisator.main import __version__ as VERSION

long_description = open("README.txt").read()
classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]

entry_points = {
    "console_scripts": [
        "atomisator = atomisator.main.commands:atomisator"
    ]
}

setup(name='atomisator.main',
      version=VERSION,
      description="Expert Python Programming - Main package for Atomisator app",
      long_description=long_description,
      classifiers=classifiers,
      keywords='',
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
          'multiprocessing',
          'atomisator.db>=0.3.1',
          'atomisator.feed>=0.3.2',
          # default plugins
          'atomisator.parser>=0.2.4',
          'atomisator.readers>=0.1.1',
          # default filters
          'atomisator.filters>=0.1.9',
          # default enhancers
          'atomisator.enhancers>=0.1.1',
          # default outputs
          'atomisator.outputs'
      ],
      tests_require=['nose'],
      test_suite='atomisator.main.tests.test_docs.test_suite',
      entry_points=entry_points
      )

