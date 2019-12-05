"""This module is used to create a status screen for the
:attr:`display <hvctl.advanced_tui.AdvancedTUI.display>`
of an :class:`~hvctl.advanced_tui.AdvancedTUI`.

Attributes:
    palette:
        A colour palette for an
        :class:`~hvctl.advanced_tui.AdvancedTUI`.
        
    red_button:
        This is displayed by :class:`urwid.Text` widgets as a red
        circle, if the widgets are used in an
        :class:`~hvctl.advanced_tui.AdvancedTUI`
        initialized with :attr:`palette`.
        
    green_button:
        Similar to :attr:`red_button`, but green instead of red.
"""

# (name, text color, background color)
palette = [('green', 'light green', ''), 
           ('red', 'light red', '')]

red_button = ('red', '⏺')
green_button = ('green', '⏺')

def generate_text(status):
    """Return a formatted status display.
    
    Returns:
        A nested iterable of strings, which will be interpreted by
        :class:`urwid.Text` as coloured text.
        The format is explained 
        `here <http://urwid.org/manual/displayattributes.html
        ?highlight=display%20attributes#text-markup>`_.
    """
    text = ([
        _output_text, '\n',
        _onoff_text(status), '\n',
        '\n',
        _mode_text(status), '\n',
        _inhibition_text(status), '\n',
        _interlock_text(status), '\n',
        _fault_text(status)
    ])
    return text


def _output_text(status):
    """Return the voltage and the current as an iterable
    accepted by urwid.Text.
    """
    voltage_str = f'Voltage: {status.voltage:.2f} V'
    current_str = f'Current: {status.current:.2f} mA'
    
    # The vertical position of regulation_str depends on the length of
    # the longer string.
    width = max(len(voltage_str), len(current_str))
    regulation_str = '  ⯇ Regulated'
    if status.regulation == 'voltage':
        voltage_str = voltage_str.ljust(width) + regulation_str
    else:
        current_str += current_str.ljust(width) + regulation_str
    
    return voltage_str + '\n' + current_str


# The amount of characters before the red or green button.
# All functions below use the same value in order to make the
# buttons line up.
_width = 14


def _onoff_text(status):
    """Return the HV on/off status as well as the status of the 
    HV on and HV off commands as an iterable accepted by urwid.Text.
    """
    name = ('', 'HV output: '.ljust(_width))
    button = green_button if status.hv_on_status else red_button
    space = ' '
    value = 'On' if status.hv_on_status else 'Off'
    return [name, button, space, value]


def _mode_text(status):
    """Return the control mode as an iterable
    accepted by urwid.Text.
    """
    name = ('', 'Control mode: '.ljust(_width))
    button = green_button if status.mode == 'remote' else red_button
    space = ' '
    value = status.mode.capitalize()
    return [name, button, space, value]


def _inhibition_text(status):
    """Return the status of inhibition as an iterable
    accepted by urwid.Text.
    """
    name = ('', 'Inhibition: '.ljust(_width))
    button = red_button if status.inhibit else green_button
    space = ' '
    value = 'On' if status.inhibit else 'Off'
    return [name, button, space, value]


def _interlock_text(status):
    """Return the status of the interlock as an iterable
    accepted by urwid.Text.
    """
    name = ('', 'Interlock:'.ljust(_width))
    button = green_button if status.interlock == 'closed' else red_button
    space = ' '
    value = status.interlock.capitalize()
    return [name, button, space, value]


def _fault_text(status):
    """Return the status of the fault state as an iterable
    accepted by urwid.Text.
    """
    name = ('', 'Fault:'.ljust(_width))
    button = green_button if not status.fault else red_button
    space = ' '
    value = 'Yes' if status.fault else 'No'
    return [name, button, space, value]
