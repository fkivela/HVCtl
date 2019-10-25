from urwid import Text, Filler, Padding, Pile, Columns, MainLoop, ListBox

t_upper = Text('upper half')
t_left = ListBox([])
t_right = Text('lower right')
f_upper = Filler(t_upper)
f_left = (t_left)
f_right = Filler(t_right)

lower = Columns([f_left, f_right])
screen = Pile([f_upper, lower])

loop = MainLoop(screen)
loop.run()


#t_left = ListBox([])
#f_left = Filler(t_left)

#loop = MainLoop(t_left)
#loop.run()