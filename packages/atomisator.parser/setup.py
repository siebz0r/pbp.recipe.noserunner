from setuptools import setup, find_packages
import os

version = '0.1.0'
long_description = open("README.txt").read()
classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]

setup(name='atomisator.parser',
      version=version,
      description="A thin layer on the top of the Universal Feed Parser",
      long_description=long_description,
      classifiers=classifiers,
      keywords='python best practices',
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
          'feedparser'
          # -*- Extra requirements: -*-
      ],
      tests_require=['feedparser',],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
