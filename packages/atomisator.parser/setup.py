from setuptools import setup, find_packages
import os

version = '0.2.1'
long_description = open("README.txt").read()
classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]

entry_point = 'atomisator.parser:Parser'
entry_points = {"atomisator.plugins": ["rss = %s" % entry_point]}

setup(name='atomisator.parser',
      version=version,
      description="Expert Python Programming - A thin layer on the top of the Universal Feed Parser",
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
          'feedparser'
          # -*- Extra requirements: -*-
      ],
      tests_require=['feedparser',],
      entry_points=entry_points,
      )
