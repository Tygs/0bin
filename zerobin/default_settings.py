#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4


######## NOT SETTINGS, JUST BOILER PLATE ##############
import os
import math

VERSION = '0.1'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_DIR = os.path.join(os.path.dirname(ROOT_DIR), 'libs')

######## END OF BOILER PLATE ##############

# debug will get you error message and auto reload
# don't set this to True in production
DEBUG = False

# Should the application serve static files on it's own ?
# IF yes, set the absolute path to the static files.
# If no, set it to None
# In dev this is handy, in prod you probably want the HTTP servers
# to serve it, but it's OK for small traffic to set it to True in prod too.
STATIC_FILES_ROOT = os.path.join(ROOT_DIR, 'static')

# If True, will link the compressed verion of the js and css files,
# otherwise, will use the ordinary files
COMPRESSED_STATIC_FILES = False

# absolute path where the paste files should be store
# default in projectdirectory/static/content/
# use "/" even under Windows
PASTE_FILES_ROOT = os.path.join(STATIC_FILES_ROOT, 'content')

# a tuple of absolute paths of directory where to look the template for
# the first one will be the first to be looked into
# if you want to override a template, create a new dir, write the
# template with the same name as the one you want to override in it
# then add the dir path at the top of this tuple
TEMPLATE_DIRS = (
    os.path.join(ROOT_DIR, 'views'),
)

# Port and host the embeded python server should be using
# You can also specify them using the --host and --port script options
# which have priority on these settings
HOST = "127.0.0.1"
PORT = "8000"

# User and group the server should run as. Set to None if it should be the
# current user. Some OS don't support it and if so, it will be ignored.
USER = None
GROUP = None

# Names/links to insert in the menu bar.
# Any link with "mailto:" will be escaped to prevent spam
MENU = (
    ('Home', '/'), # internal link. First link will be highlited
    ('Download 0bin', 'https://github.com/sametmax/0bin'), # external link
    ('Contact', 'mailto:your@email.com') # email
)

# limit size of pasted text in bytes. Be carefull allowing too much size can
# slow down user's browser
MAX_SIZE = 1024 * 500
