"""This module defines the :class:`AdvancedTUI` class.

:class:`AdvancedTUI` uses `urwid <http://urwid.org/>`_.
If urwid hasn't been installed,
:class:`~hvctl.command_line_ui.CommandLineUI` should be used instead.
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
            Use :meth:`display.set_text() <urwid.Text.set_text>` to
            change its contents.

        command_line_interface(:class:`~hvctl.widgets.ScrollableCommandLines`):
            A command-line interface for issuing commands, located
            below :attr:`display`.
    """

    def __init__(self, script, inputfile, outputfile):
        """Initialize a new :class:`AdvancedTUI`.

        Args:
            script:
                The program that this UI controls.
                It should be wrapped in a callable object so that
                calling ``script()`` executes it.
                The UI communicates with the program through
                *inputfile* and *outputfile*;
                the program should read its input from *inputfile*
                and send its output to *outputfile*.
            inputfile (file-like object):
                User input entered into the UI is written into this
                object.
            outputfile (file-like object):
                Output printed on the screen by the UI is read from
                this object.
        """
        self.display = urwid.Text('')
        self.command_line_interface = widgets.ScrollableCommandLines(
            inputfile, outputfile)
        self._script_finished = False

        upper_half = self.display
        divider = urwid.Divider('─')
        lower_half = self.command_line_interface
        # 'pack' treats upper_half and divider as flow widgets and
        # prevents the adding of padding to them.
        screen = urwid.Pile(
            [('pack', upper_half), ('pack', divider), lower_half])
        super().__init__(screen)

        def run_script():
            script()
            self.command_line_interface.command_lines.outputfile.write(
                "PRESS 'q' TO EXIT")
            self._script_finished = True

        self._thread = threading.Thread(target=run_script, daemon=True)
        self._loop = urwid.MainLoop(self)
        self._loop.set_alarm_in(0.01, self._callback, user_data=None)

    def keypress(self, size, key):
        """Handle key presses.

        Pressing 'q' after the program has finished its execution
        breaks the UI loop.
        """
        if key == 'q' and self._script_finished:
            raise urwid.ExitMainLoop

        return super().keypress(size, key)

    def _callback(self, loop, user_data):
        """Update self.command_line_interface.command_lines
        periodically so that it handles new output.
        This also updates self.command_line_interface.scrollbar,
        since printing new output may change its size or position.
        """
        self.command_line_interface.command_lines.update()
        
        # _invalidate marks a widget for re-rendering.
        # urwid documentation suggests using this method even though
        # it begins with '_'.
        # pylint: disable=protected-access
        self.command_line_interface.scrollbar._invalidate()
        # pylint: enable=protected-access
        
        self._loop.set_alarm_in(0.01, self._callback, user_data=None)

    def run(self):
        """Run the program and the UI loop in parallel threads.
        
        .. Warning:: 
            If the UI loop (which is executed in the main thread)
            crashes,
            the program (executed in a parallel thread) will probably
            be left waiting for input in a blocking state.
            Safeguards to prevent this should be built into code that
            uses :class:`AdvancedTUI`; for example, this method may
            be called in a ``with`` or a ``try-finally`` block that
            makes sure the program is closed when the block is
            exited.
        """
        self._thread.start()
        self._loop.run()
