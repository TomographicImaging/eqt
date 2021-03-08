#!/bin/bash

# install using pip from the whl file
# pip install https://files.pythonhosted.org/packages/98/7b/98fcb18998153977ed3cb41f9e231ae7a8ceaa1fbda74a4c8e642b69e676/qtelements-1.0.1-py3-none-any.whl

#$PYTHON -m pip install eqt --no-deps
cd $RECIPE_DIR/..
$PYTHON setup.py install
