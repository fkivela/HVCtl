"""This module defines a simple command-line UI for HVCtl."""

import ast
import inspect
# Importing readline adds command editing etc. to the input function.
import readline
import sys
import textwrap

from . import api
from . import config

class CommandLineUI:
    """A simple command-line UI.
    
    Attributes:
        inputfile: 
            A file object for receiving input.
        
        outputfile: 
            A file object for writing output.
        
        debug (bool):
            Setting this to True enables a debug mode; the default 
            value is ``False``.
            See :meth:`cmd_debug` for details.
        
        api:
            An :class:`~hvctl.api.API` object used to send commands '
            'to the HV PSU.                    
    """
    
    intro = "Welcome to HVCtl! Type 'help' for a list of commands."
    """Class attribute.
    A string displayed to the user upon starting the UI.
    """
    prompt = '>> '
    """Class attribute.
    A string displayed to the user every time the UI requests input.
    """
    indent = '    '
    """Class attribute.
    A string used to indent text blocks.
    """
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
    """Class attribute.
    A list of two-index tuples.
    The first index is of each tuple is the primary name of a command 
    accepted by the UI,
    and the second is a list of aliases for that command.
    """
    
    def __init__(self, serial_kwargs=None, inputfile=None, outputfile=None):
        """Initialize a new CommandLineUI.
        
        Args:
            serial_kwargs:
                A dict of keyword arguments for forming a serial 
                connection, passed to the initializer of :attr:`api`.
                If this is ``None``, 
                :attr:`~hvctl.config.SERIAL_KWARGS` is used.
            inputfile:
                The value of :attr:`inputfile`.
                If this is ``None``, the value is :attr:`sys.stdin`.
            outputfile:
                The value of :attr:`outputfile`.
                If this is ``None``, the value is :attr:`sys.stdin`.
        """
                
        if inputfile:
            self.inputfile = inputfile
        else:
            self.inputfile = sys.stdin
            
        if outputfile:
            self.outputfile = outputfile
        else:
            self.outputfile = sys.stdout
            
        if not serial_kwargs:
            serial_kwargs = config.SERIAL_KWARGS
        
        self.debug = False
        self.api = api.API(serial_kwargs=config.SERIAL_KWARGS, 
                           poll=True, 
        )

    # Don't use reStructuredText in command docstrings, since they are 
    # displayed to the user unaltered.
    def cmd_getvoltage(self):
        """Get HV voltage (in V)."""
        voltage = self.api.get_voltage()
        self.print(f'The voltage is {voltage} V')
    
    def cmd_getcurrent(self):
        """Get HV current (in mA)."""
        current = self.api.get_current()
        self.print(f'The current is {current} mA')
        
    def cmd_setvoltage(self, value):
        """Set HV voltage to *value* (in V)."""
        voltage = self.api.set_voltage(value)
        self.print(f'Voltage set to {voltage} V')
    
    def cmd_setcurrent(self, value):
        """Set HV current to *value* (in mA)."""
        current = self.api.set_current(value)
        self.print(f'Current set to {current} mA')

    def cmd_hvon(self, value):
        """Turn the HV on."""
        self.api.HV_on()
        self.print('HV turned on')
        
    def cmd_hvoff(self, value):
        """Turn the HV off."""
        self.api.HV_on()
        self.print('HV turned off')

    def cmd_mode(self, value):
        """Set the HV to remote or local mode.
        
        Set *value* to 'local', 'l' or 1 for local mode, or
        'remote', 'r' or 0 for remote mode.
        """
        self.api.set_mode(value)
        if value in ['local', 'l']: 
            self.print('Local mode activated')
        else:
            self.print('Remote mode activated')

    def cmd_inhibit(self, value):
        """Activate or deactivate HV inhibition.
        
        If bool(value) evaluates to ``True``, inhibition is activated; 
        otherwise it is deactivated."""
        self.api.set_inhibit(value)    
        if value:
            self.print('HV inhibition activated')
        else:
            self.print('HV inhibition deactivated')
                
    def cmd_status(self):
        """Get HV status (excluding voltage and current)."""
        
        statusdict = self.api.get_status()
        string = self._status_str(statusdict)
        self.print('Status:\n' + textwrap.indent(string, self.indent))
        
    def cmd_fullstatus(self):
        """Get full HV status including voltage and current."""
        
        statusdict = self.api.full_status()
        string = (f"Voltage: {statusdict['voltage']}\n"
                  f"Current: {statusdict['current']}\n"
                  + self._status_str(statusdict)
                 ) 
        self.print('Status:\n' + textwrap.indent(string, self.indent))
        
    def _status_str(self, statusdict):
        """Return a formatted string displaying the data returned 
        by API.get_status.
        """
        return '\n'.join([
            f'Regulation mode: {statusdict["regulation"]}',
            f'HV power: {"on" if statusdict["HV_on_status"] else "off"}',
            f'HV on command given: {statusdict["HV_on_command"]}',
            f'HV off command given: {statusdict["HV_off_command"]}',
            f'Interlock: {statusdict["interlock"]}',
            ('Fault(s) present' if statusdict["fault"] 
                                else 'No faults present'),        
        ])
        
    def cmd_help(self, value=None):
        """Disply a help message. 
        
        *value* should be the name or alias of a command that should
        be described. If no *value* is specified, all commands are 
        listed and described. 
        """
        if value: 
            string = self._helpstring(value)
        else:
            descriptions = []
            for name, _ in self.cmds_and_aliases:
                descriptions.append(self._helpstring(name))
            description_str = '\n\n'.join(descriptions)
            string = ('Valid commands:\n' + 
                      textwrap.indent(description_str, self.indent))
                    
        self.print(string)
                
    def cmd_exit(self):
        """Exit the UI."""
        return True
    
    def cmd_debug(self, value):
        """Activate or deactivate debug mode.
        
        If bool(value) evaluates to True, debug mode is activated; 
        otherwise it is deactivated.
        
        When debug mode is inactive, TypeErrors and ValueErrors raised 
        during the execution of commands are caught to prevent users 
        from crashing the program with invalid commands.
        In debug mode, this functionality is disabled to make 
        debugging easier.
        """
        self.debug = bool(value)
        self.print('Debug mode ' + 
                   'activated' if self.debug else 'deactivated')
    
    def input(self, prompt=''):
        """Ask the user for input.
        
        This method works like the built-in :func:`.input` function, 
        but uses :attr:`inputfile` and :attr:`outputfile` instead of 
        :attr:`sys.stdin` and :attr:`sys.stdout`.
        """
        # `.input` instead of `input` makes Sphinx refer to the 
        # built-in input instead of this method.
        self.print(prompt, end='')
        string = self.inputfile.readline()
        
        if string[-1] == '\n':
            return string[:-1]
        else:
            return string

    def print(self, *objects, sep=' ', end='\n'):
        """Print text to the UI.
        
        This method works like the built-in :func:`.print` function, 
        but uses :attr:`inputfile` and :attr:`outputfile` instead of 
        :attr:`sys.stdin` and :attr:`sys.stdout`, and doesn't include 
        the *file* argument.
        """
        print(*objects, file=self.outputfile, sep=sep, end=end, flush=True)
                        
    def run(self):
        """Start the UI."""
        with self.api:
            self.api.run()
            self.print(self.intro)

            stop = False
            while not stop:
                string = self.input(self.prompt)
                stop = self._run_command(string)
        
    def _run_command(self, line):
        """Parse *line* and run it as a command."""
        # Separate the command and its arguments.
        parts = [x for x in line.split(' ') if x]
        try:
            cmdname = parts[0]
        except IndexError:
            # Skip empty lines.
            return
        args = parts[1:]
        
        # Get the method.
        try:
            method = self._get_method(cmdname)
        except ValueError as e:
            self.print(f'Error: {e}')
            return
        
        # Parse the arguments into appropriate Python 
        # objects.
        # Arguments that cannot be parsed into other types are kept 
        # as strings.
        for i, arg in enumerate(args):
            try:
                args[i] = ast.literal_eval(arg)
            except ValueError:
                pass
        
        # Call the method.
        try:
            return method(*args)
        except (ValueError, TypeError) as e:
            
            if self.debug:
                raise e
            
            if isinstance(e, ValueError):
                self.print(f'Error: {e}')
            else:
                self.print('Error: invalid argument type or number of '
                           'arguments')
                
    def _get_method(self, command):
        """Return the method matching the string *command*."""
        
        names = [command] + self._get_aliases(command)
        for name in names:
            try:
                return getattr(self, 'cmd_' + name)
            except AttributeError:
                pass
        
        raise ValueError(f'invalid command: {command}')
        
    def _get_aliases(self, command):
        """Return a list of aliases of the string *command*.
        
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
        """Return a help message describing the usage of *command*."""
        method = self._get_method(cmdname)        
        argstr = self._argstring(method)
        aliasstr = self._alias_string(cmdname)
        docstr = inspect.getdoc(method) 
        if docstr == None:
            docstr = ''
        
        return (f'{cmdname} {argstr}\n'
                + textwrap.indent(docstr, self.indent)
                + ('\n\n' + textwrap.indent(aliasstr, self.indent) if aliasstr 
                                                                   else '')
                )

    def _alias_string(self, command):
        """Return a formatted string that lists the aliases of 
        "*command*.
        
        Format: 'Aliases: a, b, c' or '', if there are no aliases.
        """
        aliases = self._get_aliases(command)
        if aliases:
            return 'Aliases: ' + ', '.join(aliases)
        else:
            return ''
        
    def _argstring(self, method):
        """Return a formatted string that lists the arguments of 
        *command*.
        
        Format: '<arg1> [optional_arg2=default]'
        """
        argspec = inspect.getfullargspec(method)
        args = argspec.args[1:] # Ignore *self*.
        defaults = argspec.defaults
        if defaults == None:
            defaults = []
        
        reversed_args = args[::-1]
        reversed_defaults = defaults[::-1]
        reversed_argstrings = [None] * len(args)
        
        for i, arg in enumerate(reversed_args):
            try:
                default = reversed_defaults[i]
                reversed_argstrings[i] = f'[{arg}={default}]'
            except IndexError:
                reversed_argstrings[i] = f'<{arg}>'
        
        return ' '.join(reversed_argstrings[::-1])