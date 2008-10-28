from setuptools import setup, find_packages
import os

long_description = open("README.txt").read()
classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]

setup(name='Atomisator',
      version='1.0',
      description="Data processing framework",
      long_description=long_description,
      classifiers=classifiers,
      keywords='data mining',
      author='Tarek Ziade',
      author_email='tarek@ziade.org',
      url='http://atomisator.ziade.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'atomisator.main>=0.5.1',
      ]
      )

