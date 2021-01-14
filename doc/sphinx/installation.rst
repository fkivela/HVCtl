Installation
============

.. _dependencies:

Dependencies
------------

HVCtl was written and tested in Python 3.8.5, but it may also work with some
older versions, such as Python 3.7.
It is intended to be used on a Linux operating system, and probably won't work
on other systems such as Windows without some tweaks. 

In addition to the Python standard library, HVCtl uses pySerial_ (tested with
version 3.5) and Urwid_ (tested with version 2.1.2).
pySerial must be installed for HVCtl to work, but HVCtl can run without Urwid
by using an alternative user interface (see :doc:`usage` for details).


The HVCtl directory
-------------------

HVCtl doesn't include an installation script; simply download the ``HVCtl``
directory to a location of your choosing.
In order to access the ``hvctl`` package and the ``hvctl-run`` script, the
``HVCtl`` directory  should be added to ``$PYTHONPATH`` and ``$PATH`` or made
the working directory.

.. _pySerial: https://pypi.org/project/pyserial/
.. _Urwid: http://urwid.org/
