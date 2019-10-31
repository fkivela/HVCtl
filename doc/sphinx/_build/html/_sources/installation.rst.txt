Installation
============

HVCtl was written and tested in Python 3.7.3, so that or another relatively new Python version should be installed.

.. _urwid-installation:

In addition to the Python standard library, HVCtl uses pySerial_ (tested with version 3.4) and urwid_ (tested with version 2.0.1). pySerial must be installed for HVCtl to work, but HVCtl can run without urwid by using a simpler user interface (see :doc:`usage` for details).

After these dependencies are met, HVCtl doesn't require any special installation steps; simply downloading the ``HVCtl`` directory with its contents is sufficient.

In order to access the modules included in the program, the directory ``HVCtl/hvctl/`` should be added to ``$PATH`` or made the working directory.

.. _pySerial: https://pypi.org/project/pyserial/
.. _urwid: http://urwid.org/
