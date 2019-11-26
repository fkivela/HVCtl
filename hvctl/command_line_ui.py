"""This module defines a simple command-line user interface for
HVCtl.
"""

import ast
import inspect
# Importing readline adds command editing etc. to the input function.
import readline  # pylint: disable=unused-import
import sys
import textwrap

from . import api


class CommandLineUI:
    """A simple command-line UI.

    Instances of this class should be closed after they are no longer
    needed by calling :meth:`api.halt() <hvctl.api.API.halt()>` or
    using a ``with`` block. Otherwise the parallel thread created by
    :attr:`api` may continue to run in the background and consume
    resources.
    
    This class contains several methods with names following the pattern
    ``cmd_<command>``.
    These methods correspond to the commands a user can give to the
    UI: when the command string ``'command'`` is entered, the method
    ``cmd_command`` is called.
    Because messages printed by the ``help`` command use the
    docstrings of these methods in an unaltered form, the docstrings
    are written in plain text and cannot contain any reStructuredText
    syntax that isn't easily readable by humans.

    Attributes:
        inputfile:
            A file-like object for receiving input.

        outputfile:
            A file-like object for writing output.

        debug (bool):
            Setting this to ``True`` activates the debug mode;
            the default value is ``False``.
            See :meth:`cmd_debug` for details.

        api:
            An :class:`~hvctl.api.API` object used for sending commands
            to the HV generator.

        intro:
            A string displayed to the user upon starting the UI.
            The default value is ``"Welcome to HVCtl! Type 'help'
            for a list of commands."``.

        prompt:
            A string displayed to the user every time the UI
            requests input. The default value is ``'>> '``.

        indent:
            Class attribute.
            A string used to indent text blocks.
            The default value is ``'    '`` (four spaces).

        cmds_and_aliases:
            Class attribute.
            A list of tuples, where index 0 of each tuple contains
            the name of a command accepted by the UI and index 1
            contains a list of aliases for that command.
            It has the following value:
            ::

                [
                    ('getvoltage', ['getu']),
                    ('getcurrent', ['geti']),
                    ('setvoltage', ['setu']),
                    ('setcurrent', ['seti']),
                    ('hvon'      , []),
                    ('hvoff'     , []),
                    ('mode'      , []),
                    ('inhibit'   , ['i']),
                    ('status'    , ['s']),
                    ('fullstatus', ['fs']),
                    ('exit'      , ['e', 'q', 'x']),
                    ('help'      , ['h']),
                    ('debug'     , ['d']),
                ]
    """

    indent = '    '

    # pylint: disable=bad-whitespace
    cmds_and_aliases = [
        ('getvoltage', ['getu']),
        ('getcurrent', ['geti']),
        ('setvoltage', ['setu']),
        ('setcurrent', ['seti']),
        ('hvon'      , []),
        ('hvoff'     , []),
        ('mode'      , []),
        ('inhibit'   , ['i']),
        ('status'    , ['s']),
        ('fullstatus', ['fs']),
        ('exit'      , ['e', 'q', 'x']),
        ('help'      , ['h']),
        ('debug'     , ['d']),
    ]
    # pylint: enable=bad-whitespace

    def __init__(self, port=None, inputfile=None, outputfile=None):
        """Initialize a new CommandLineUI.

        Args:
            port:
                This is passed to the initializer of :attr:`api`.
            inputfile:
                The value of :attr:`inputfile`.
                If this is ``None``, the value is :data:`sys.stdin`.
            outputfile:
                The value of :attr:`outputfile`.
                If this is ``None``, the value is :data:`sys.stdout`.
        """
        if inputfile:
            self.inputfile = inputfile
        else:
            self.inputfile = sys.stdin

        if outputfile:
            self.outputfile = outputfile
        else:
            self.outputfile = sys.stdout

        # Replacing sys.stdin and sys.stdout would be simpler, but
        # could lead to unintended consequences, and would e.g.
        # prevent using multiple CommandLineUIs at once.

        self.api = api.API(port=port)
        self.debug = False
        self.intro = "Welcome to HVCtl! Type 'help' for a list of commands."
        self.prompt = '>> '

    def __enter__(self):
        """Called upon entering a ``with`` block; returns *self*."""
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Called upon exiting a ``with`` block;
        calls :meth:`api.halt() <hvctl.api.API.halt()>`.

        The arguments are ignored.
        """
        self.api.halt()

    def run(self):
        """Start the UI.

        This functions runs the following algorithm:

        1. Print :attr:`prompt` and wait for user input.
        2. Parse the input string into a command and its arguments by
           splitting it at whitespace.
        3. Call a method with the name ``cmd_<the given command>``.
           The method will execute the command and print its output.
           If no method with that name exists, print an error message
           and start again from step 1.
        4. If the method returned ``True``, break the loop.
           Otherwise, start another iteration from step 1.
        """
        self.print(self.intro)

        stop = False
        while not stop:
            string = self.input(self.prompt)
            stop = self._run_command(string)

    # Don't use reStructuredText in command docstrings, since they are
    # displayed to the user unaltered.

    def cmd_getvoltage(self):
        """Get the voltage (in V)."""
        voltage = self.api.get_voltage()
        self.print(f'The voltage is {voltage} V')

    def cmd_getcurrent(self):
        """Get the current (in mA)."""
        current = self.api.get_current()
        self.print(f'The current is {current} mA')

    def cmd_setvoltage(self, value):
        """Set the voltage to *value* (in V)."""
        voltage = self.api.set_voltage(value)
        self.print(f'Voltage set to {voltage} V')

    def cmd_setcurrent(self, value):
        """Set the current to *value* (in mA)."""
        current = self.api.set_current(value)
        self.print(f'Current set to {current} mA')

    def cmd_hvon(self):
        """Turn the HV generator on."""
        self.api.hv_on()
        self.print('HV turned on')

    def cmd_hvoff(self):
        """Turn the HV generator off."""
        self.api.hv_off()
        self.print('HV turned off')

    def cmd_mode(self, value):
        """Set the HV generator to remote or local mode.

        Set *value* to 'local', 'l' or 1 for local mode,
        or 'remote', 'r' or 0 for remote mode.
        """
        self.api.set_mode(value)
        if value in ['local', 'l']:
            self.print('Local mode activated')
        else:
            self.print('Remote mode activated')

    def cmd_inhibit(self, value):
        """Activate or deactivate inhibition.

        If bool(value) evaluates to True, inhibition is
        activated; otherwise it is deactivated.
        """
        self.api.set_inhibit(value)
        if value:
            self.print('HV inhibition activated')
        else:
            self.print('HV inhibition deactivated')

    def cmd_status(self):
        """Get the status of the HV generator
        (excluding voltage and current).
        """
        statusdict = self.api.get_status()
        string = self._status_str(statusdict)
        self.print('Status:\n' + textwrap.indent(string, self.indent))

    def cmd_fullstatus(self):
        """Get the full status of the HV generator,
        including voltage and current.
        """
        statusdict = self.api.full_status()
        string = (f"Voltage: {statusdict['voltage']}\n"
                  f"Current: {statusdict['current']}\n"
                  + self._status_str(statusdict))
        self.print('Status:\n' + textwrap.indent(string, self.indent))

    @staticmethod
    def _status_str(statusdict):
        """Return a formatted string displaying the data returned
        by API.get_status.
        """
        return '\n'.join([
            f'Regulation mode: {statusdict["regulation"]}',
            f'HV power: {"on" if statusdict["hv_on_status"] else "off"}',
            f'HV on command given: {statusdict["hv_on_command"]}',
            f'HV off command given: {statusdict["hv_off_command"]}',
            f'Interlock: {statusdict["interlock"]}',
            ('Fault(s) present' if statusdict["fault"]
             else 'No faults present'),
        ])

    def cmd_help(self, value=None):
        """Display a help message.

        *value* should be the name or an alias of the command that
        should be described.
        If no *value* is specified, all commands are listed and
        described.
        """
        if value:
            string = self._helpstring(value)
        else:
            descriptions = []
            for name, _ in self.cmds_and_aliases:
                descriptions.append(self._helpstring(name))
            description_str = '\n\n'.join(descriptions)
            string = ('Valid commands:\n'
                      + textwrap.indent(description_str, self.indent))

        self.print(string)

    @staticmethod
    def cmd_exit():
        """Exit the UI."""
        return True

    def cmd_debug(self, value):
        """Activate or deactivate the debug mode.

        If bool(value) evaluates to True, the debug mode is activated;
        otherwise it is deactivated.

        When the debug mode is inactive, TypeErrors and ValueErrors
        raised during the execution of commands are caught to prevent
        users from crashing the program with invalid commands.
        The debug mode disables this error-catching in order to make
        debugging easier.
        """
        self.debug = bool(value)
        self.print('Debug mode '
                   + 'activated' if self.debug else 'deactivated')

    def input(self, prompt=''):
        """Ask the user for input.

        This method works like the built-in :func:`.input` function,
        but uses :attr:`inputfile` and :attr:`outputfile` instead of
        :data:`sys.stdin` and :data:`sys.stdout`.

        The line editing functionality provided by the :mod:`readline`
        module works with this method only if :attr:`inputfile` is
        :data:`sys.stdin`.
        """
        # `.input` instead of `input` makes Sphinx refer to the
        # built-in input function instead of this method.

        if self.inputfile == sys.stdin:
            return input(prompt)

        self.print(prompt, end='')
        string = self.inputfile.readline()

        if string[-1] == '\n':
            return string[:-1]

        return string

    def print(self, *objects, sep=' ', end='\n'):
        """Print text to the UI.

        This method works like the built-in :func:`.print` function,
        but uses :attr:`inputfile` and :attr:`outputfile` instead of
        :data:`sys.stdin` and :data:`sys.stdout`, and doesn't include
        the *file* and *flush* arguments.
        """
        print(*objects, file=self.outputfile, sep=sep, end=end, flush=True)

    def _run_command(self, line):
        """Parse *line* and run it as a command.

        Returns:
            True if the main loop should be broken, otherwise
            False.
        """
        # Separate the command and its arguments.
        # split() splits at any whitespace character
        # and discards empty strings.
        parts = line.split()
        try:
            cmdname = parts[0]
        except IndexError:
            # Skip empty lines.
            return False
        args = parts[1:]

        # Get the method.
        try:
            method = self._get_method(cmdname)
        except ValueError as error:
            self.print(f'Error: {error}')
            return False

        # Parse the arguments into appropriate Python objects.
        # Arguments that cannot be parsed into any other type are kept
        # as strings.
        for i, arg in enumerate(args):
            try:
                args[i] = ast.literal_eval(arg)
            except ValueError:
                pass

        # Call the method.
        try:
            return method(*args)
        except (ValueError, TypeError) as error:

            if self.debug:
                raise error

            if isinstance(error, ValueError):
                self.print(f'Error: {error}')
            else:
                self.print('Error: invalid argument type or number of '
                           'arguments')
            return False

    def _get_method(self, command):
        """Return the method corresponding to *command* (a str)."""

        names = [command] + self._get_aliases(command)
        for name in names:
            try:
                return getattr(self, 'cmd_' + name)
            except AttributeError:
                pass

        raise ValueError(f'invalid command: {command}')

    def _get_aliases(self, command):
        """Return a list of aliases for *command*.

        *command* itself is never part of the list, but if *command*
        is itself an alias, the primary name of the command will be
        included in the list.
        """
        for cmd, aliases in self.cmds_and_aliases:
            names = [cmd] + aliases
            if command in names:
                names.remove(command)
                return names

        raise ValueError(f'invalid command: {command}')

    def _helpstring(self, cmdname):
        """Return a help message describing the usage of *cmdname*."""
        method = self._get_method(cmdname)
        argstr = self._argstring(method)
        aliasstr = self._alias_string(cmdname)
        docstr = inspect.getdoc(method)
        if docstr is None:
            docstr = ''

        return (f'{cmdname} {argstr}\n'
                + textwrap.indent(docstr, self.indent)
                + ('\n\n' + textwrap.indent(aliasstr, self.indent) if aliasstr
                   else '')
                )

    def _alias_string(self, command):
        """Return a formatted string that lists the aliases of
        "*command*.

        Returns:
            A string with the format 'Aliases: a, b, c',
            or '' if there are no aliases.
        """
        aliases = self._get_aliases(command)
        if aliases:
            return 'Aliases: ' + ', '.join(aliases)
        return ''

    @staticmethod
    def _argstring(method):
        """Return a formatted string that lists the arguments of
        *command*.

        Format: '<arg1> [optional_arg2=default]'
        """
        argspec = inspect.getfullargspec(method)
        args = argspec.args[1:]  # Ignore *self*.
        defaults = argspec.defaults  # Default values for arguments.
        if defaults is None:
            defaults = []

        reversed_args = args[::-1]
        reversed_defaults = defaults[::-1]
        reversed_argstrings = [None] * len(args)

        # The lists are reversed, so that arguments with default
        # values are iterated first.
        # Arguments without default values are iterated afterwards,
        # when *reversed_defaults* has run out of indices.
        for i, arg in enumerate(reversed_args):
            try:
                default = reversed_defaults[i]
                reversed_argstrings[i] = f'[{arg}={default}]'
            except IndexError:
                reversed_argstrings[i] = f'<{arg}>'

        return ' '.join(reversed_argstrings[::-1])
