"""This module defines a set of methods for controlling the HV
generator.
"""
import time
import threading
from dataclasses import dataclass
from typing import Callable

import serial

from . import config
from .message import Message


class API():
    """This class defines an API for communicating with a
    Technix SR100KV-5KW high voltage generator.

    Creating an instance of this class forms a serial connection to
    the generator, after which messages can be sent to it by calling
    the methods of the instance.

    If the serial connection is lost, all methods of this class that
    communicate with the generator will raise a
    :class:`serial.SerialException`.

    If an API is initialized with ``poll=True``, it will automatically
    call :meth:`full_status` every :attr:`timestep` seconds.
    This updates the data in :attr:`status` and prevents the generator
    from switching to local mode, which it normally does after not
    receiving a command for 5 seconds.

    The polling routine is run in a parallel thread, and should be
    closed after the API is no lenger needed.
    This can be done by calling :meth:`halt` or running the API in a
    ``with`` block. Both of these closing methods also close the
    serial connection.

    Attributes:
        status (Status):
            An object storing the current status of the generator.
            Its attributes are updated every time the generator sends
            back a reply.

        timestep (int or float):
            If *self* was initialized with ``poll=True``, this
            determines the time (in seconds) between polling messages.
            The default value is ``1``.
    """

    def __init__(self, port=None, poll=True):
        """Create a new instance of this class and form a serial
        connection to the HV generator.

        Args:
            port (str):
                The serial port device name. If a value is not given,
                it will be set to :const:`SERIAL_KWARGS['port']
                <hvctl.config.SERIAL_KWARGS>`.

            poll (bool):
                Determines whether automatic polling should be used
                or not (see the class docstring for more details.)

        Raises:
            RuntimeError:
                If a serial connection cannot be formed.
        """
        self.status = Status()
        self.timestep = 1

        if not port:
            port = config.SERIAL_KWARGS['port']

        serkwargs = {
            k: v for k, v in config.SERIAL_KWARGS.items() if k != 'port'}

        # This may raise a serial.SerialException.
        self._connection = serial.Serial(port=port, **serkwargs)

        self._stop_flag = threading.Event()
        # *lock* prevents messages from being sent at the same time by
        # _run_poll and the user.
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._run_poll, daemon=True)
        # _thread and _lock are created even with poll=False,
        # since they are referenced by methods.

        if poll:
            self._thread.start()

    def __enter__(self):
        """Called upon entering a ``with`` block; returns *self*."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Called upon exiting a ``with`` block; calls :meth:`halt`."""
        self.halt()

    def set_voltage(self, value):
        """Set the voltage to *value* (in V).

        The sign of *value* doesn't matter, since it is automatically
        changed to match the polarity of the HV generator.

        Returns:
            The voltage value sent back by the HV generator.
            This is always non-negative regardless of the polarity
            of the generator.
        """
        return self._set(
            'voltage', value, config.DELTA_U, config.VOLTAGE_LIMIT)

    def set_current(self, value):
        """Set the current to *value* (in mA).

        Returns: The current value sent back by the HV generator.
        """
        return self._set(
            'current', value, config.DELTA_I, config.CURRENT_LIMIT)

    def _set(self, name, value, delta, limit):
        """Set voltage or current to *value*.

        Args:
            name:
                'voltage' or 'current'.
            value:
                The value.
            delta:
                config.DELTA_U or config.DELTA_I.
            limit:
                The maximum value for *value*;
                config.VOLTAGE_LIMIT or config.CURRENT_LIMIT.

        Raises:
            ValueError: If *value* is not between 0 and *limit*.
        """
        if not 0 <= value <= limit:
            raise ValueError(
                f'*value* should be between 0 and {limit}; was {value}')

        int_value = round(value / delta)
        answer = self._send(Message(f'set {name}', int_value))
        return delta * answer.value

    def get_voltage(self):
        """Get the voltage (in V).

        Returns:
            The voltage value sent by the HV generator.
            This is always non-negative regardless of the polarity
            of the generator.
        """
        return self._get('voltage', config.DELTA_U)

    def get_current(self):
        """Get the current (in mA).

        Returns:
            The current value sent back by the HV generator.
        """
        return self._get('current', config.DELTA_I)

    def _get(self, name, delta):
        """Get voltage or current.

        Args:
            name:
                'voltage' or 'current'.
            delta:
                config.DELTA_U or config.DELTA_I.
        """
        answer = self._send(Message(f'get {name}'))
        return delta * answer.value

    def hv_on(self):
        """Turn the HV generator on."""
        self._send(Message('hv on', 1))
        time.sleep(0.1)
        self._send(Message('hv on', 0))

    def hv_off(self):
        """Turn the HV generator off."""
        self._send(Message('hv off', 1))
        time.sleep(0.1)
        self._send(Message('hv off', 0))

    def set_mode(self, mode):
        """Set the HV generator to remote or local mode.

        Args:
            mode: ``'local'``, ``'l'`` or ``1`` for local mode;
                ``'remote'``, ``'r'`` or ``0`` for remote mode.

        Raises:
            ValueError: If *mode* is not a valid value.
        """
        if mode in ['local', 'l', 1]:
            value = 1
        elif mode in ['remote', 'r', 0]:
            value = 0
        else:
            raise ValueError(f'invalid mode: {mode}')
        self._send(Message('set mode', value))

    def set_inhibition(self, value):
        """Activate or deactivate inhibition.

        args:
            value:
                If ``bool(value)`` evaluates to ``True``,
                inhibition is activated; otherwise it is deactivated.
        """
        value = bool(value)
        self._send(Message('set inhibition', value))

    def get_status(self):
        """Get the status of the HV generator.

        Returns:
            A :class:`dict` with keys and values corresponding to the 
            attributes of :attr:`status` and the values of those
            attributes as reported by the HV generator.
            However, :attr:`~Status.voltage` and
            :attr:`~Status.current` are not included. 
        """
        reply = self._send(Message('get status'))
        return self._parse_status_bits(reply.value)

    def full_status(self):
        """The same as :meth:`get_status`, but also includes
        :attr:`~Status.voltage` and :attr:`~Status.current`.
        """
        statusdict = self.get_status()
        statusdict['voltage'] = self.get_voltage()
        statusdict['current'] = self.get_current()
        return statusdict

    def halt(self):
        """Close the connection.

        This method sets the voltage and the current to 0,
        turns the HV generator off, closes the serial connection, and
        stops the parallel thread, if automatic polling is on.

        If there is no connection, actions that can't be performed
        are skipped.
        """
        self._stop_flag.set()
        # Threads that haven't been started are not alive.
        while self._thread.is_alive():
            time.sleep(0.001)

        # Try to turn the HV off; skip if there is no connection.
        try:
            self.set_voltage(0)
            self.set_current(0)
            self.hv_off()
        except serial.SerialException:
            pass

        # Try to close the connection; skip if the connection hasn't
        # been created (i.e. creating the connection caused an error).
        # This works even if the connection has already been closed.
        try:
            self._connection.close()
        except NameError:
            pass

    def _run_poll(self):
        """Update self.status continuously by calling
        self.full_status() at regular intervals.
        """
        while not self._stop_flag.is_set():
            self.full_status()
            time.sleep(self.timestep)

    def _send(self, query: Message) -> Message:
        """Send *query* to the HV generator and return the reply.

        Raises:
            serial.SerialException:
                If sending the message fails.
        """
        self._lock.acquire()

        try:
            # This may raise a serial.SerialException.
            self._connection.write(bytes(query))

            reply_bytes = self._connection.read_until(terminator=b'\r')
            reply = Message.from_bytes(reply_bytes)

            self._check_reply(query, reply)
            self._update_status(reply)
            return reply
        finally:
            # Make sure the lock is released in all cases.
            self._lock.release()

    def _update_status(self, reply: Message):
        """Update self.status according to the information in
        *reply*.
        """
        if reply.command in ['get voltage', 'set voltage']:
            self.status.voltage = config.DELTA_U * reply.value

        elif reply.command in ['get current', 'set current']:
            self.status.current = config.DELTA_I * reply.value

        elif reply.command == 'hv on':
            self.status.hv_on_command = bool(reply.value)

        elif reply.command == 'hv off':
            self.status.hv_off_command = bool(reply.value)

        elif reply.command == 'set mode':
            self.status.mode = 'local' if reply.value else 'remote'

        elif reply.command == 'set inhibition':
            self.status.inhibition = bool(reply.value)

        elif reply.command == 'get status':
            statusdict = self._parse_status_bits(reply.value)
            for name, value in statusdict.items():
                setattr(self.status, name, value)

        else:
            raise ValueError(f'invalid command: {reply.command}')

    @staticmethod
    def _parse_status_bits(value: int):
        """Extract the information contained in a value returned by
        the status command, and return it as a dict.

        Returns:
            A dict with keys consisting of the names of all
            the attributes of the Status class except
            voltage and current, and values containing the
            corresponding values.
        """
        bit_str = bin(value)[2:].zfill(8)
        bits = [int(b) for b in bit_str]

        return {
            'inhibition'    : bool(bits[0]),
            'mode'          : 'local' if bits[1] else 'remote',
            'hv_off_command': bool(bits[2]),
            'hv_on_command' : bool(bits[3]),
            'hv_on_status'  : bool(bits[4]),
            'interlock'     : 'open' if bits[5] else 'closed',
            'fault'         : bool(bits[6]),
            'regulation'    : 'voltage' if bits[7] else 'current'
        }

    @staticmethod
    def _check_reply(query: Message, reply: Message):
        """Make sure *reply* is a valid response to *query.*

        Raises:
            RuntimeError: If this is not the case.
        """
        if query.command != reply.command:
            raise RuntimeError(
                f"the query {repr(query.command)} was sent, "
                f"but {repr(reply.command)} was received")

        # Getters and the status command don't include a value, but
        # responses to them do.
        if query.command in ['get voltage', 'get current', 'get status']:
            return

        # For other commands, the return value should be the same that
        # was sent.
        if query.value != reply.value:
            raise RuntimeError(
                f"the value {query.value} was sent, "
                f"but {reply.value} was received")


@dataclass
class Status:
    """This class stores information about the current status of the
    HV generator.
    """

    voltage: float = 0.0
    """The voltage produced by the generator in V."""

    current: float = 0.0
    """The current produced by the generator in mA."""

    regulation: str = 'voltage'
    """``'voltage'`` or ``'current'`` depending on whether voltage or
    current regulation is being used.
    """

    hv_on_status: bool = False
    """``True`` if the generator is currently on, ``False`` if it's
    off.
    """

    hv_on_command: bool = False
    """The generator is turned on by setting the "hv on" parameter
    to 1 and then back to 0.
    This attribute displays the current value of that parameter as a
    boolean.
    """

    hv_off_command: bool = False
    """The generator is turned on by setting the "hv off" parameter
    to 1 and then back to 0.
    This attribute displays the current value of that parameter as a
    boolean.
    """

    mode: str = 'remote'
    """The control mode of the generator:
    ``'remote'`` or ``'local'``.
    """
    # Sphinx needs a line break after ':' here to parse it correctly.

    inhibition: bool = False
    """``True`` if inhibition is turned on, ``False`` otherwise.
    """

    interlock: str = 'closed'
    """The status of the interlock; ``open`` or ``closed``.
    """

    fault: bool = False
    """``True`` if there the generator is in a fault state, 
    ``False`` otherwise.
    """

    callback: Callable = None
    """A function that is called every time the contents of this object
    are changed. Its signature should be
    ::
        
        callback(status: Status) -> None
    """

    def __setattr__(self, name, value):
        """Call :attr:`callback(self) <callback>` whenever an attribute
        is set.
        """
        super().__setattr__(name, value)
        if self.callback:
            # *callback* is a function assigned as an attribute to 
            # *self* instead of a bound method, so *self* has to be
            # passed as an argument.
            self.callback(self)
