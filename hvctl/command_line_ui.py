"""This module defines a simple command-line UI for HVCtl."""

# Importing readline adds command editing etc. to the input function.
import readline
import ast
import textwrap
from collections import namedtuple, OrderedDict

import tabulate

from api import API

Command = namedtuple('Command', 'names, function, args, description')    
"""A :class:`namedtuple` to represent accepted commands.

Attributes:
    names (list of strings): 
        A list of aliases the command can be called with.
    function (string): 
        The name of the method called with the command.
    args (list of strings): 
        A list of arguments accepted by the command. 
        E.g. ['x', 'y', 'z=None'].
    description:
        A description shown to the user.
"""

class CommandLineUI(API):
    """A simple command-line UI.
    
    Attributes:
        stopflag (bool): 
            A ``True`` value of this flag tells the UI 
            loop to stop.
    """
    
    prompt = '>> '
    """Class attribute. The prompt displayed before waiting for input.
    """
    start_msg = "Welcome to HVCtl! Type 'help' for a list of commands."
    """Class attribute. The message displayed when the UI is started.
    """

    commandlist = [    
        Command(
            names=['getvoltage', 'getu'],
            function='get_voltage',
            args=[],
            description=('Get voltage in V.')),            
            
        Command(
            names=['getcurrent', 'geti'],
            function='get_current',
            args=[],
            description=('Get current in mA.')),
                
        Command(
            names=['setvoltage', 'setu'],
            function='set_voltage',
            args=['value'],
            description=('Set voltage to *value* (in V).')),            
            
        Command(
            names=['setcurrent', 'seti'],
            function='set_current',
            args=['value'],
            description=('Set current to *value* (in mA).')),
                
        Command(
            names=['hvon', 'on'],
            function='HV_on',
            args=[],
            description=('Turn the HV on.')),            
            
        Command(
            names=['hvoff', 'off'],
            function='HV_off',
            args=[],
            description=('Turn the HV off.')),
                
        Command(
            names=['mode', 'm'],
            function='set_mode',
            args=['value'],
            description=(
                "value in ['local', 'l']: Set HV to local mode.\n"
                "value in ['remote', 'r']: Set HV to remote mode.")),
            
        Command(
            names=['inhibit', 'i'],
            function='set_inhibit',
            args=['value'],
            description=(
                'bool(value)=True: Activate HV inhibition.\n'
                'bool(value)=False: Deactivate HV inhibition.')),
                
        Command(
            names=['status', 's'],
            function='get_status',
            args=[],
            description=('Get HV status.')),

        Command(
            names=['halt', 't'],
            function='halt',
            args=[],
            description=('Turn off the HV and exit the program.')),

        Command(
            names=['exit', 'e', 'q', 'x'],
            function='stop',
            args=[],
            description=('Exit the program.')),
                
        Command(
            names=['help', 'h'],
            function='help',
            args=[],
            description=('Display this help message.')),
    ]    
    """Class attribute. A list of accepted commands 
    (as :class:`Command` objects).
    """
    
    commands = OrderedDict()
    """Class attribute. A dict of accepted commands, 
    with command names as keys and :class:`Command` objects as values. 
    Aliases for the same command are represented with different keys 
    mapping to the same value.
    """
    # Turn all command aliases into separate keys.
    for command in commandlist:
        for cmdname in command.names:
            commands[cmdname] = command
        
    def __init__(self, *args, **kwargs):
        """Initialize a new CommandLineUI.
        
        Args and kwargs are passed to :meth:`API.__init__`.
        """
        super().__init__(*args, **kwargs)
        self.stopflag = False
    
    def run(self):
        """Start the UI."""
        self.print(self.start_msg)
        while True:
            string = self.input(self.prompt)
            self.run_command(string)
            if self.stopflag:
                break
            
    def stop(self):
        """Stop the UI by setting :attr:`stopflag` to ``True``."""
        self.stopflag = True
        
    def halt(self, *args, **kwargs):
        """Call :meth:`API.halt` and stop the UI by setting 
        :attr:`stopflag` to ``True``.
        """
        super().halt(*args, **kwargs)
        self.stopflag = True
            
    def input(self, prompt=''):
        """Ask the user for input.
        
        Works like the built-in :func:`input` function.
        """
        self.print(prompt, end='')
        string = self.inputfile.readline()
        
        if string[-1] == '\n':
            return string[:-1]
        else:
            return string

    def print(self, *objects, sep=' ', end='\n'):
        """Print text to the UI.
        
        Works like the built-in :func:`print` function, but without 
        the *file* argument.
        """
        print(*objects, file=self.outputfile, sep=sep, end=end, flush=True)
            
    def help(self):
        """Print a help message."""
        string = 'Accepted commands:'
        description_width = 50
        
        def format_arg(arg):
            if '=' in arg:
                return f'[{arg}]'
            else:
                return f'<{arg}>' 
        
        data = []
        headers = ['Command', 'Aliases', 'Args', 'Description']
        for command in self.commandlist:       
            name = command.names[0]
            aliases = ', '.join(command.names[1:])
            args = ' '.join([format_arg(arg) for arg in command.args])
            description = '\n'.join(textwrap.wrap(command.description, 
                                                  description_width))
            data.append([name, aliases, args, description])
    
        table = tabulate.tabulate(data, headers=headers, tablefmt='simple')
        return string + '\n' + textwrap.indent(table, '  ')
        
    def run_command(self, line):
        """Parse *line* and run it as a command."""
        # Separate the command and its arguments.
        parts = [x for x in line.split(' ') if x]
        try:
            cmdname = parts[0]
        except IndexError:
            # Skip empty lines.
            return
        args = parts[1:]
        
        # Find the method matching the command.
        try:
            funcname = self.commands[cmdname].function
        except KeyError:
            self.print(f'Error: invalid command: {cmdname}')
            return
        func = getattr(self, funcname)
        
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
            ret = func(*args)
        except ValueError as e:
            self.print(f'Error: {e}')
            return
        except TypeError:
            self.print('Error: invalid argument type or number of arguments')
            return
                
        # If there is a return value, print it.
        if ret != None:
            self.print(ret)