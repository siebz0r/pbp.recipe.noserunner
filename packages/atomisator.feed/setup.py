from setuptools import setup, find_packages
import os

version = '0.2.6'

long_description = open("README.txt").read()
classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]

setup(name='atomisator.feed',
      version=version,
      description="Expert Python Programming - Feed generator",
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
          'Cheetah',
          'atomisator.db'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
