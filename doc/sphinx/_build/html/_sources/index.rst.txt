HVCtl
=====

HVCtl is a RS-232 controller for a Technix SR100KV-5KW high voltage generator.
It was written in Python 3.8 and is intended for Linux operating systems.

Documentation
-------------

.. toctree::
   :maxdepth: 2
   
   installation.rst
   usage.rst
   modules/index.rst
   protocol.rst
   
Compatibility with other Technix models
---------------------------------------

HVCtl is based on information provided in the SR100KV-5KW user manual,
which only describes that specific model.
It might also work with other Technix SR series models,
since it seems likely that those models use the same or a very similar control
protocol.

Author
------

HVCtl was written by Feliks Kivelä based on an earlier work by Pekko Metsä.
The author can be contacted at firstname.lastname@helsinki.fi
(with the "ä" replaced by an "a").

Copyright © 2019 - 2021 University of Helsinki Fusor Team.

License
-------
   
HVCtl is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/.
