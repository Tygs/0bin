# -*- coding: utf-8 -*-

import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FILES_ROOT = os.path.join(ROOT_DIR, 'static')

#####################################################
# You can start editing settings after this comment #
#####################################################

# debug will get you error message and auto reload
# don't set this to True in production
DEBUG = True

# absolute path where the paste files should be store
# default in projectdirectory/static/content/
# use "/" even under Windows
PASTE_FILES_ROOT = os.path.join(STATIC_FILES_ROOT, 'content')
# Port and host the embeded python server should be using in prod and in dev
PROD_HOST = "0.0.0.0"
PROD_PORT= "80"
DEV_HOST = "127.0.0.1"
DEV_PORT= "8000"

# User and group the server should run as. Set to None if it should be the
# current user
USER = None
GROUP = None