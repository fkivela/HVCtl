#!/usr/bin/env python3
"""This is the main script used to run HVCtl."""

import argparse
import sys

from hvctl import config, display
from hvctl.command_line_ui import CommandLineUI
from hvctl.queuefile import QueueFile
from hvctl.virtualhv import VirtualHV
# Be careful not to import config as 'import config'.
# Because this is a script which won't be imported, 'import config'
# would also work instead of 'from hvctl import config'.
# However, this would cause config to be loaded twice as different
# module objects: config (by this script) and hvctl.config
# (by imported modules).
# Changing the constants in config would then affect 
# only this script, not imported modules.

### Command line arguments ###

# The argparse module helps with parsing command line arguments.
# The -h option displays an automatically generated help message.
parser = argparse.ArgumentParser(description='This script runs HVCtl.')

# Some options.
# Help strings are written in lower case and without periods to
# match the help string automatically created for the -h option. 

parser.add_argument(
    '-c', '--config',
    help='specify a configuration file',
    nargs='?', default=None)

port_options = parser.add_mutually_exclusive_group()

port_options.add_argument(
    '-p', '--port',
    help='specify a port',
    nargs='?', default=None)

port_options.add_argument(
    '-v', '--virtual', 
    help='use a virtual HV generator', 
    action='store_true')

parser.add_argument(
    '-s', '--simple',
    help="use a UI that doesn't require urwid.",
    action='store_true')

parser.add_argument(
    '-n', '--no-poll',
    help='disable automatic polling',
    action='store_true')

args = parser.parse_args()

# If a non-default configuration file is specified, all configuration
# constants are re-loaded from that file.
# This is done before the main part of the script to make sure all
# parts of the program use the new values of the constants.
if args.config:
    config.load(args.config)


### The main part of the script ###

def main(args):
    """Execute the script with the command-line arguments given in
    *args*.
    """
    try:
        # If virtualhv was defined in another function
        # and an error occurred between its creation and the
        # 'return virtualhv' statement, 
        # the finally block wouldn't work, because 'virtualhv' wouldn't
        # be included in the namespace of main().
        # This also holds for command_line_ui. Because of this,
        # both objects are defined directly in main(). 

        virtualhv = VirtualHV() if args.virtual else None
        port = get_port(args, virtualhv)
        
        poll = not args.no_poll
        inputfile, outputfile = get_io_files(args)
        command_line_ui = CommandLineUI(port, poll, inputfile, outputfile)
        
        ui = get_ui(command_line_ui)
        ui.run()
    finally:
        # Make sure all parallel threads are closed.

        try:
            # This raises a NameError if the script raises an error
            # before command_line_ui is defined.
            command_line_ui.api.halt()
        except NameError:
            pass
    
        try:
            # An AttributeError is raised if virtualhv is None. 
            virtualhv.connection.close()
        except AttributeError:
            pass


def get_port(args, virtualhv):
    """Return the port used for the serial connection.
    
    If a virtual HV isn't used, the *virtualhv* argument is ignored.
    """
    if args.virtual:
        port = virtualhv.connection.port
    elif args.port:
        port = args.port
    else:
        port = config.SERIAL_KWARGS['port']
        
    return port


def get_io_files(args):
    """Return the input and output files for the UI.
    
    Returns:
        (inputfile, ouptufile)
    """
    if args.simple:
        inputfile = sys.stdin
        outputfile = sys.stdout
    else:
        inputfile = QueueFile(block=True)
        outputfile = QueueFile()

    return inputfile, outputfile    


def get_ui(command_line_ui):
    """Return *command_line_ui* or an AdvancedUI object that uses
    *command_line_ui*.
    """
    if args.simple:
        ui = command_line_ui
    else:
        # Because AdvancedTUI imports urwid, it is imported only if
        # it is needed.
        # This makes it possible to run HVCtl without urwid by using
        # CommandLineUI.
        from hvctl.advanced_tui import AdvancedTUI
        advanced_ui = AdvancedTUI(command_line_ui.run, 
                                  command_line_ui.inputfile, 
                                  command_line_ui.outputfile,
                                  display.palette)
        
        # Show the status of the HV generator in the UI.
        def callback(status):
            text = display.generate_text(status)
            advanced_ui.display.set_text(text)
        command_line_ui.api.status.callback = callback
        ui = advanced_ui

    return ui


main(args)