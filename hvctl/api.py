"""This module defines a set of methods for controlling the HV 
generator.
"""
import sys
import serial
import time
import threading
import textwrap
from dataclasses import dataclass

import config
from message import Message

@dataclass
class Status:
    """This class stores information about the current status of the 
    HV PSU.
    """
        
    voltage: float = 0
    """The voltage produced by the HV PSU in V."""
            
    current: float = 0
    """The current produced by the HV PSU in mA."""
    
    inhibit: bool = False
    """``True`` if the inhibit parameter is turned on, ``False`` 
    otherwise.
    """
            
    mode: str = 'remote'
    """HV control mode; ``'remote'`` or ``'local'.``"""
    # ';' is used instead of ':' because sphinx napoleon doesn't 
    # parse the latter correctly.
        
    HV_on_command: bool = False
    """The HV PSU is turned on by setting the "HV on" parameter to 1 
    and then back to 0. This attribute displays the current value of 
    that parameter as a boolean.
    """
            
    HV_off_command: bool = False
    """The HV PSU is turned on by setting the "HV off" parameter to 1 
    and then back to 0. This attribute displays the current value of 
    that parameter as a boolean.
    """

    HV_on_status: bool = False
    """``True`` if the HV PSU is currently on, ``False`` if it's 
    off.
    """
            
    interlock: str = 'closed'
    """The value of the interlock parameter; ``open`` or 
    ``closed``.
    """
            
    fault: bool = False
    """``True`` if there is a fault present at the HV PSU, ``False`` 
    otherwise.
    """
    
    regulation: str = 'current'
    """``'voltage'`` or ``'current'`` depending on whether voltage or 
    current regulation is being used.
    """
    
    callback: object = None
    """A function (with no arguments) that is called every time the 
    contents of this object are changed.
    """
    
    def __setattr__(self, name, value):
        """Call :attr:`callback` whenever an attribute is set."""
        super().__setattr__(name, value)
        if self.callback:
            self.callback()
            
    def __str__(self):
        """Return the contents of *self* in a form suitable to be 
        displayed in a TUI.
        """
        return '\n'.join([
            f'Voltage: {self.voltage:.2f} V',
            f'Current: {self.current:.2f} mA',
            f'Regulation mode: {self.regulation}',
            f'',
            f'HV power: {"on" if self.HV_on_status else "off"}',
            f'HV on command given: {self.HV_on_command}',
            f'HV off command given: {self.HV_off_command}',
            f'',
            f'Interlock: {self.interlock}',
            'Fault(s) present' if self.fault else 'No faults present',
        ])
    
class API():
    """This class defines an API for communicating with a 
    Technix HV PSU.
    
    Creating an instance of this class forms a serial connection to 
    the HV PSU, after which messages can be sent to it by calling the 
    methods of the instance.
    
    If an API is initialized with ``poll=True`` it will periodically 
    send an automatic command to the HV PSU.
    This prevents the HV PSU from switching to local mode, which it 
    normally does after not receiving a command for 5 seconds.
    
    The commands that are sent cycle between :meth:`get_voltage`, 
    :meth:`get_current` and :meth:`status`.
    They will print no messages even if :attr:`verbose` is ``False``, 
    but will update the values of the attributes of the API.
    The time period between commands is determined by :attr:`timestep`.

    The polling routine is run in a parallel thread, and should be 
    closed by calling after the API is no lenger needed.
    This can be done by calling :meth:`halt` or running the API in a 
    ``with`` bolck. Both methods also close the serial connection.
            
    Attributes:
        status (:class:`Status`):
            An object storing the current status of the HV PSU. 
            Its attributes are updated every time the HV PSU send 
            back a reply.
            
        verbose (bool):
            If this is ``True``, methods will print messages 
            explaining what they are doing whenever they are called. 
            
        timestep (float):
            If *self* was initialized with ``poll=True``, this 
            determines the time (in seconds) between polling messages.
            The initial value is 1.
            
        inputfile:
            A file-like object for receiving input. This isn't
            directly used by this class (i.e. is only used by the 
            :class:`CommandLineTUI` subclass), but is included for 
            symmetry since :attr:`outputfile` is also defined here.
            
        outputfile:
            A file-like object used for writing output.
    """
    
    def __init__(self, status, serial_kwargs=config.SERIAL_KWARGS, poll=True):
        """Create a new instance of this class and form a serial 
        connection to the HV PSU.
        
        Args:
            serial_kwargs (dict): 
                Keyword arguments for creating a 
                :class:`serial.Serial` object.
            
            poll (bool): 
                Determines whether automatic polling should be used 
                or not (see the class description for more details.)
            
        The other arguments set initial values for the attributes of 
        this class.                 
        """        
        self._connection = None
        self.status = status
        self.serial_kwargs = serial_kwargs
        self.poll = poll
        self.timestep = 1
        
        self._stop_flag = threading.Event()
        # *lock* prevents *_poll*-sent and user-sent messages from 
        # being sent at the same time. 
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._poll, daemon=True)
        
    def run(self):
        self._connection = serial.Serial(**self.serial_kwargs)       
        if self.poll:
            self._thread.start()
        
    def __enter__(self):
        """Called upon enering a ``with`` block; returns *self*."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Called upon exiting a ``with`` block; calls :meth:`halt`."""
        self.halt()

    def set_voltage(self, value):
        """Set HV voltage to *value* (in V).
        
        Returns: The voltage value sent back by the HV PSU.
        """
        return self._set('voltage', 'V', config.DELTA_U, config.VOLTAGE_LIMIT, 
                         value)
    
    def set_current(self, value):
        """Set HV current to *value* (in mA).
        
        Returns: The current value sent back by the HV PSU.
        """
        return self._set('current', 'mA', config.DELTA_I, config.CURRENT_LIMIT, 
                         value)
        
    def get_voltage(self):
        """Get HV voltage (in V).
        
        Returns: The voltage value sent by the HV PSU.
        """
        return self._get('voltage', 'V', config.DELTA_U)
    
    def get_current(self):
        """Get HV current (in mA).
        
        Returns: 
            The current value sent back by the HV PSU.
        """
        return self._get('current', 'mA', config.DELTA_I)
        
    def HV_on(self):
        """Turn the HV on."""
        self._send(Message('HV on', 1))
        time.sleep(0.1) # Delay 100 ms
        self._send(Message('HV on', 0))
        self.HV_on = True
        
    def HV_off(self):
        """Turn the HV off."""        
        self._send(Message('HV off', 1))
        time.sleep(0.1) # Delay 100 ms
        self._send(Message('HV off', 0))
        self.HV_on = False
        
    def set_mode(self, mode):
        """Set the HV to remote or local mode.
        
        Args:
            mode: 'local', 'l' or 1 for local mode;
                'remote', 'r' or 0 for remote mode.
                
        Raises:
            ValueError: If *mode* is not a valid value.
        """        
        if mode in ['local', 'l', 1]:
            value = 1
        elif mode in ['remote', 'r', 0]:
            value = 0
        else:
            raise ValueError(f'invalid mode: {mode}')        
        self._send(Message('mode', value))

    def set_inhibit(self, value):
        """Activate or deactivate HV inhibition.
        
        args:
            value: 
                If ``bool(value)`` evaluates to ``True``, 
                inhibition is activated; otherwise it is deactivated.
        """
        value = bool(value)
        self._send(Message('inhibit', value))
        
    def get_status(self):
        """Ask HV status. A status message contains the values of 
        all the attributes of :attr:`status` except voltage and 
        current.
        """
        # TODO: update docstring
        reply = self._send(Message('status'))
        
        statusdict = self._parse_status_bits(reply.value)
        return statusdict
        
    def halt(self):
        """Close the connection.
        
        This method sets the voltage and the current to 0, 
        turns the HV off, closes the serial connection and stops the 
        parallel thread, if automatic polling is on.
        
        If the connection is already closed, actions that can't be 
        performed are skipped.
        """
        self._stop_flag.set()
        while self._thread.is_alive():
            time.sleep(0.001)
        
        # A try block wouldn't work, since an extra "setting voltage"
        # message would be printed even if the connection is already 
        # closed.
        if self._connection and self._connection.is_open:
            self.set_voltage(0)
            self.set_current(0)
            self.HV_off()
            self._connection.close()
        
    def _log(self, message):
        """Print *message* if :attr:`verbose` is ``True``."""
        if self.verbose:
            print(message, file=self.outputfile, flush=True)
                
    def _poll(self):
        """Send messages to the HV PSU at regular intervals."""
        
        cycle = [self.get_voltage, self.get_current, self.get_status]
        i = 0
        
        while not self._stop_flag.is_set():
            cycle[i]()
            i = (i + 1) % len(cycle)
            time.sleep(self.timestep)

    def _set(self, name, unit, delta, limit, value):
        """Set voltage or current."""
        self._check_value(value, limit)
        int_value = round(value / delta)
        answer = self._send(Message(f'set {name}', int_value))
        return_value = delta * answer.value
        setattr(self, name, return_value)
        return return_value
    
    @staticmethod
    def _check_value(value, limit):
        """Make sure *value* is between 0 and *limit*.
        *limit* can also be negative.
        
        Raises:
            ValueError: If *value* is not between 0 and *limit*.
        """
        in_nonnegative_range = limit >= 0 and 0 <= value <= limit
        in_negative_range = limit < 0 and limit <= value <= 0
        
        if not (in_nonnegative_range or in_negative_range):
            raise ValueError(
                f'*value* should be between 0 and {limit}; was {value}')
            
    def _get(self, name, unit, delta):
        """Get voltage or current."""        
        answer = self._send(Message(f'get {name}'))
        return_value = delta * answer.value
        setattr(self, name, return_value)
        return return_value

    def _send(self, query: Message) -> Message:
        """Send *query* to the HV PSU and return the reply."""
        self._lock.acquire()
        self._connection.write(query.to_bytes())
        
        reply_bytes = self._connection.read_until(terminator=b'\r')
        reply = Message.from_bytes(reply_bytes)
        
        self._check_reply(query, reply)
        self._update_status(reply)
        self._lock.release()
        return reply
        
    def _update_status(self, reply: Message):
        """Update self.status according to the information in 
        *reply*.
        """
        if reply.command in ['get voltage', 'set voltage']:
            self.status.voltage = config.DELTA_U * reply.value
        
        elif reply.command in ['get current', 'set current']:
            self.status.current = config.DELTA_I * reply.value
            
        elif reply.command == 'HV on':
            self.status.HV_on_command = bool(reply.value)
            
        elif reply.command == 'HV off':
            self.status.HV_off_command = bool(reply.value)
            
        elif reply.command == 'mode':
            self.status.mode = 'local' if reply.value else 'remote'
            
        elif reply.command == 'inhibit':
            self.status.inhibit = bool(reply.value)
            
        elif reply.command == 'status':
            statusdict = self._parse_status_bits(reply.value)
            for name, value in statusdict.items():
                setattr(self.status, name, value)
            
        else:
            raise ValueError(f'invalid command: {reply.command}')
            
    def _parse_status_bits(self, value: int):
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
            'inhibit'       : bool(bits[0]),
            'mode'          : 'local' if bits[1] else 'remote',
            'HV_off_command': bool(bits[2]),
            'HV_on_command' : bool(bits[3]),
            'HV_on_status'  : bool(bits[4]),
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
        if query.command in ['get voltage', 'get current', 'status']:
            return
        
        # For other commands, the return value should be the same that 
        # was sent.
        if query.value != reply.value:
            raise RuntimeError(
                f"the value {query.value} was sent, "
                f"but {reply.value} was received")