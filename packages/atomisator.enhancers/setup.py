from setuptools import setup, find_packages
import os

version = '0.1.0'

long_description = open("README.txt").read()

classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]

entry_points = {"atomisator.enhancers": 
                    ["digg = atomisator.enhancers:DiggComments",
                     "related = atomisator.enhancers:RelatedEntries"]}

setup(name='atomisator.enhancers',
      version=version,
      description="Expert Python Programming - Enhancers",
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

