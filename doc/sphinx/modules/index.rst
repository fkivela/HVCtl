Modules
=======

This page contains a list of all Python modules included in the HVCtl program. 
All modules are located in the ``hvctl`` package, and can be imported with any of the following syntaxes, 
as long as the ``HVCtl`` directory is your working directory or in your ``PYTHONPATH``. 

>>> import hvctl
>>> api = hvctl.api.API()

>>> import hvctl.api
>>> api = hvctl.api.API()

>>> from hvctl import api
>>> apiobj = api.API() # The name 'api' is already taken

>>> from hvctl.api import API
>>> api = API()

.. toctree::
   :maxdepth: 2
   :caption: List of modules:
   
   config.rst
   message.rst
   api.rst
   widgets.rst
   command_line_ui.rst
   advanced_tui.rst
   queuefile.rst
   virtualconnection.rst
   virtualhv.rst
   
