#!/usr/bin/env python3

from setuptools import setup
import os
try:
    from sphinx.setup_command import BuildDoc
    sphinx_available = False
    cmdclass = {'build_sphinx': BuildDoc}

except ImportError as ie:
    sphinx_available = False
    cmdclass = {}

import re

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open('eqt/__init__.py') as fd:
    version = re.search("__version__ = '(.*)'", fd.read()).group(1)

if 'CONDA_BUILD' in os.environ.keys():
    install_requires = []
else:
    install_requires = [
    
        'sphinx',
        'pyside2'

    ]

name = "eqt"

setup(name=name,
      version = version,
      description = 'A number of templates and tools to develop Qt GUIs with Python effectively',
      long_description = long_description,
      author = 'Edoardo Pasca',
      author_email = 'edoardo.pasca@stfc.ac.uk',
      url = '',
      packages = ['eqt', 'eqt.threading', 'eqt.ui'],
      license = 'Apache v2.0',
      install_requires=install_requires,
      classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
      ],
      command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'source_dir': ('setup.py', 'doc')}},
      )
