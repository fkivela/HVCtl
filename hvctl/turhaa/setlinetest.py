import urwid

class ScrollableLines(urwid.WidgetWrap):
        
    def __init__(self):
        string = '\n'.join([f'test {i}' for i in range(100)])
        pile = urwid.Pile( [urwid.Text(string)] )
        super().__init__(urwid.ListBox([pile]))
        

    def mouse_event(self, size, event, button, col, row, focus):
        """Handle mouse events."""
        # Super makes the screen scroll up or down with the arrow keys.
        # Here the arrow keys are used to browse history, and the 
        # mouse wheel is used to scroll instead.
        
#        if button == 1:
#            raise ValueError(self.get_focus_offset_inset(size))
        
        if button == 4:
            #super().keypress(size, 'up')
            self.scroll_up(size)
            #self.upon_scroll(1)
        elif button == 5:
            #super().keypress(size, 'down')
            self.scroll_down(size)
            #self.upon_scroll(-1)
        else:
            return super().mouse_event(size, event, button, col, row, focus)
        
        
    def set_offset(self, size, offset):      
        self._w.change_focus(size, 0, -offset)
        
#    def widget_rows(self, size):
#        cols, rows = size
#        return [w.rows((cols,)) for w in list(self.body.contents)]
        
#    def total_rows(self, size):
#        return sum(self.widget_rows(size))
        
    def offset(self, size):
        widget_offset, widget_inset = self._w.get_focus_offset_inset(size)
        ret = widget_inset
        #if ret > self.max_offset(size):
        #    #raise ValueError('offset: going over max offset')
        #    ret = self.max_offset(size)
        return ret
    
#    def max_offset(self, size):
#        cols, visible_rows = size
#        return max(self.total_rows(size) - visible_rows, 0)
        
    def scroll_down(self, size):
        new_offset = self.offset(size) + 1
        #if new_offset > self.max_offset(size):
        #    new_offset = self.max_offset(size)
        
        self.set_offset(size, new_offset)
        
    def scroll_up(self, size):
        new_offset = self.offset(size) - 1
        #if new_offset < 0:
        #    new_offset = 0
        
        self.set_offset(size, new_offset)        

box = ScrollableLines()
loop = urwid.MainLoop(box)
loop.run()