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
    'set inhibition': 'P8,{}\r',
    'get status' : 'E{}\r'
}

_PATTERN_TO_COMMAND = {p: c for c, p
                       in _COMMAND_TO_PATTERN.items()}


class Message():
    """This class represents a message sent to or received from the HV
    generator.

    All of the following attributes are defined as read-only
    properties to prevent changing them after an object is instantiated.

    Attributes:
        command (string):
            The command that is sent to the HV generator,
            or the command to which this object is an answer.
            The following values are accepted:

                | ``'set voltage'``
                | ``'set current'``
                | ``'get voltage'``
                | ``'get current'``
                | ``'hv on'``
                | ``'hv off'``
                | ``'set mode'``
                | ``'set inhibition'``
                | ``'get status'``

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
        """Create a new :class:`Message` and set its attributes
        to the values given as arguments.

        Raises:
            ValueError:
                If *command* is not recognized or *value* is not valid.
        """
        try:
            self._pattern = _COMMAND_TO_PATTERN[command]
        except KeyError:
            raise ValueError(f'invalid command: {command}')

        self._command = command
        self._value = value
        self._is_answer = is_answer

        self._check_value()

    # pylint: disable=missing-function-docstring
    # These are documented in the class docstring.
    @property
    def command(self):
        return self._command

    @property
    def value(self):
        return self._value

    @property
    def is_answer(self):
        return self._is_answer
    # pylint: enable=missing-function-docstring

    @classmethod
    def from_bytes(cls, bytes_, is_answer=True):
        """Create a new :class:`Message` from a :class:`bytes`
        object received through the serial connection.
        """
        string = bytes_.decode(cls.ENCODING)
        try:
            command, value = cls._pattern_match(string)
        except ValueError:
            raise ValueError(f'invalid bytes_: {bytes_} (={repr(string)})')

        return cls(command, value, is_answer=is_answer)

    @classmethod
    def _pattern_match(cls, string):
        """Return the command and value encoded in *string*.

        Args:
            string:
                A string in the format used by the HV generator for
                communication; e.g. 'd1,1000\r'.

        Returns:
            A tuple containing a command string and a value;
            e.g. ('set voltage', 100)
        """
        for pattern, command in _PATTERN_TO_COMMAND.items():
            regexp = '^' + pattern.format('([0-9]*)') + '$'
            match = re.fullmatch(regexp, string)
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
        if self.value is None:
            format_value = ''
        else:
            format_value = int(self.value)
            # Convert to int, since *value* can be a boolean.
        string = self._pattern.format(format_value)
        return string.encode(self.ENCODING)

    def __repr__(self):
        """Return a string with the format
        ``'ClassName(command=<command>, value=<value>,
        is_answer=<is_answer>)'``.
        """
        return (f'{type(self).__name__}('
                f'command={repr(self.command)}, '
                f'value={self.value}, '
                f'is_answer={self.is_answer})')

    def _check_value(self):
        """Raise a ValueError if self.value is invalid."""

        if self.command in ['set voltage', 'set current']:
            self._check_setter_value()

        elif self.command in ['get voltage', 'get current']:
            self._check_getter_value()

        elif self.command in ['hv on', 'hv off', 'set mode', 'set inhibition']:
            self._check_parameter_value()

        elif self.command == 'get status':
            self._check_status_value()

        else:
            raise ValueError('invalid command: {self.command}')

    def _check_setter_value(self):
        """Make sure self.value a valid value for a setter command.

        Raises:
            ValueError: If this is not the case.
        """
        values = range(config.INT_MAX + 1)
        if self.value not in values:
            raise ValueError(
                f'self.value should be in {values}, was {self.value}')

    def _check_getter_value(self):
        """Make sure self.value is a valid value for a getter command.

        Raises:
            ValueError: If this is not the case.
        """
        if self.is_answer:
            self._check_setter_value()
            return

        if self.value is not None:
            raise ValueError(
                'self.value should be None, was {self.value}')

    def _check_parameter_value(self):
        """Make sure self.value is a valid value for a
        parameter-related command.

        Raises:
            ValueError: If this is not the case.
        """
        if self.value not in [1, 0]:
            raise ValueError(
                f'self.value should be 1 or 0, not {self.value}')

    def _check_status_value(self):
        """Make sure self.value is a valid value for the status
        command.

        Raises:
            ValueError: If this is not the case.
        """
        if self.is_answer:
            values = range(256)
            if self.value not in values:
                raise ValueError(
                    f'self.value should be in {values}, was {self.value}')
        else:
            if self.value is not None:
                raise ValueError(
                    f'self.value should be None, was {self.value}')
