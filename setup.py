#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from setuptools import setup, find_packages
import os

# Parse the version from the main __init__.py
with open('gadm/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue


extra_reqs = {'docs': ['sphinx',
                       'furo']}

with codecs.open('README.rst', encoding='utf-8') as f:
    readme = f.read()

setup(name='gadm',
      version=version,
      description=u"Helpers for accessing and loading data from the Database of Global Administrative Areas (GADM)",
      long_description=readme,
      keywords='Geojson, administrative areas, public data',
      author=u"Loic Dutrieux",
      author_email='loic.dutrieux@gmail.com',
      url='https://github.com/loicdtx/pygadm',
      license='GPLv3',
      classifiers=[
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      packages=find_packages(),
      install_requires=[
          'fiona',
          'requests'
      ],
      extras_require=extra_reqs)

