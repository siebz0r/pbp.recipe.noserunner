from setuptools import setup, find_packages
import os

version = '0.2.5'

long_description = open("README.txt").read()
classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]

setup(name='atomisator.db',
      version=version,
      description="Expert Python Programming - Manages the Atomisator storage.",
      long_description=long_description,
      classifiers=classifiers,
      keywords='atomisator',
      author='Tarek Ziade',
      author_email='tarek@ziade.org',
      url='http://atomisator.ziade.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['atomisator'],
      test_suite = 'nose.collector',
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'SQLAlchemy',
          'pysqlite'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
