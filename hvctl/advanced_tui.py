"""This module defines the AdvancedTUI class.

This module uses `urwid <http://urwid.org/>`_.
If urwid isn't installed, 
:class:`~hvctl.command_line_ui.CommandLineUI` 
provides a UI that can be run without it.
"""
import threading
import urwid

from . import widgets        
            
class AdvancedTUI(urwid.WidgetWrap):
    """A text-based user interface combining a terminal-style 
    command line interface and a text screen.
    
    Attributes:
        display (:class:`urwid.Text`):
            A text field for presenting information to the user.
            Use :func:`display.set_text` to change its 
            contents.
        
        cli (:class:`CLI`):
            A command-line interface for issuing commands; located 
            below the display. 
    """
    
    def __init__(self, script, inputfile, outputfile):
        """Initialize a new :class:`AdvancedTUI`.
        
        Args:
            script:
                An object that should run the program controlled by 
                the TUI when called with ``script()``.
            inputfile:
                A file-like object where user input is sent.
            outputfile:
                A file-like object where :attr:`script` should print 
                its output, if it is to be printed on the screen.
        """
        self.display = urwid.Text('')
        self.cli = widgets.CLI(inputfile, outputfile)
        self._script_finished = False
        
        upper_half = self.display
        divider = urwid.Divider('─')
        lower_half = self.cli
        # 'pack' treats upper_half and divider as flow widgets and 
        # prevents the adding of padding to them. 
        screen = urwid.Pile(
                [('pack', upper_half), ('pack', divider), lower_half])
        super().__init__(screen)
        
        def run_script():
            script()
            self.cli.cmdlines.outputfile.write("PRESS 'q' TO EXIT")
            self._script_finished = True
        
        self._thread = threading.Thread(target=run_script, daemon=True)
        self._loop = urwid.MainLoop(self)
        self._loop.set_alarm_in(0.01, self._callback, user_data=None)
        
    def keypress(self, size, key):
        """Handle key presses.
        
        Pressing 'q' after the program has returned exits the 
        UI. 
        """
        if key == 'q' and self._script_finished:
            raise urwid.ExitMainLoop
        else:
            return super().keypress(size, key)
        
    def _callback(self, loop, user_data):
        """Update self.cli.cmdlines periodically so that it handles 
        new output.
        This also updates self.cli.scrollbar, since printing new 
        output may change its size or position.
        """
        self.cli.cmdlines.update()
        # _invalidate marks a widget for re-rendering.
        self.cli.scrollbar._invalidate()
        self._loop.set_alarm_in(0.01, self._callback, user_data=None)

    def run(self):
        """Start the program and the UI loop in parallel threads."""
        self._thread.start()
        self._loop.run()