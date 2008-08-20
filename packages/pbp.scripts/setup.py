from setuptools import setup, find_packages
import os

version = '0.2.2'

long_description = open("README.txt").read()
classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]

setup(name='pbp.scripts',
      version=version,
      description="Expert Python Programming - Contains scripts presented throughout the book",
      long_description=long_description,
      classifiers=classifiers,
      keywords='',
      author='Tarek Ziade',
      author_email='tarek@ziade.org',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pbp'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'guppy'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
