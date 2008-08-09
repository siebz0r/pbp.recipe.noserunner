from setuptools import setup, find_packages
import os

version = '0.1.0'
long_description = open("README.txt").read()
classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]

entry_points = {"atomisator.filters": ["stopwords = atomisator.filters:StopWords",
                                       "buzzwords = atomisator.filters:BuzzWords"]}

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
          # -*- Extra requirements: -*-
      ],
      entry_points=entry_points,
      )
