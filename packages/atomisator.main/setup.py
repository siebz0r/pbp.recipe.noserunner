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
        "atomisator = atomisator.main.run:atomisator"
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
          'atomisator.db>=0.2.4',
          'atomisator.feed>=0.2.5',
          # default plugins
          'atomisator.parser>=0.2.2',
          'atomisator.readers>=0.1.1',
          # default filters
          'atomisator.filters>=0.1.2',
          # default enhancers
          'atomisator.enhancers'
      ],
      tests_require=['nose'],
      test_suite='atomisator.main.tests.test_docs.test_suite',
      entry_points=entry_points
      )

