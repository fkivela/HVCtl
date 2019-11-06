Usage
=====

HVCtl may be launched in an interactive mode by running the script ``hvctl-run``. 
``hvctl-run`` accepts the following command-line arguments:

-s, --simple	Run HVCtl with a simple command-line interface. 
				Running this UI doesn't require installing :doc:`urwid <installation>`.
				If HVCtl is run without the -s argument, a slighlty more advanced UI will be used (see below for  an example).
-v, --virtual 	Run HVCtl with a virtual HV PSU. 
				If this argument is included, instead of sending messages to a real HV PSU, HVCtl creates a simulated virtual one and sends messages to it. 
				This makes it possible to test HVCtl easily without having to connect to a physical HV device.

HVCtl also includes a scripting possibility. The HV PSU may be controlled programmatically by creating an instance of the :class:`hvctl.api.API` class and accessing its methods (see :mod:`hvctl.api` for details).

Configuration settings for HVCtl, such as the port used for the serial connection, are located and documented in the file ``hv.conf``.

Examples
--------

The following examples demonstrate voltage can be read and set using each of the user interfaces provided by HVCtl.

In the first example, HVCtl is run in an interactive mode with the -s argument.

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

In the second example, no -s argument is given, and HVCtl uses a more advanced UI. The bottom of the UI is an interactive command-line interface identical to the one above, but the top part contains a screen showing the current status of the HV PSU. The command-line interface can be scrolled using the mouse wheel, clicking the scroll bar next to the command-line interface, or clicking the arrow buttons above and below the scroll bar.

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

The last example demonstrates using HVCtl programmatically with an :class:`~hvctl.api.API` object. The last call to :meth:`~hvctl.api.API.halt()` closes the serial connection and the parallel thread that is used to poll the HV PSU to keep it from switching to local mode.

>>> import hvctl.api
>>> api = hvctl.api.API()
>>> api.get_voltage()
-0.0
>>> api.set_voltage(-5000)
-5006.1050061050055
>>> api.get_voltage()
-5006.1050061050055
>>> api.halt()
