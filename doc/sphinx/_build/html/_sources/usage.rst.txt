Usage
=====

Interactive mode
----------------

HVCtl may be launched in an interactive mode by running the ``__main__.py`` script inside the ``hvctl`` package.
This is done with the command

::

	$ python path/to/hvctl -args
	
Because this command requires providing the relative or absolute path to the ``hvctl`` package every time it is used, 
HVCtl also provides a shell script which automatically fills in the path before calling the command.
If the ``HVCtl`` directory is added to ``$PATH``, the shell script can be run from any directory with

::

	$ hvctl-run -args 

Both of these commands accept the following command-line arguments:

-s, --simple	Run HVCtl with a simple command-line interface that doesn't require :doc:`urwid <installation>` to work.
				If HVCtl is run without the ``-s`` argument, a slightly more advanced UI will be used (see below for  an example).
-v, --virtual 	Run HVCtl with a virtual HV generator. 
				If this argument is included, instead of sending messages to a real HV generator, HVCtl creates a simulated, virtual one and sends messages to that. 
				This makes it possible to test HVCtl easily without having to connect to an actual HV generator.

Importing
---------

HVCtl also includes an importable API for controlling the HV generator programmatically. 
The API is used by creating an instance of the :class:`~hvctl.api.API` class and calling its methods, 
and the :class:`~hvctl.virtualhv.VirtualHV` class allows it to be tested without access to a physical HV generator.
These two classes are members of the ``hvctl`` namespace as well as the namespaces of their own modules, 
so they can be imported with 

>>> from hvctl import API, VirtualHV

as well as

>>> from hvctl.api import API
>>> from hvctl.virtualhv import VirtualHV

All importable modules in the ``hvctl`` package are listed in the :doc:`Modules <modules/index>` page. 

Configuration
-------------

Configuration settings for HVCtl, such as the port used for the serial connection, are defined and documented in the file ``hv.conf``, located in the ``HVCtl/hvctl`` directory.

Examples
--------

The following examples demonstrate reading and setting the voltage by using the different interfaces provided by HVCtl.

Interactive mode with ``-s``
............................

HVCtl is run in interactive mode with the ``-s`` argument, resulting in a simple command-line ui.
The UI imports the :mod:`readline` module, which enables command editing and browsing command history with the up and down arrows.

::

	$ hvctl-run -s
	Welcome to HVCtl! Type 'help' for a list of commands.
	>> hvon
	HV turned on
	>> getvoltage
	The voltage is 0.0 V
	>> setvoltage 5000
	Voltage set to 5006.1050061050055 V
	>> getvoltage
	The voltage is 5006.1050061050055 V
	>> exit

Interactive mode without ``-s``
...............................

Here the ``-s`` argument hasn't been given, and HVCtl uses a more advanced UI. 
The bottom of the UI is an interactive command-line interface similar to the one above, but the top part contains a screen showing the current status of the HV generator. 
The command-line interface can be scrolled using the mouse wheel, clicking the scroll bar next to the command-line interface, or clicking the arrow buttons above and below the scroll bar.

::

	Voltage: 5006.11 V
	Current: 0.00 mA
	Regulation mode: voltage

	HV power: on
	HV on command given: False
	HV off command given: False

	Mode: remote
	Interlock: open
	No faults present
	─────────────────────────────────────────────────────────
	Welcome to HVCtl! Type 'help' for a list of commands.  ▲
	>> hvon                                                ██
	HV turned on                                           ██
	>> getvoltage                                          ██
	The voltage is 0.0 V                                   ██
	>> setvoltage 5000                                     ██
	Voltage set to 5006.1050061050055 V                    ██
	>> getvoltage                                          ██
	The voltage is 5006.1050061050055 V                    ██
	>> exit                                                ██
	PRESS 'q' TO EXIT                                      ██
	                                                       ▼

Using the API
.............

This example demonstrates using HVCtl in an interactive Python interpreter with an :class:`~hvctl.api.API` object. 
The last call to :meth:`~hvctl.api.API.halt()` closes the serial connection and the parallel thread that is used to poll the HV generator to keep it from switching to local mode.

>>> import hvctl
>>> api = hvctl.API()
>>> api.get_voltage()
-0.0
>>> api.set_voltage(-5000)
-5006.1050061050055
>>> api.get_voltage()
-5006.1050061050055
>>> api.halt()

Using the API with a virtual HV generator
.........................................

This is an example of a Python script that uses a virtual HV generator.
The script uses ``with`` blocks to ensure that both the :class:`~hvctl.api.API` and the :class:`~hvctl.virtualhv.VirtualHV` are closed properly at the end.

::

	from hvctl import API, VirtualHV

	with VirtualHV as vhv:
		with API(port=vhv.connection.port) as api:
			api.set_voltage(-5000)
			# More code here...
