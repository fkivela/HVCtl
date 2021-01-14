RS-232 control protocol
=======================

Communication with the HV generator is based on command-answer pairs.
Both commands and answers consist of a string of ASCII characters ending with
the carriage return character (ASCII character number 13).
Carriage return is displayed here as ``\r``, since that is the representation
used by Python.

Command strings start with a letter denoting the given command, followed by one
or more function parameters separated by commas.
Answers copy the command string, and may append a return value to its end
(without a separating comma).

The RS-232 connection has the following specifications:

- 1 start bit
- 8 data bits
- 1 stop bit
- No parity bit
- Duplex mode: full
- Signal rate: 9600 baud

.. Note::
   If the HV generator doesn't receive any instructions for 5 seconds, it will
   automatically turn the HV `off <hv-off_>`_ and enter `local mode <mode_>`_.


List of commands and answers
----------------------------

This section lists all commands recognized by the HV generator and the answers
to them.
An *X* denotes a numerical value.
Unless otherwise signified, it is a 12-bit unsigned integer
(i.e. :math:`X \in \left[0, 4095 \right]`),
linearly scaled to cover the entire voltage or current range of the generator. 
For example, with a SR100KV-5KW generator with negative polarity, ``X = 0``
sets the voltage to 0 V (i.e. the ground potential), and ``X = 4095`` sets it
to -100 kV, which is the highest (by absolute value) voltage the generator can
produce.


.. _set-voltage:

1. Set output voltage
.....................

:Command: ``d1,X\r``
:Answer: ``d1,X\r``

This command sets the voltage produced by the HV generator to the given value.
If the command is sent while the generator is currently in the
`HV off <hv-off_>`_ state or inhibition_ has been activated,
the new value will be applied when the pump is switched to a HV on/inhibition
off state.


.. _set-current:

2. Set output current
.....................

:Command: ``d2,X\r``
:Answer: ``d2,X\r``

This command works just like `the previous one <set-voltage_>`_, but sets the
output current instead of the output voltage. 


.. _get-voltage:

3. Get output voltage
.....................

:Command: ``a1\r``
:Answer: ``a1X\r``

This command returns the voltage produced by the HV generator.
If the generator is in the `HV off <hv-off_>`_ state or inhibition_ has been
activated, the returned value will be zero.


.. _get-current:

4. Get output current
.....................

:Command: ``a2\r``
:Answer: ``a2X\r``

This command works just like `the previous one <get-voltage_>`_, but returns
the output current instead of the output voltage.


.. _hv-on:

5. Turn the HV on
.................

:Command: ``P5,1\r``
:Answer: ``P5,1\r``

**Wait 100 ms.**

:Command: ``P5,0\r``
:Answer: ``P5,0\r``

This command is used to switch the generator to the HV on state. 
The command is actually a sequence of two different commands,
which are sent with a 100 ms delay between receiving the answer to the first
command and sending the second one.

The HV generator has two states: HV on and HV off.
In the HV off state the generator doesn't produce any output (i.e. the voltage
and the current are 0), while in the HV on state output is produced normally.

Note that the HV on and HV off states are a different thing than the HV
generator itself being on or off; the generator is powered on and can respond
to commands in both the HV on and the HV off state. 


.. _hv-off:

6. Turn the HV off
..................

:Command: ``P6,1\r``
:Answer: ``P6,1\r``

**Wait 100 ms.**

:Command: ``P6,0\r``
:Answer: ``P6,0\r``

This command works just like `the previous one <hv-on_>`_, but switches the HV
generator to the HV off state instead of the HV on state.


.. _mode:

7. Switch between local and remote mode
.......................................

Switch to local mode:

:Command:   ``P7,1\r``
:Answer:    ``P7,1\r``

Switch to remote mode:

:Command:   ``P7,0\r``
:Answer:    ``P7,0\r``

This command switches the HV generator to the local mode or the remote mode.

The HV generator can be operated in two modes: local and remote.
In the remote mode, the generator is controlled through a remote connection,
such as the RS-232 connection described here,
while in the local mode it is controlled through the buttons located on its
front panel.

In the local mode, the `HV on <hv-on_>`_ command cannot be sent remotely,
and switching the generator to the local mode in the HV on state will
automatically set it to the HV off state.
However, the command to switch to remote mode and the
`inhibition <inhibition_>`_ command can be sent remotely even in the local
mode. 


.. _inhibition:

8. Activate or deactivate inhibition
....................................

This command is used to activate or deactivate output inhibition.
While inhibition is activated, the HV generator doesn't produce output even in
the `HV on <hv-on_>`_ state.

Activate inhibition:

:Command: ``P8,1\r``
:Answer:  ``P8,1\r``

Deactivate inhibition:

:Command:   ``P8,0\r`` 
:Answer:    ``P8,0\r``


.. _status:

9. Get generator status
.......................

:Command: ``E\r``
:Answer: ``EX\r``, :math:`X \in \left[0, 255 \right]`

This command returns the status of the HV generator, excluding the values of
the voltage and the current.
The returned value is the decimal representation of an 8-bit unsigned integer,
where each bit signifies a single status condition.

The bits are numbered in the following manner,
with MSB and LSB denoting the most and least significant bits.
Bits 5-8 directly correspond to the parameter values (1 or 0) of commands 5-8.

+---------+---+---+---+---+---+---+---------+
| 8 (MSB) | 7 | 6 | 5 | 4 | 3 | 2 | 1 (LSB) |
+---------+---+---+---+---+---+---+---------+

The meanings of the bits are explained below.

+-----+-----------------------------------------+---------------------------------+
| Bit | Value                                                                     |
|     +-----------------------------------------+---------------------------------+
|     | 1                                       | 0                               |
+=====+=========================================+=================================+
| 8   | Inhibition active                       | Inhibition not active           |
+-----+-----------------------------------------+---------------------------------+
| 7   | Local mode                              | Remote mode                     |
+-----+-----------------------------------------+---------------------------------+
| 6   | First HV off command (``P6,1\r``) given | First HV off command not given  |
+-----+----------------------------+------------+---------------------------------+
| 5   | First HV on command (``P5,1\r``) given  | First HV on command not given   |
+-----+-----------------------------------------+---------------------------------+
| 4   | HV on                                   | HV off                          |
+-----+-----------------------------------------+---------------------------------+
| 3   | Interlock open                          | Interlock closed                |
+-----+-----------------------------------------+---------------------------------+
| 2   | Fault                                   | No fault                        |
+-----+-----------------------------------------+---------------------------------+
| 1   | Voltage regulation                      | Current regulation              |
+-----+-----------------------------------------+---------------------------------+


Bit 8: inhibition
*****************
This bit tells whether `inhibition`_ is active or not.


Bit 7: mode
***********
This bit tells whether the HV generator is in `local or remote <mode_>`_ mode.


Bit 6: HV off
*************
The value of this bit is 1 if the first `HV off <hv-off_>`_ command has been
sent and the second one hasn't.


Bit 5: HV on
************
The value of this bit is 1 if the first `HV on <hv-on_>`_ command has been sent
and the second one hasn't.


Bit 4: HV status
****************
This bit tells whether the HV generator is in the `HV on <hv-on_>`_ state or
the `HV off <hv-off_>`_ state.


.. _interlock:

Bit 3: interlock  
****************
This bit tells whether the interlock is closed or open.

The interlock is a physical safety device consisting of two pins on the rear
panel of the HV generator.
In some generator models the interlock is a Lemo-type 2-pin connector; in
others, pins 16 and 24 of a 25-pin D-subminiature remote connector serve as the
interlock.
In both cases, the interlock must be closed by connecting the two pins to one
another for the generator to produce output.
Opening the interlock will switch the generator to the `HV off <hv-off_>`_
state and activate the fault_ state.

.. _fault:

Bit 2: fault
************
This bit tells whether the fault state is active or not.

The fault state is activated whenever some error condition happens.
This turns the HV `off <hv-off_>`_ and prevents it from being turned back
`on <hv-on_>`_.
The fault state can be activated e.g. if the interlock is opened, the key lock
is turned on before powering on the generator, or if there is a  hardware
problem inside the generator.
After the cause of the error condition is removed, the fault state can be reset
by pressing the HV off button on the front panel of the generator.


Bit 1: regulation
*****************
This bit tells whether the generator is currently regulating voltage or
current.

The `set voltage <set-voltage_>`_ command activates the voltage regulation
mode, where the generator sets its output voltage to the desired value and
keeps it there.
The output current is then determined by the output voltage and the resistance
of the circuit the generator is connected to.

Conversely, the `set current <set-current_>`_ command sets the current to the
desired value and the voltage to whatever value is needed to generate that
current; this is the current regulation mode.
