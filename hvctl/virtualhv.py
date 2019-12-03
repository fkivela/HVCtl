"""This module defines the :class:`VirtualHV` class."""

import time

from .api import Status
from .message import Message
from .virtualconnection import VirtualConnection


class VirtualHV():
    """A virtual high voltage generator.
    
    This class simulates a HV generator that can be communicated with
    through  a serial connection. This makes it possible to test
    HVCtl without access to a physical device.

    Attributes:
        connection (VirtualConnection):
            A simulated serial connection.
            
        status (Status):
            The status of the virtual HV generator.
            
        time_of_last_command (float):
            This is initialized to :func:`time.time` when a
            :class:`VirtualHV` object is created,
            and updated to the current time every time a command is
            sent to the virtual HV.
            
            See :attr:`refresh_watchdog` for further details.

    ..
        Some aliases for Sphinx.
        |attribute| shows up in the final documentaton as
        status.attribute,
        with 'status' linking to VirtualHV.status and
        '.attribute' linking to api.Status.attribute.     
        
    .. |voltage| replace::
        :attr:`status`:attr:`.voltage
        <hvctl.api.Status.voltage>`
    .. |current| replace::
        :attr:`status`:attr:`.current
        <hvctl.api.Status.current>`
    .. |regulation| replace::
        :attr:`status`:attr:`.regulation
        <hvctl.api.Status.regulation>`
    .. |hv_on_status| replace::
        :attr:`status`:attr:`.hv_on_status
        <hvctl.api.Status.hv_on_status>`
    .. |hv_on_command| replace::
        :attr:`status`:attr:`.hv_on_command
        <hvctl.api.Status.hv_on_command>`
    .. |hv_off_command| replace::
        :attr:`status`:attr:`.hv_off_command
        <hvctl.api.Status.hv_off_command>`
    .. |mode| replace::
        :attr:`status`:attr:`.mode
        <hvctl.api.Status.mode>`
    .. |inhibit| replace::
        :attr:`status`:attr:`.inhibit
        <hvctl.api.Status.inhibit>`
    .. |interlock| replace::
        :attr:`status`:attr:`.interlock
        <hvctl.api.Status.interlock>`
    .. |fault| replace::
        :attr:`status`:attr:`.fault
        <hvctl.api.Status.fault>`
    """

    def __init__(self):
        """Initialize a new :class:`VirtualHV`."""
        self.connection = VirtualConnection(process=self.process)
        self.status = Status()
        self.time_of_last_command = time.time()

    def __enter__(self):
        """Called upon entering a ``with`` block;
        returns *self*.
        """
        return self

    def __exit__(self, type_, value, traceback):
        """Called upon exiting a ``with`` block; calls
        :attr:`connection`:meth:`.close()
        <hvctl.virtualconnection.VirtualConnection.close>`.
        """
        self.connection.close()
        
    def get_voltage(self, *args):
        """Handle a ``'get voltage'`` command.
        
        Args:
            args: These are ignored.

        Returns:
            |voltage|, or 0 if |hv_on_status| is ``False`` or
            |inhibit| is ``True``.
            """
        output_active = self.status.hv_on_status and not self.status.inhibit
        return self.status.voltage if output_active else 0

    def get_current(self, *args):
        """Handle a ``'get current'`` command.

        Args:
            args: These are ignored.

        Returns:
            |current|, or 0 if |hv_on_status| is ``False`` or
            |inhibit| is ``True``.
            """
        output_active = self.status.hv_on_status and not self.status.inhibit
        return self.status.current if output_active else 0

    def set_voltage(self, value):
        """Handle a ``'set voltage'`` command.

        Sets |voltage| to *value* and |regulation| to ``'voltage'``.

        Returns:
            *value*.
        """
        self.status.voltage = value
        self.status.regulation = 'voltage'
        return self.status.voltage

    def set_current(self, value):
        """Handle a ``'set current'`` command.

        Sets |current| to *value* and |regulation| to ``'current'``.

        Returns:
            The new value of |current|.
        """
        self.status.current = value
        self.status.regulation = 'current'
        return self.status.current

    def hv_on(self, value):
        """Handle a ``'HV on'`` command.

        This method first sets |hv_on_command| to ``bool(value)``.
        |hv_on_status| is then set to ``True``,
        if the following conditions are met:
            
        - The old value of |hv_on_command| was ``True``.
        - The new value of |hv_on_command| is ``False``.
        - |inhibit| is ``False``.
        - |fault| is ``False``.

        Returns:
            *value*.
        """
        old_value = self.status.hv_on_command
        self.status.hv_on_command = bool(value)
        
        should_turn_on = old_value == 1 and value == 0
        can_turn_on = not (self.status.fault or self.status.mode == 'local')
        
        if should_turn_on and can_turn_on:
            self.status.hv_on_status = True

        return value

    def hv_off(self, value):
        """Handle a ``'HV off'`` command.

        This method first sets |hv_off_command| to ``bool(value)``.
        |hv_on_status| is then set to ``False``,
        if the following conditions are met:
            
        - The old value of |hv_off_command| was ``True``.
        - The new value of |hv_off_command| is ``False``.

        Returns:
            *value*.
        """
        old_value = self.status.hv_off_command
        self.status.hv_off_command = bool(value)
        
        should_turn_off = old_value == 1 and value == 0
        
        if should_turn_off:
            self.status.hv_on_status = False

        return value

    def set_mode(self, value):
        """Handle a ``'set mode'`` command.

        If ``bool(value)`` is ``True``,
        |mode| is set to ``'local'``;
        otherwise it is set to ``'remote'``.
        
        Setting the mode to ``'local'`` also sets
        |hv_on_status| to ``False``,
        if it is not already.

        Returns:
            *value*.
        """
        if value:
            self.status.mode = 'local'
            self.status.hv_on_status = False
        else:
            self.status.mode = 'remote'
        
        return value

    def set_inhibit(self, value):
        """Handle a ``'set inhibit'`` command.

        Sets |inhibit| to ``bool(value)``.
        
        Returns:
           *value*.
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

        :Bit 0: |inhibit|
        :Bit 1: |mode|
            (``1`` for ``'local'``, ``0`` for ``'remote'``)
        :Bit 2: |hv_off_command|
        :Bit 3: |hv_on_command|
        :Bit 4: |hv_on_status|
        :Bit 5: |interlock|
            (``1`` for ``'open'``, ``0`` for ``'closed'``)
        :Bit 6: |fault|
        :Bit 7: |regulation|
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
        """Parse *input_* into a command and execute it.

        This method executes the following steps:
        
        1. Call :meth:`refresh_watchdog`.
        2. Turn *input_* into a :class:`~hvctl.message.Message`
           object with :meth:`Message.from_bytes()
           <hvctl.message.Message.from_bytes>`.
        3. Generate a method name by replacing ``' '`` with
           ``'_'`` in :class:`message.command <hvctl.message.Message>`
           and call a method with that name.
        4. Create a new :class:`~hvctl.message.Message` object.
           The :attr:`command <hvctl.message.Message.command>`
           attribute of the new object is copied from the input
           message and the
           :attr:`value <hvctl.message.Message.command>` attribute is
           the value returned by the method that was called.
        5. Convert the new message to a :class:`bytes` object with
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
        self.refresh_watchdog()
        
        message = Message.from_bytes(input_, is_answer=False)
        command = message.command
        method = getattr(self, command.replace(' ', '_'))

        ret = method(message.value)
        return bytes(Message(command, ret, is_answer=True))

    def open_interlock(self):
        """Simulate opening the interlock.
        
        Sets |interlock| to ``'open'``, |fault| to ``True``
        and |hv_on_status| to ``False``.
        """
        self.status.interlock = 'open'
        self.status.fault = True
        self.status.hv_on_status = False
        
    def close_interlock(self):
        """Simulate closing the interlock.
        
        Sets |interlock| to ``'closed'``.
        """
        self.status.interlock = 'closed'
        
    def reset_fault(self):
        """Simulate resetting the fault state through the HV off button
        on the front panel of the HV generator.
        
        Sets |Fault| to ``'False'``, if |interlock| is ``'closed'``.
        """
        if self.status.interlock == 'closed':
            self.status.fault = False

    def refresh_watchdog(self):
        """Switch to local mode if over 5 seconds has elapsed since
        the last command was sent.
        
        The HV generator contains a watchdog device that automatically
        turns the HV off and switches the generator to local mode if
        the generator doesn't receive any commands for 5 seconds.
        
        VirtualHV emulates this functionality with this method,
        which compares :attr:`time_of_last_command` to the current
        time. If the difference between these two times is more than 5
        seconds, |mode| is set to ``'local'``
        and |hv_on_status| to ``False``.
        Finally, :attr:`time_of_last_command` is updated to the current
        time.
        """
        now = time.time()
        if now - self.time_of_last_command > 5:
            self.status.mode = 'local'
            self.status.hv_on_status = False
        self.time_of_last_command = time.time()
