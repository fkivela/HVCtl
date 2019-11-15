#!/usr/bin/env python3
"""This is the main script used to run HVCtl."""

import argparse

from hvctl.command_line_ui import CommandLineUI
from hvctl.config import SERIAL_KWARGS
from hvctl.queuefile import QueueFile
from hvctl.virtualhv import VirtualHV

### Command line arguments ###

# The argparse module hepls with parsing command line arguments.
# The -h option displays an automatically generated help message.
parser = argparse.ArgumentParser(description='This script runs HVCtl')

# Some options.
parser.add_argument('-v', '--virtual', help='use a virtual HV PSU',
                    action='store_true')
parser.add_argument('-s', '--simple', help='use a simple command-line UI',
                    action='store_true')

args = parser.parse_args()

### The main part of the script ###

try:
    # If the "--virtual" command line argument is supplied,
    # use a virtual HV.
    if args.virtual:
        virtualhv = VirtualHV()
        port = virtualhv.connection.port
    else:
        port = SERIAL_KWARGS['port']

    # If the "-simple" command line argument is specified,
    # AdvancedTUI is not imported.
    # This makes it possible to run the program without installing
    # urwid.
    if args.simple:
        clui = CommandLineUI(port=port)
        clui.run()
    else:
        from hvctl.advanced_tui import AdvancedTUI

        # Connect the program and the UI with *inputfile* and
        # *outputfile*.
        inputfile = QueueFile(block=True)
        outputfile = QueueFile()

        # Create an AdvancedTUI that wraps a CommandLineUI.
        clui = CommandLineUI(port, inputfile, outputfile)
        adv_ui = AdvancedTUI(clui.run, inputfile, outputfile)

        # Show HV status in the UI.
        status = clui.api.status
        status.callback = lambda: adv_ui.display.set_text(str(status))

        adv_ui.run()

finally:

    # Close the serial connection and stop the parallel thread
    # used for polling.
    try:
        clui.api.halt()
    except NameError:
        # An error may be raised before the name clui is defined.
        pass

    # Close the virtual connection, if it was used.
    try:
        virtualhv.connection.close()
    except NameError:
        pass
