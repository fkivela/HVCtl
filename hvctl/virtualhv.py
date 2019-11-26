"""This module defines the :class:`VirtualHV` class."""

from .message import Message
from .virtualconnection import VirtualConnection


class VirtualHV():
    """A virtual high voltage generator.
    
    This class simulates a HV generator that can be communicated with
    through  a serial connection. This makes it possible to test
    HVCtl without access to a physical device.

    Attributes:
        connection:
            A :class:`~hvctl.virtualconnection.VirtualConnection`
            object used for simulating a serial connection.

        voltage (float):
            | The voltage of the virtual HV generator in V.
            | Initial value: ``0``.

        current (float):
            | The current of the virtual HV generator in mA.
            | Initial value: ``0``.

        hv_on_command (bool):
            | The virtual HV generator is turned on by setting this
              first to ``True`` and then back to ``False``.
            | Initial value: ``False``.

        hv_off_command (bool):
            | The virtual HV generator is turned off by setting this
              first to ``True`` and then back to ``False``.
            | Initial value: ``False``.

        hv_on_status (bool):
            | Determines whether the virtual HV generator is on 
              (``True``) or off (``False``).
            | Initial value: ``False``.

        mode (string):
            | ``'local'`` or ``'remote'``.
            | Determines the control mode of the virtual HV generator.
            | Initial value: ``'remote'``.

        inhibit (bool):
            | Determines whether inhibition is turned on (``True``) or
              off (``False``) at the virtual HV generator.
            | Initial value: ``False``.

        interlock (bool):
            | ``True`` if the interlock is active, ``False`` if it is
              not.
            | Initial value: ``False``.

        fault (bool):
            | ``True`` if there is a fault present in the virtual
              HV generator, ``False`` otherwise.
            | Initial value: ``False``.

        regulation (string):
            | ``'current'`` or ``'voltage'``.
            | Determines whether the virtual HV generator is regulating
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

    def get_voltage(self, *args):
        """Handle a ``'get voltage'`` command.

        Args:
            args: These are ignored.

        Returns:
            :attr:`voltage`."""
        return self.voltage

    def get_current(self, *args):
        """Handle a ``'get current'`` command.

        Args:
            args: These are ignored.

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
        self.regulation = 'voltage'
        return self.get_voltage()

    def set_current(self, value):
        """Handle a ``'set current'`` command.

        Sets :attr:`current` to *value*.

        Returns:
            The new value of :attr:`current`.
        """
        self.current = value
        self.regulation = 'current'
        return self.get_current()

    def hv_on(self, value):
        """Handle a ``'HV on'`` command.

        If :attr:`hv_on_command` is ``False`` and *value* is ``True``,
        :attr:`hv_on_command` is set to ``True``.

        If :attr:`hv_on_command` is ``True`` and *value* is ``False``,
        :attr:`hv_on_status` is set to ``True`` and
        :attr:`hv_on_command` is set to ``False``.

        If *value* has the same value as :attr:`hv_on_command`,
        a :exc:`RuntimeError` is raised.

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
        a :exc:`RuntimeError` is raised.

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
            ``1`` if the new value of :attr:`mode` is ``'local'``,
            ``0`` if it is ``'remote'``.
        """
        self.mode = 'local' if value else 'remote'
        return value

    def set_inhibit(self, value):
        """Handle a ``'set inhibit'`` command.

        Sets :attr:`inhibit` to ``bool(value)``.
        
        Returns:
            The new value of :attr:`inhibit`. 
        """
        self.inhibit = bool(value)
        return self.inhibit

    def get_status(self, _):
        """Handle a ``'get status'`` command.

        This method returns an 8-bit unsigned integer describing the
        current status of the virtual HV generator (excluding voltage
        and current).
        The values of the bits in the number are copied from the
        attributes of this object in the following manner:

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

        This method executes the following steps:
        
        1. Turn *input_* into a :class:`~hvctl.message.Message`
           object with :meth:`Message.from_bytes()
           <hvctl.message.Message.from_bytes>`.
        2. Generate a method name by replacing ``' '`` with
           ``'_'`` in :class:`message.command <hvctl.message.Message>`
           and call a method with that name.
        3. Create a new :class:`~hvctl.message.Message` object.
           The :attr:`command <hvctl.message.Message.command>`
           attribute of the new object is copied from the input
           message and the
           :attr:`value <hvctl.message.Message.command>` attribute is
           the value returned by the method that was called.
        4. Convert the new message to a :class:`bytes` object with
           :meth:`Message.__bytes__()
           <hvctl.message.Message.__bytes__>` and return the bytes.

        Args:
            input_:
                A :class:`bytes` object created by
                :meth:`Message.__bytes__()
                <hvctl.message.Message.__bytes__>`.

        Returns:
            A :class:`bytes` object that can be passed to
            :meth:`Message.from_bytes()
            <hvctl.message.Message.from_bytes>`.
        """
        message = Message.from_bytes(input_, is_answer=False)
        command = message.command
        method = getattr(self, command.replace(' ', '_'))

        ret = method(message.value)
        return bytes(Message(command, ret, is_answer=True))
