from setuptools import setup, find_packages
import os

version = '0.1.0'
long_description = open("README.txt").read()
classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],

setup(name='atomisator.db',
      version=version,
      description="Manages the Atomisator storage.",
      long_description=long_description,
      classifiers=classifiers,
      keywords='atomisator',
      author='Tarek Ziade',
      author_email='tarek@ziade.org',
      url='http://hg.programmation-python.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['atomisator'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'SQLAlchemy'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
