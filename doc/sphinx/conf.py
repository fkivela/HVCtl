# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

# The HVCtl directory should already be in $PATH.

# -- Project information -----------------------------------------------------

project = 'HVCtl'
copyright = '2019, University of Helsinki Fusor Team'
author = 'Feliks Kivelä'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

# Autodoc: Generate documentation from docstrings automatically.
# Napoleon: Support for Google-style docstrings.
# Intersphinx: Link to the documentaion of other sphinx projects.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx.ext.intersphinx']

# Use the class docstring (instead of the __init__ docstring) for class descriptions.
# This seems to be the default value, but is specified just in case.
autoclass_content = 'class'

# Document classes, functions etc. in the same order as they are defined in the source code,
# instead of in alphabetical order.
autodoc_member_order = 'bysource'

# :special-members: prints __weakref__ by default; this disables that.
autodoc_default_options = {
	# Print members (i.e. attributes, methods, classes etc.) when documenting a module or an object.
	'members': True,
	# Print special members such as __init__ and __repr__.
	'special-members': True,
	# Print members in the same order as they ae in the source files.
	'member-order': 'bysource',
	# Don't print __weakref__.
    'exclude-members': '__weakref__',
}

# Projects linked to by Intersphinx.
intersphinx_mapping = {'python': ('https://docs.python.org/3', None),
					   'serial': ('https://pyserial.readthedocs.io/en/latest', None),
					   'urwid': ('http://urwid.org', None),}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

html_static_path = ['_static']

