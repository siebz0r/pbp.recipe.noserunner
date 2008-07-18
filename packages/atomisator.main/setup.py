from setuptools import setup, find_packages
import os

version = '0.2.0'
long_description = open("README.txt").read()
classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]

entry_points = {
    "console_scripts": [
        "load_feeds = atomisator.main:load_feeds",
        "generate_feed = atomisator.main:generate_feed",
        "atomisator = atomisator.main:atomisator"
    ]
}

setup(name='atomisator.main',
      version=version,
      description="Python Expert Programming - Main package for Atomisator app",
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
          'atomisator.db',
          'atomisator.feed',
          'atomisator.parser'
      ],
      tests_require=['nose'],
      test_suite='atomisator.main.tests.test_docs.test_suite',
      entry_points=entry_points
      )

