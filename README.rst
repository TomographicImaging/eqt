Qt Elements qte
===============

A number of templates and tools to develop Qt GUI's with Python effectively.

Developing GUIs I often find myself creating forms to pass some input and also
running some task asynchronously so that the interface is still responsive.

This little package tries to address both recurring requirements.


1. ``UIFormWidget``, a class to help creating Qt forms 
  programmatically, useable in ``QDockWidgets`` and ``QWidget`` 
1. ``FormDialog``, a ``QDialog`` with a form inside with OK and Cancel button
1. ``Worker``, a class that defines a ``QRunnable`` to 
   handle worker thread setup, signals and wrap up

Installation
------------

You may install via ``pip`` or ``conda``

.. code-block:: bash
  
  python -m pip install qte 
  # or 
  conda install qte -c paskino

Example
-------

In the ``example`` directory there is an example on how to launch a 
``QDialog`` with a form inside using ``qte``'s 
 `QWidget <https://github.com/paskino/qt-elements/blob/main/examples/dialog_example.py>`_ or `FormDialog <https://github.com/paskino/qt-elements/blob/main/examples/dialog_example_2.py>`_.

