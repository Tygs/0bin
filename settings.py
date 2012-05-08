# -*- coding: utf-8 -*-

# import default settings value from src/default_settings.py
# you can refer to this file if you forgot what
# settings is for and what it is set to by default
# DO NOT ALTER THIS LINE
from src.default_settings import *

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

# limit size of pasted text in bytes. Be carefull allowing too much
# size can slow down user's browser
MAX_SIZE = 1024 * 500
MAX_SIZE_KB = int(math.ceil(MAX_SIZE / 1024.0))

# Names/links to insert in the menu bar.
# Any link with "mailto:" will be escaped to prevent spam
MENU = (
    ('Home', '/'), # internal link
    ('Download 0bin', 'https://github.com/sametmax/0bin'), # external link
    ('Contact', 'mailto:your@email.com') # email
)

# this import a file named settings_local.py if it exists
# you may want to create such a file to have different settings
# on each machine
try:
    from settings_local import *
except ImportError:
    pass
