# eqt: Qt Elements

[![Tests](https://img.shields.io/github/actions/workflow/status/TomographicImaging/eqt/test.yml?branch=main&label=Tests&logo=GitHub)](https://github.com/TomographicImaging/eqt/actions?query=branch%3Amain) [![PyPI](https://img.shields.io/pypi/v/eqt.svg?logo=pypi&logoColor=white)](https://pypi.org/project/eqt) [![Conda](https://img.shields.io/conda/v/conda-forge/eqt.svg?label=conda-forge&logo=conda-forge)](https://anaconda.org/conda-forge/eqt)

Templates & tools to develop Qt GUIs in Python.

One use case is accepting user input while running another task asynchronously (so that the UI is still responsive).

1. `UIFormWidget`: a class to help creating Qt forms programmatically, useable in `QDockWidgets` and `QWidget`
2. `FormDialog`: a `QDialog` with a form inside with <kbd>OK</kbd> and <kbd>Cancel</kbd> buttons
3. `Worker`: a class that defines a `QRunnable` to handle worker thread setup, signals and wrap up

## Installation

Via `pip`/`conda`/`mamba`, i.e. any of the following:

- `python -m pip install eqt`
- `conda install -c conda-forge eqt`
- `mamba install -c conda-forge eqt`

## Examples

See the [`examples`](examples) directory, e.g. how to launch a `QDialog` with a form inside using `eqt`'s [`QWidget`](examples/dialog_example.py) or [`FormDialog`](examples/dialog_example_2.py).

### Running asynchronous tasks

To run a function in a separate thread we use a `Worker` which is a subclass of a `QRunnable`.

For the `Worker` to work one needs to define:

1. the function that does what you need
2. Optional callback methods to get the status of the thread by means of `QtCore.QSignal`s

On [initialisation](https://github.com/TomographicImaging/eqt/blob/535e487d09d928713d7d6aa1123657597627c4b0/eqt/threading/QtThreading.py#L32-L38) of the `Worker` the user needs to pass the function that has to run in the thread, i.e. `fn` below, and additional optional positional and keyword arguments, which will be passed on to the actual function that is run in the `QRunnable`.

```python
class Worker(QtCore.QRunnable):
    def __init__(self, fn, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
```

In practice the user will need to pass to the `Worker` as many parameters as there are listed in the [function](https://github.com/TomographicImaging/eqt/blob/535e487d09d928713d7d6aa1123657597627c4b0/eqt/threading/QtThreading.py#L56) to be run.

```python
result = self.fn(*self.args, **self.kwargs)
```

But `Worker` will [add](https://github.com/TomographicImaging/eqt/blob/535e487d09d928713d7d6aa1123657597627c4b0/eqt/threading/QtThreading.py#L41-L43) to the `**kwargs` the following `QSignal`.

```python
        # Add progress callback to kwargs
        self.kwargs['progress_callback'] = self.signals.progress
        self.kwargs['message_callback'] = self.signals.message
        self.kwargs['status_callback'] = self.signals.status
```

Therefore it is advisable to always have `**kwargs` in the function `fn` signature so that you can access the `QSignal` and emit the signal required. For instance one could emit a progress by:

```python
def fn(num_iter, **kwargs):
    progress_callback = kwargs.get('progress_callback', None)
    for i in range(num_iter):
        do_something
        if progress_callback is not None:
            progress_callback.emit( i )
```

### Passing a signal to a Worker

This is done just after one has defined the `Worker`:

```python
def handle_progress(num_iter):
    # do something with the progress
    print ("Current progress is ", num_iter)

worker = Worker(fn, 10)
worker.signals.progress.connect(handle_progress)
```

So, each time `fn` comes to `progress_callback.emit( i )` the function `handle_progress` will be called with the parameter `i` of its `for` loop.

### Signals available

The signals that are available in the `Worker` class are defined in [`WorkerSignal`](https://github.com/TomographicImaging/eqt/blob/535e487d09d928713d7d6aa1123657597627c4b0/eqt/threading/QtThreading.py#L66) and are the following. Below you can also see the type of data that each signal can emit.

```python
finished = QtCore.Signal()
error = QtCore.Signal(tuple)
result = QtCore.Signal(object)

progress = QtCore.Signal(int)
message = QtCore.Signal(str)
status = QtCore.Signal(tuple)
```

Read more on [Qt signals and slots](https://doc.qt.io/qt-5/signalsandslots.html) and on how to use them in [PySide2](https://wiki.qt.io/Qt_for_Python_Signals_and_Slots).

## Developer Contribution Guide
See [CONTRIBUTING.md](./CONTRIBUTING.md).
