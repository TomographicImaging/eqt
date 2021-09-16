#!/usr/bin/env python3

from setuptools import setup
import os
import subprocess

try:
    from sphinx.setup_command import BuildDoc
    sphinx_available = False
    cmdclass = {'build_sphinx': BuildDoc}

except ImportError as ie:
    sphinx_available = False
    cmdclass = {}

#with open("README.rst", "r") as fh:
#    long_description = fh.read()
long_description = 'A number of templates and tools to develop Qt GUIs with Python effectively.'
    
cmd = 'git describe'
dversion = subprocess.check_output(cmd, shell=True).strip().decode('utf-8')[1:]

print ('version {}'.format(dversion))

if 'CONDA_BUILD' in os.environ.keys():
    install_requires = []
else:
    install_requires = [
    
        'sphinx',
        'pyside2'

    ]

name = "eqt"

setup(name=name,
      version = dversion,
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
            'version': ('setup.py', dversion),
            'source_dir': ('setup.py', 'doc')}},
      )
