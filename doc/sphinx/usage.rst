Usage
=====

Interactive mode
----------------

HVCtl may be launched in an interactive mode with the command ``python hvctl -args`` or ``hvctl-run -args``. 
Both commands run the same script; the latter is simply a shortcut to make the command slightly shorter.
The commands accept the following command-line arguments:

-s, --simple	Run HVCtl with a simple command-line interface. 
				Running this UI doesn't require installing :doc:`urwid <installation>`.
				If HVCtl is run without the -s argument, a slighlty more advanced UI will be used (see below for  an example).
-v, --virtual 	Run HVCtl with a virtual HV PSU. 
				If this argument is included, instead of sending messages to a real HV PSU, HVCtl creates a simulated virtual one and sends messages to it. 
				This makes it possible to test HVCtl easily without having to connect to a physical HV device.

Importing
---------

HVCtl also includes an importable API for controlling the HV PSU programmatically. 
This can be accessed by creating an instance of the :class:`hvctl.api.API` class and accessing its methods (see :mod:`hvctl.api` for details).
The :class:`hvctl.virtualhv.VirtualHV` class can be used to test the API without access to a physical HV PSU.

The :doc:`Modules <modules/index>` page lists all importable Python modules included in HVCtl.
These modules are all located in the ``hvctl`` package, and can be imported with any of the following syntaxes, 
as long as the ``HVCtl`` directory is your working directory or in your ``PYTHONPATH``. 

>>> import hvctl
>>> api = hvctl.api.API()

>>> import hvctl.api
>>> api = hvctl.api.API()

>>> from hvctl import api
>>> apiobj = api.API() # The name 'api' is already taken

>>> from hvctl.api import API
>>> api = API()

Configuration settings for HVCtl, such as the port used for the serial connection, are located and documented in the file ``hv.conf``.

Examples
--------

The following examples demonstrate reading and setting the voltage by using the different interfaces provided by HVCtl.

Interactive mode with -s
........................

HVCtl is run in interactive mode with the -s argument, resulting in a simple command-line ui.

::

	$ hvctl-run -s
	Welcome to HVCtl! Type 'help' for a list of commands.
	>> getvoltage
	The voltage is -0.0 V
	>> setvoltage -5000        
	Voltage set to -5006.1050061050055 V
	>> getvoltage
	The voltage is -5006.1050061050055 V
	>> exit

Interactive mode without -s
...........................

Here the -s argument hasn't been given, and HVCtl uses a more advanced UI. 
The bottom of the UI is an interactive command-line interface identical to the one above, but the top part contains a screen showing the current status of the HV PSU. 
The command-line interface can be scrolled using the mouse wheel, clicking the scroll bar next to the command-line interface, or clicking the arrow buttons above and below the scroll bar.

::

	Voltage: -0.00 V
	Current: 0.00 mA
	Regulation mode: voltage

	HV power: off
	HV on command given: False
	HV off command given: False

	Mode: remote
	Interlock: closed
	No faults present
	─────────────────────────────────────────────────────────
	Welcome to HVCtl! Type 'help' for a list of commands.  ▲
	>> getvoltage                                          ██
	The voltage is -0.0 V                                  ██
	>> setvoltage -500                                     ██
	Voltage set to -488.40048840048837 V                   ██
	>> getvoltage                                          ██
	The voltage is -488.40048840048837 V                   ██
	>> exit                                                ██
	PRESS 'q' TO EXIT                                      ▼

Using the API
.............

This example demonstrates using HVCtl in an interactive Python interpreter with an :class:`~hvctl.api.API` object. 
The last call to :meth:`~hvctl.api.API.halt()` closes the serial connection and the parallel thread that is used to poll the HV PSU to keep it from switching to local mode.

>>> import hvctl.api
>>> api = hvctl.api.API()
>>> api.get_voltage()
-0.0
>>> api.set_voltage(-5000)
-5006.1050061050055
>>> api.get_voltage()
-5006.1050061050055
>>> api.halt()

Using the API with a virtual HV PSU
...................................

This is an example of a Python script that uses a virtual HV PSU.
The script uses ``with`` blocks to ensure that both the :class:`~hvctl.api.API` and the :class:`~hvctl.virtualhv.VirtualHV` are closed properly at the end.

::

	from hvctl import api, virtualhv

	with virtualhv.VirtualHV as vhv:
		with api.API(port=vhv.connection.port):
			api.set_voltage(-5000)
			# More code here...
