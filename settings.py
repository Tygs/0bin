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