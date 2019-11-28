"""This module defines the :class:`VirtualHV` class."""

from .api import Status
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
            
        status:
            A :class:`~hvctl.api.Status` object that stores the status
            of the virtual HV generator.
    """

    def __init__(self):
        """Initialize a new :class:`VirtualHV`."""
        self.connection = VirtualConnection(process=self.process)
        self.status = Status()

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
            :attr:`status.voltage <status>`."""
        return self.status.voltage

    def get_current(self, *args):
        """Handle a ``'get current'`` command.

        Args:
            args: These are ignored.

        Returns:
            :attr:`status.current <status>`."""
        return self.status.current

    def set_voltage(self, value):
        """Handle a ``'set voltage'`` command.

        Sets :attr:`status.voltage <status>` to *value*.

        Returns:
            The new value of :attr:`status.voltage <status>`.
        """
        self.status.voltage = value
        self.status.regulation = 'voltage'
        return self.get_voltage()

    def set_current(self, value):
        """Handle a ``'set current'`` command.

        Sets :attr:`status.current <status>` to *value*.

        Returns:
            The new value of :attr:`status.current <status>`.
        """
        self.status.current = value
        self.status.regulation = 'current'
        return self.get_current()

    def hv_on(self, value):
        """Handle a ``'HV on'`` command.

        If :attr:`status.hv_on_command <status>` is ``False``
        and *value* is ``True``,
        :attr:`status.hv_on_command <status>` is set to ``True``.

        If :attr:`status.hv_on_command <status>` is ``True``
        and *value* is ``False``,
        :attr:`status.hv_on_status <status>` is set to ``True`` and
        :attr:`status.hv_on_command <status>` is set to ``False``.

        If *value* has the same value as
        :attr:`status.hv_on_command <status>`,
        a :exc:`RuntimeError` is raised.

        Returns:
            The new value of :attr:`status.hv_on_command <status>`.
        """
        if value == self.status.hv_on_command:
            raise RuntimeError(f'*hv_on_command* is already {value}')

        if self.status.hv_on_command:
            self.status.hv_on_status = True

        self.status.hv_on_command = value
        return self.status.hv_on_command

    def hv_off(self, value):
        """Handle a ``'HV off'`` command.

        If :attr:`status.hv_off_command <status>` is ``False``
        and *value* is ``True``,
        :attr:`status.hv_off_command <status>` is set to ``True``.

        If :attr:`status.hv_off_command <status>` is ``True``
        and *value* is ``False``,
        :attr:`status.hv_on_status <status>` is set to ``False`` and
        :attr:`status.hv_off_command <status>` is set to ``False``.

        If *value* has the same value as
        :attr:`status.hv_off_command <status>`,
        a :exc:`RuntimeError` is raised.

        Returns:
            The new value of :attr:`status.hv_off_command <status>`.
        """
        if value == self.status.hv_off_command:
            raise RuntimeError(f'*hv_off_command* is already {value}')

        if self.status.hv_off_command:
            self.status.hv_on_status = False

        self.status.hv_off_command = value
        return self.status.hv_off_command

    def set_mode(self, value):
        """Handle a ``'set mode'`` command.

        If ``bool(value)`` is ``True``,
        :attr:`status.mode <status>` is set to ``'local'``;
        otherwise it is set to ``'remote'``.

        Returns:
            ``1`` if the new value of :attr:`status.mode <status>`
            is ``'local'``, ``0`` if it is ``'remote'``.
        """
        self.mode = 'local' if value else 'remote'
        return value

    def set_inhibit(self, value):
        """Handle a ``'set inhibit'`` command.

        Sets :attr:`status.inhibit <status>` to ``bool(value)``.
        
        Returns:
            The new value of :attr:`status.inhibit <status>`. 
        """
        self.status.inhibit = bool(value)
        return self.status.inhibit

    def get_status(self, _):
        """Handle a ``'get status'`` command.

        This method returns an 8-bit unsigned integer describing the
        current status of the virtual HV generator (excluding voltage
        and current).
        The values of the bits in the number are copied from the
        attributes of this object in the following manner:

        :Bit 0: :attr:`status.inhibit <status>`
        :Bit 1: :attr:`status.mode <status>`
            (``1`` for ``'local'``, ``0`` for ``'remote'``)
        :Bit 2: :attr:`status.hv_off_command <status>`
        :Bit 3: :attr:`status.hv_on_command <status>`
        :Bit 4: :attr:`status.hv_on_status <status>`
        :Bit 5: :attr:`status.interlock <status>`
        :Bit 6: :attr:`status.fault <status>`
        :Bit 7: :attr:`status.regulation <status>`
            (``1`` for ``'voltage'``, ``0`` for ``'current'``)

        Since ``True`` equals ``1`` in Python, attributes with a value
        of ``True`` will set their respective bit to ``1``,
        and attributes with a value of ``False`` will set their bit
        to ``0``.
        The bits are in big-endian order.

        Returns:
            An :class:`int` in ``range(256)``.
        """
        values = [
            self.status.inhibit,
            self.status.mode == 'local',
            self.status.hv_off_command,
            self.status.hv_on_command,
            self.status.hv_on_status,
            self.status.interlock == 'open',
            self.status.fault,
            self.status.regulation == 'voltage']
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
