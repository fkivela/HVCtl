:mod:`command_line_ui`
======================

.. automodule:: command_line_ui
	   
.. autoclass:: Command
	   
.. autoclass:: CommandLineUI
	:members:
	:exclude-members: commandlist, commands
	
   
   	.. automethod:: __init__
   	
   	.. 
   		commandlist and commands are documented here manually, because autodoc 
   		displays their values, which are very long.
   	
   	.. attribute:: commandlist
   	
	   	Class attribute. A list of accepted commands 
		(as :class:`Command` objects).
   	
   	.. attribute:: commands
    
		Class attribute. A dict of accepted commands, 
		with command names as keys and :class:`Command` objects as values. 
		Aliases for the same command are represented with different keys 
		mapping to the same value.


   
