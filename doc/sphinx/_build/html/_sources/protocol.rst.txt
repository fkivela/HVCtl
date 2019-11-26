RS-232 control protocol
=======================

Communication with the HV generator is based on command-answer pairs.
Both commands and answers consist of a string of ASCII characters ending with the carriage return character (ASCII character number 13).
Carriage return is displayed here as ``\r``, since that is the representation used by Python.

Command strings start with a letter denoting the given command, followed by one or more function parameters separated by commas.
Answers copy the command string, and may append a return value to its end (without a separating comma).

The RS-232 connection has the following specifications:

- 1 start bit
- 8 data bits
- 1 stop bit
- No parity bit
- Duplex mode: full
- Signal rate: 9600 baud

.. Note::
   If the HV generator doesn't receive any instructions for 5 seconds, it will automatically power off and enter local mode.

List of commands and answers
----------------------------

This section lists all commands recognized by the HV generator and the answers to them.
An *X* denotes a numerical value.
Unless otherwise signified, it is a 12-bit unsigned integer (i.e. :math:`X \in \left[0, 4095 \right]`),
linearly scaled to cover the entire voltage or current range of the generator. 
For example, with a SR 100 kV - 5 kW generator with negative polarity, ``X = 0`` sets the voltage to 0 V (i.e. the ground potential), and ``X = 4095`` sets it to -100 kV, which is the highest voltage the generator can produce.

1. Set output voltage
.....................

  :Command: ``d1,X\r``
  :Answer: ``d1,X\r``

2. Set output current
.....................

  :Command: ``d2,X\r``
  :Answer: ``d2,X\r``

3. Get output voltage
.....................

  :Command: ``a1\r``
  :Answer: ``a1X\r``

4. Get output current
.....................

  :Command: ``a2\r``
  :Answer: ``a2X\r``

5. Turn the HV on
.................

  This instruction requires sending two commands, with a 100 ms delay between receiving the answer to the first command and sending the second one.
  
  The first command-answer pair:

  :Command: ``P5,1\r``
  :Answer: ``P5,1\r``

  The second command-answer pair:
  
  :Command: ``P5,0\r``
  :Answer: ``P5,0\r``

6. Turn the HV off
..................

  This instruction requires sending two commands, with a 100 ms delay between receiving the answer to the first command and sending the second one.
  
  The first command-answer pair:

  :Command: ``P6,1\r``
  :Answer: ``P6,1\r``

  The second command-answer pair:

  :Command: ``P6,0\r``
  :Answer: ``P6,0\r``

7. Switch between local and remote mode
.......................................

  Switch to local mode:

    :Command:   ``P7,1\r``
    :Answer:    ``P7,1\r``

  Switch to remote mode:

    :Command:   ``P7,0\r``
    :Answer:    ``P7,0\r``

8. Activate or deactivate inhibition
....................................

  Activate inhibition:

    :Command: ``P8,1\r``
    :Answer:  ``P8,1\r``

  Deactivate inhibition:

    :Command:   ``P8,0\r`` 
    :Answer:    ``P8,0\r``

9. Get power supply status
..........................

  :Command: ``E\r``
  :Answer: ``EX\r``, :math:`X \in \left[0, 255 \right]`

  This command returns an 8-bit big-endian unsigned integer, with the bits being numbered in the following manner.
  MSB and LSB denote the most and least significant bits.
  
  +---------+---+---+---+---+---+---+---------+
  | 8 (MSB) | 7 | 6 | 5 | 4 | 3 | 2 | 1 (LSB) |
  +---------+---+---+---+---+---+---+---------+

  The values of bits 5-8 correspond to the values set by the commands 5-8.
  Bits 1-4 are status bits whose values don't directly correspond to a single command.
  The meanings of different bit values are presented in the table below. 

  +-----+-----------------------------------------+---------------------------------+
  | Bit | Value                                                                     |
  |     +-----------------------------------------+---------------------------------+
  |     | 1                                       | 0                               |
  +=====+=========================================+=================================+
  | 8   | Inhibition active                       | Inhibition idle                 |
  +-----+-----------------------------------------+---------------------------------+
  | 7   | Local mode                              | Remote mode                     |
  +-----+-----------------------------------------+---------------------------------+
  | 6   | First HV off command (``P6,1\r``) given |  First HV off command not given |
  +-----+----------------------------+------------+---------------------------------+
  | 5   | First HV on command (``P5,1\r``) given  | First HV on command not given   |
  +-----+-----------------------------------------+---------------------------------+
  | 4   | HV on                                   | HV off                          |
  +-----+-----------------------------------------+---------------------------------+
  | 3   | Interlock open                          | Interlock closed                |
  +-----+-----------------------------------------+---------------------------------+
  | 2   | Fault present                           | Fault not present               |
  +-----+-----------------------------------------+---------------------------------+
  | 1   | Voltage regulation                      | Current regulation              |
  +-----+-----------------------------------------+---------------------------------+

