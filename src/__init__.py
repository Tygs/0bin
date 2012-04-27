# -*- coding: utf-8 -*-

"""
    General configuration and imports gathering.
"""

import os
import sys

import settings
from paste import Paste


def setup_path():
    """
        Add the project dir in the python path to the site to run with the
        source code beeing just copied/pasted and not installed.

        Also try to import dependancies. If it fails, fallback on embeded libs.
    """
    sys.path.insert(0, os.path.dirname(settings.ROOT_DIR))

    try:
        import bottle
    except ImportError:
        sys.path.append(os.path.join(settings.ROOT_DIR, 'libs'))