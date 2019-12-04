"""This module defines several constants based on the options defined
in a configuration file.
The default configuration file should be named ``'default.conf'`` and be
located in the same directory as this module.

Attributes:
    SERIAL_KWARGS
        A :class:`dict` of keyword arguments and values for creating a
        :class:`serial.Serial` object. The following keyword arguments
        and their values are included: *port*, *baudrate*, *bytesize*,
        *parity*, *stopbits*, *timeout*, *xonxoff*, *rtscts*, *dsrdtr*.
        The *exclusive* keyword will also be included and set to
        ``True``, if the version of the serial module is 3.3 or
        later. See the documentation of :class:`serial.Serial` for
        further details.

    VOLTAGE_LIMIT
        The maximum voltage for a particular application in V.
        HVCtl will never set the voltage to a value exceeding this.

    CURRENT_LIMIT
        The maximum current for a particular application in mA.
        HVCtl will never set the current to a value exceeding this.

    INT_MAX
        The serial protocol uses 12-bit unsigned integers for the
        values of voltage and current.
        This is the maximum value of that integer, ``4095``.

    DELTA_U
        The smallest amount by which the value of the voltage can be
        changed, in V. This is computed by dividing the maximum voltage
        produced by the generator with :const:`INT_MAX`.

    DELTA_I
        The smallest amount by which the value of the current can be
        changed, in mA. This is computed analogously to 
        :const:`DELTA_U`.
"""

import configparser
import os
from typing import Union

import serial

# Defining the constants at the module level helps automatic tools
# such as IDEs and Pylint. 
SERIAL_KWARGS = None
VOLTAGE_LIMIT = None
CURRENT_LIMIT = None
INT_MAX = None
DELTA_U = None
DELTA_I = None


def load(filename=None):
    """Parse the configuration file and define the constants.
    
    This function is called automatically with the default argument
    when the module is imported. If a different configuration file
    should be used, the constants should be reloaded by calling this
    function manually with the correct argument.
    
    Args:
        filename:
            The path to the configuration file.
            If this isn't defined, the file ``'default.conf'``
            (located in the same directory as this module)
            is used.

    Raises:
        FileNotFoundError: If the configuration file cannot be found.
        RuntimeError: If the configuration file is found but cannot be
            parsed.
    """    
    if not filename:
        configfile = 'default.conf'
        dirpath = os.path.dirname(__file__)
        path = os.path.join(dirpath, configfile)
    else:
        path = filename

    parser = configparser.ConfigParser()
    # read_file is used instead of read, because read doesn't raise
    # an error if the file is not found.
    with open(path) as file:
        parser.read_file(file)

    try:
        _load_values(parser)
    except ValueError as error:
        raise RuntimeError(f"couldn't parse configurations") from error


def _load_values(parser):
    """Define module-wide constants."""

    global SERIAL_KWARGS
    global VOLTAGE_LIMIT
    global CURRENT_LIMIT
    global INT_MAX
    global DELTA_U
    global DELTA_I

    # pylint: disable=bad-whitespace
    SERIAL_KWARGS = {
        'port'    :           parser.get(       'serial', 'port'    ),
        'baudrate':           parser.getint(    'serial', 'baudrate'),
        'bytesize': _bytesize(parser.getint(    'serial', 'bytesize')),
        'parity'  :   _parity(parser.get(       'serial', 'parity'  )),
        'stopbits': _stopbits(parser.getint(    'serial', 'stopbits')),
        'timeout' :  _timeout(parser.get(       'serial', 'timeout' )),
        'xonxoff' :           parser.getboolean('serial', 'xonxoff' ),
        'rtscts'  :           parser.getboolean('serial', 'rtscts'  ),
        'dsrdtr'  :           parser.getboolean('serial', 'dsrdtr'  ),
    }
    # pylint: enable=bad-whitespace

    # The exclusive keyword isn't found in older versions of the
    # serial module.
    if float(serial.VERSION) >= 3.3:
        SERIAL_KWARGS['exclusive'] = True

    max_voltage = parser.getfloat('voltage', 'max_voltage')
    max_current = parser.getfloat('current', 'max_current')
    VOLTAGE_LIMIT = parser.getfloat('voltage', 'voltage_limit')
    CURRENT_LIMIT = parser.getfloat('current', 'current_limit')

    INT_MAX = 2**12 - 1
    DELTA_U = max_voltage / INT_MAX
    DELTA_I = max_current / INT_MAX


def _parity(letter: str):
    """Parse a string into a parity constant used by the serial
    module.
    """
    try:
        return {'N': serial.PARITY_NONE,
                'E': serial.PARITY_EVEN,
                'O': serial.PARITY_ODD,
                'S': serial.PARITY_SPACE,
                'M': serial.PARITY_MARK}[letter]
    except KeyError:
        raise ValueError(f'invalid parity: {letter}')


def _stopbits(bits: Union[int, float]):
    """Parse a string into a stop bits constant used by the serial
    module.
    """
    try:
        return {1  : serial.STOPBITS_ONE,
                1.5: serial.STOPBITS_ONE_POINT_FIVE,
                2  : serial.STOPBITS_TWO}[bits]
    except KeyError:
        raise ValueError(f'invalid stopbits: {bits}')


def _bytesize(size: int):
    """Parse a string into a byte size constant used by the serial
    module.
    """
    try:
        return {5: serial.FIVEBITS,
                6: serial.SIXBITS,
                7: serial.SEVENBITS,
                8: serial.EIGHTBITS}[size]
    except KeyError:
        raise ValueError(f'invalid bytesize: {size}')


def _timeout(value: str):
    """Parse a string into a numeric timeout value or None."""
    if value.upper() == 'NONE':
        return None
    try:
        return float(value)
    except ValueError:
        raise ValueError('invalid timeout: {value}')


load()
