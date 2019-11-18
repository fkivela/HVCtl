"""This module defines the :class:`Message` class for communicating with
the HV generator."""

import re

from . import config

_COMMAND_TO_PATTERN = {
    'set voltage': 'd1,{}\r',
    'set current': 'd2,{}\r',
    'get voltage': 'a1{}\r',
    'get current': 'a2{}\r',
    'hv on'      : 'P5,{}\r',
    'hv off'     : 'P6,{}\r',
    'set mode'   : 'P7,{}\r',
    'set inhibit': 'P8,{}\r',
    'get status' : 'E{}\r'
}

_PATTERN_TO_COMMAND = {p: c for c, p
                       in _COMMAND_TO_PATTERN.items()}

COMMANDS = list(_COMMAND_TO_PATTERN.keys())
"""A list of valid commands."""


class Message():
    """This class represents a message sent to or received from the HV
    generator.

    Attributes:
        command (string):
            The command that is sent to the HV generator, 
            or the command to which *self* is an answer; 
            e.g. ``'set voltage'`` or ``'hv on'``.
            All valid commands are listed in
            :const:`~hvctl.message.COMMANDS`.

        value (int or None):
            A value associated with the command, e.g. the value to
            which the voltage should be set.
            This should be left to ``None`` when sending getter
            or status commands.
            For current and voltage, *value* ranges between ``0``
            and :const:`~hvctl.config.INT_MAX`; the actual voltage or
            current value in V or mA can be computed by
            multiplying *value* with :const:`~hvctl.config.DELTA_U`
            or :const:`~hvctl.config.DELTA_I`.

        is_answer (bool):
            Determines whether *self* represents a message to the
            HV generator or a response from it.
    """

    ENCODING = 'UTF-8'
    """The encoding used for conversions between strings and
    :class:`bytes` objects.
    """

    def __init__(self, command, value=None, is_answer=False):
        """Create a new message and set its attributes to the values
        given as arguments.
        """
        try:
            self.pattern = _COMMAND_TO_PATTERN[command]
        except KeyError:
            raise ValueError(f'invalid command: {command}')

        self.command = command
        self.is_answer = is_answer
        self.check_value = self._get_check_value(command)
        self.value = value

    @classmethod
    def from_bytes(cls, bytes_, is_answer=True):
        """Create a new message from a bytes object received through
        the serial connection.
        """
        string = bytes_.decode(cls.ENCODING)
        try:
            command, value = cls._pattern_match(string)
        except ValueError:
            raise ValueError(f'invalid bytes_: {bytes_} (={repr(string)})')

        return cls(command, value, is_answer=is_answer)

    @classmethod
    def _pattern_match(cls, string):
        """Return the command and value encoded in *string*."""
        for pattern, command in _PATTERN_TO_COMMAND.items():
            fullpattern = '^' + pattern.format('([0-9]*)') + '$'
            match = re.fullmatch(fullpattern, string)
            if not match:
                continue

            string = match.group(1)
            value = int(string) if string else None
            return command, value

        raise ValueError(f'invalid string: {string}')

    def __bytes__(self):
        """Convert *self* to a :class:`bytes` object, which can then be
        sent to the HV generator through the serial connection.
        """
        value = int(self.value) if self.value is not None else ''
        string = self.pattern.format(value)
        return string.encode(self.ENCODING)

    def __repr__(self):
        """Return a string with the format
        ``'ClassName(command=<command>, value=<value>,
        is_answer=<value>)'``.
        """
        return (f'{type(self).__name__}('
                f'command={repr(self.command)}, '
                f'value={self.value}, '
                f'is_answer={self.is_answer})')

    @property
    def value(self):
        """Get or set :attr:`value`.

        Raises:
            ValueError: If an attempt is made to set an invalid
                :attr:`value`.
                The range of valid values depends on :attr:`command`.
        """
        return self._value

    @value.setter
    def value(self, value):
        self.check_value(value)
        self._value = value

    def _get_check_value(self, command):
        """Return a appropriate value checker method based
        *command*."""

        if command in ['set voltage', 'set current']:
            return self._check_setter_value
        if command in ['get voltage', 'get current']:
            return self._check_getter_value
        if command in ['hv on', 'hv off', 'set mode', 'set inhibit']:
            return self._check_parameter_value
        if command == 'get status':
            return self._check_status_value
        raise ValueError('invalid command: {command}')

    @staticmethod
    def _check_setter_value(value):
        """Make sure *value* is a valid :attr:`value` for a
        setter command.

        Raises:
            ValueError: If this is not the case.
        """

        values = range(config.INT_MAX + 1)
        if value not in values:
            raise ValueError(f'*value* should be in {values}, was {value}')

    def _check_getter_value(self, value):
        """Make sure *value* is a valid :attr:`value` for a
        getter command.

        Raises:
            ValueError: If this is not the case.
        """

        if self.is_answer:
            self._check_setter_value(value)
            return

        if value is not None:
            raise ValueError('*value* should be None for queries, was {value}')

    @staticmethod
    def _check_parameter_value(value):
        """Make sure *value* is a valid :attr:`value` for a
        parameter-related command.

        Raises:
            ValueError: If this is not the case.
        """

        if value not in [1, 0]:
            raise ValueError(f'*value* should be 1 or 0, not {value}')

    def _check_status_value(self, value):
        """Make sure *value* is a valid :attr:`value` for the
        status command.

        Raises:
            ValueError: If this is not the case.
        """

        if self.is_answer:
            values = range(256)
            if value not in values:
                raise ValueError(f'*value* should be in {values}, was {value}')
        else:
            if value is not None:
                raise ValueError(
                    f'*value* should be None for queries, was {value}')
