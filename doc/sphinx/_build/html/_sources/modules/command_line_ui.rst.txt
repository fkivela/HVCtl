:mod:`command_line_ui`
======================

.. automodule:: command_line_ui
	   
.. autoclass:: CommandLineUI
	:members:
	:exclude-members: cmds_and_aliases
   
   	.. automethod:: __init__
   	
   	.. 
   		cmds_and_aliases is documented here manually to prevent autodoc 
   		from displaying its value.
   		
   	.. attribute:: cmds_and_aliases
   	
   	   	Class attribute.
		A list of two-index tuples.
		The first index is of each tuple is the primary name of a command 
		accepted by the UI,
		and the second is a list of aliases for that command.
