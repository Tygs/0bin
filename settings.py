# -*- coding: utf-8 -*-

import os
import math
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FILES_ROOT = os.path.join(ROOT_DIR, 'static')

#####################################################
# You can start editing settings after this comment #
#####################################################

# debug will get you error message and auto reload
# don't set this to True in production
DEBUG = False

# absolute path where the paste files should be store
# default in projectdirectory/static/content/
# use "/" even under Windows
PASTE_FILES_ROOT = os.path.join(STATIC_FILES_ROOT, 'content')

# Port and host the embeded python server should be using
HOST = "127.0.0.1"
PORT= "8000"

# User and group the server should run as. Set to None if it should be the
# current user
USER = None
GROUP = None

# limit size of pasted text in bytes. Be carefull allowing too much size can slow down user's
# browser
MAX_SIZE = 1024 * 500
MAX_SIZE_KB = int(math.ceil(MAX_SIZE / 1024.0))

# this import a file named settings_local.py if it exists
# you may want to create such a file to have different settings
# on each machine
try:
    from settings_local import *
except ImportError:
    pass