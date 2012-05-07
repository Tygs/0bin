#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import os
import math

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_FILES_ROOT = os.path.join(ROOT_DIR, 'static')

# debug will get you error message and auto reload
# don't set this to True in production
DEBUG = False

# absolute path where the paste files should be store
# default in projectdirectory/static/content/
# use "/" even under Windows
PASTE_FILES_ROOT = os.path.join(STATIC_FILES_ROOT, 'content')

# Port and host the embeded python server should be using
# You can also specify them using the --host and --port script options
# which have priority on these settings
HOST = "127.0.0.1"
PORT= "8000"

# User and group the server should run as. Set to None if it should be the
# current user. Some OS don't support it and if so, it will be ignored.
USER = None
GROUP = None

# limit size of pasted text in bytes. Be carefull allowing too much size can slow down user's
# browser
MAX_SIZE = 1024 * 500
MAX_SIZE_KB = int(math.ceil(MAX_SIZE / 1024.0))

