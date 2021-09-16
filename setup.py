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
    
def version2pep440(version):
    '''normalises the version from git describe to pep440
    
    https://www.python.org/dev/peps/pep-0440/#id29
    '''
    if version[0] == 'v':
        version = version[1:]

    if u'-' in version:
        v = version.split('-')
        v_pep440 = "{}.dev{}".format(v[0], v[1])
    else:
        v_pep440 = version

    return v_pep440


git_version_string = subprocess.check_output('git describe', shell=True).decode("utf-8")[1:]
    

#with open("README.rst", "r") as fh:
#    long_description = fh.read()
long_description = 'A number of templates and tools to develop Qt GUIs with Python effectively.'

if 'CONDA_BUILD' in os.environ.keys():
    # if it is a conda build requirements are going to be satisfied by conda
    install_requires = []
    version = git_version_string
else:
    install_requires = [
    
        'sphinx',
        'pyside2'

    ]
    version = version2pep440(git_version_string)
    
print ('version {}'.format(version))

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
