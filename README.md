# eqt: Qt Elements

[![Tests](https://img.shields.io/github/actions/workflow/status/TomographicImaging/eqt/test.yml?branch=main&label=Tests&logo=GitHub)](https://github.com/TomographicImaging/eqt/actions?query=branch%3Amain) [![PyPI](https://img.shields.io/pypi/v/eqt.svg?logo=pypi&logoColor=white)](https://pypi.org/project/eqt) [![Conda](https://img.shields.io/conda/v/conda-forge/eqt.svg?label=conda-forge&logo=conda-forge)](https://anaconda.org/conda-forge/eqt)

Templates & tools to develop Qt GUIs in Python.

Some example classes are
1. `UIFormWidget`: a class to help creating Qt forms programmatically, useable in `QDockWidgets` and `QWidget`
2. `FormDialog`: a `QDialog` with a form inside with <kbd>OK</kbd> and <kbd>Cancel</kbd> buttons
3. `Worker`: a class that defines a `QRunnable` to handle worker thread setup, signals and wrap up

One use case is accepting a user input while running another task asynchronously (so that the UI is still responsive).

## Installation

Via `pip`/`conda`/`mamba`, i.e. any of the following:

- `python -m pip install eqt`
- `conda install -c conda-forge eqt`
- `mamba install -c conda-forge eqt`


#### Note:
`eqt` uses the [`qtpy`](https://github.com/spyder-ide/qtpy) abstraction layer for Qt bindings, meaning that it works with either PySide or PyQt bindings. Thus, the package does not depend on either. If the environment does not already have a Qt binding then the user *must* install either `pyside2` or `pyqt5`.

## Examples

See the [`examples`](examples) directory, e.g. how to launch a `QDialog` with a form inside using `eqt`'s [`QWidget`](examples/dialog_example.py) or [`FormDialog`](examples/dialog_example_2.py).

## Documentation
See [Documentation.md](./Documentation.md).

## Developer Contribution Guide
See [CONTRIBUTING.md](./CONTRIBUTING.md).
