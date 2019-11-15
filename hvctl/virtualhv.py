"""This module defines the :class:`VirtualHV` class."""

from .message import Message
from .virtualconnection import VirtualConnection


class VirtualHV():
    """A virtual high voltage generator.

    This class simulates a HV PSU that can be communicated with
    through  a serial connection. This makes it possible to test
    HVCtl without access to a physical device.

    Attributes:
        connection:
            A :class:`~hvctl.virtualconnection.VirtualConnection`
            object used for simulating a serial connection.

        voltage (float):
            | The voltage of the virtual HV PSU in V.
            | Initial value: ``0``.

        current (float):
            | The current of the virtual HV PSU in mA.
            | Initial value: ``0``.

        hv_on_command (bool):
            | The virtual HV PSU is turned on by setting this first to
              True and then back to False.
            | Initial value: ``False``.

        hv_off_command (bool):
            | The virtual HV PSU is turned off by setting this first to
              True and then back to False.
            | Initial value: ``False``.

        hv_on_status (bool):
            | Determines whether the virtual HV PSU is on (``True``)
              or off (``False``).
            | Initial value: ``False``.

        mode (string):
            | ``'local'`` or ``'remote'``.
            | Determines the control mode of the virtual HV PSU.
            | Initial value: ``'remote'``.

        inhibit (bool):
            | Determines whether inhibition is turned on (``True``) or
              off (``False``) at the virtual HV PSU.
            | Initial value: ``False``.

        interlock (bool):
            | ``True`` IFF the HV interlock is active.
            | Initial value: ``False``.

        fault (bool):
            | ``True`` IFF there are faults present in the virtual
              HV PSU.
            | Initial value: ``False``.

        regulation (string):
            | ``'current'`` or ``'voltage'``.
            | Determines whether the virtual HV PSU is regulating
              current or voltage.
            | Initial value: ``'voltage'``
    """

    def __init__(self):
        """Initialize a new :class:`VirtualHV`."""

        self.connection = VirtualConnection(process=self.process)

        self.voltage = 0
        self.current = 0
        self.hv_on_command = False
        self.hv_off_command = False
        self.hv_on_status = False
        self.mode = 'remote'
        self.inhibit = False
        self.interlock = False
        self.fault = False
        self.regulation = 'voltage'

    def __enter__(self):
        """Called upon entering a ``with`` block;
        returns *self*.
        """
        return self

    def __exit__(self, type_, value, traceback):
        """Called upon exiting a ``with`` block; calls
        :meth:`connection.close()
        <hvctl.virtualconnection.VirtualConnection.close>`.
        """
        self.connection.close()

    def get_voltage(self, _):
        """Handle a ``'get voltage'`` command.

        Args:
            _: This is ignored.

        Returns:
            :attr:`voltage`."""
        return self.voltage

    def get_current(self, _):
        """Handle a ``'get current'`` command.

        Args:
            _: This is ignored.

        Returns:
            :attr:`current`."""
        return self.current

    def set_voltage(self, value):
        """Handle a ``'set voltage'`` command.

        Sets :attr:`voltage` to *value*.

        Returns:
            The new value of :attr:`voltage`.
        """
        self.voltage = value
        return self.voltage

    def set_current(self, value):
        """Handle a ``'set current'`` command.

        Sets :attr:`current` to *value*.

        Returns:
            The new value of :attr:`current`.
        """
        self.current = value
        return self.current

    def hv_on(self, value):
        """Handle a ``'HV on'`` command.

        If :attr:`hv_on_command` is ``False`` and *value* is ``True``,
        :attr:`hv_on_command` is set to ``True``.

        If :attr:`hv_on_command` is ``True`` and *value* is ``False``,
        :attr:`hv_on_status` is set to ``True`` and
        :attr:`hv_on_command` is set to ``False``.

        If *value* has the same value as :attr:`hv_on_command`,
        a :exc:`RuntimeError` is raised.`

        Returns:
            The new value of :attr:`hv_on_command`.
        """
        if value == self.hv_on_command:
            raise RuntimeError(f'*hv_on_command* is already {value}')

        if self.hv_on_command:
            self.hv_on_status = True

        self.hv_on_command = value
        return self.hv_on_command

    def hv_off(self, value):
        """Handle a ``'HV off'`` command.

        If :attr:`hv_off_command` is ``False`` and *value* is ``True``,
        :attr:`hv_off_command` is set to ``True``.

        If :attr:`hv_off_command` is ``True`` and *value* is ``False``,
        :attr:`hv_on_status` is set to ``False`` and
        :attr:`hv_off_command` is set to ``False``.

        If *value* has the same value as :attr:`hv_off_command`,
        a :exc:`RuntimeError` is raised.`

        Returns:
            The new value of :attr:`hv_off_command`.
        """
        if value == self.hv_off_command:
            raise RuntimeError(f'*hv_off_command* is already {value}')

        if self.hv_off_command:
            self.hv_on_status = False

        self.hv_off_command = value
        return self.hv_off_command

    def set_mode(self, value):
        """Handle a ``'set mode'`` command.

        If ``bool(value)`` is ``True``, :attr:`mode` is set to
        ``'local'``; otherwise it is set to ``'remote'``.

        Returns:
            The new value of :attr:`mode`.
        """
        self.mode = 'local' if value else 'remote'
        return value

    def set_inhibit(self, value):
        """Handle a ``'set inhibit'`` command.

        If ``bool(value)`` is ``True``, :attr:`inhibit` is set to
        ``'active'``; otherwise it is set to ``'remote'``.

        Returns:
            The new value of :attr:`mode`.
        """
        self.inhibit = 'active' if value else 'idle'
        return value

    def get_status(self, _):
        """Handle a ``'get status'`` command.

        This method returns an 8-bit integer describing the current
        status of the virtual HV PSU (excluding voltage and current).
        The values of the bits in the number are copied from the
        attributes of *self* in the following manner:

        :Bit 0: :attr:`inhibit`
        :Bit 1: :attr:`mode` (``1`` for ``'local'``,
                              ``0`` for ``'remote'``),
        :Bit 2: :attr:`hv_off_command`,
        :Bit 3: :attr:`hv_on_command`,
        :Bit 4: :attr:`hv_on_status`,
        :Bit 5: :attr:`interlock`,
        :Bit 6: :attr:`fault`,
        :Bit 7: :attr:`regulation` (``1`` for ``'voltage'``,
                                    ``0`` for ``'current'``),

        Since ``True`` equals ``1`` in Python, attributes with a value
        of ``True`` will set their respective bit to ``1``,
        and attributes with a value of ``False`` will set their bit
        to ``0``.
        The bits are in big-endian order.

        Returns:
            An :class:`int` in ``range(256)``.
        """
        values = [
            self.inhibit == 'active',
            self.mode == 'local',
            self.hv_off_command,
            self.hv_on_command,
            self.hv_on_status,
            self.interlock,
            self.fault,
            self.regulation == 'voltage']
        bits = ''.join([str(int(v)) for v in values])
        return int(bits, 2)

    def process(self, input_):
        """Parse input into a command and execute it.

        Args:
            input_:
                A bytes-like object created by
                :func:`hvctl.message.Message.to_bytes`.

        Returns:
            A :class:`bytes` object that can be passed to
            :func:`hvctl.message.Message.from_bytes`.
            The return message will contain the same command as the
            input message, but if the command changed a value of an
            attribute of *self*, the new value will be included in the
            message instead of the old.
        """
        message = Message.from_bytes(input_, is_answer=False)
        command = message.command
        method = getattr(self, command.replace(' ', '_'))

        ret = method(message.value)
        return bytes(Message(command, ret, is_answer=True))
