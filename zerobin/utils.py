# coding: utf-8

from __future__ import print_function, unicode_literals, absolute_import

import time
import os
import glob
import tempfile
import sys
import codecs
import unicodedata
from functools import partial

from zerobin import default_settings
sys.path.append(default_settings.LIBS_DIR)

try:
    from zerobin.privilege import drop_privileges_permanently, coerce_user, coerce_group
except (AttributeError):
    pass  # privilege does't work on several plateform

try:
    from runpy import run_path
except ImportError:
    # python-2.6 or earlier - use simplier less-optimized execfile()
    def run_path(file_path):
        mod_globals = {'__file__': file_path}
        execfile(file_path, mod_globals)
        return mod_globals


def drop_privileges(user=None, group=None, wait=5):
    """
        Try to set the process user and group to another one.
        If no group is provided, it's set to the same as the user.
        You can wait for a certain time before doing so.
    """
    if wait:
        time.sleep(wait)
    if user:
        group = group or user
        try:
            user = coerce_user(user)
            group = coerce_group(group)

            lock_files = glob.glob(os.path.join(tempfile.gettempdir(),
                                               'bottle.*.lock'))
            for lock_file in lock_files:
                os.chown(lock_file, user, group)

            drop_privileges_permanently(user, group, ())
        except Exception:
            print("Failed to drop privileges. Running with current user.")


def dmerge(*args):
    """
        Return new directionay being the sum of all merged dictionaries passed
        as arguments
    """
    dictionary = {}
    for arg in args:
        dictionary.update(arg)
    return dictionary


class SettingsValidationError(Exception):
    pass


class SettingsContainer(object):
    """
        Singleton containing the settings for the whole app
    """

    _instance = None

    def __new__(cls, *args, **kwargs):

        if not cls._instance:
            cls._instance = super(SettingsContainer, cls).__new__(cls, *args,
                                                                  **kwargs)
            cls._instance.update_with_module(default_settings)
        return cls._instance


    def update_with_dict(self, dict):
        """
            Update settings with values from the given mapping object.
            (Taking only variable with uppercased name)
        """
        for name, value in dict.items():
            if name.isupper():
                setattr(self, name, value)
        return self


    def update_with_module(self, module):
        """
            Update settings with values from the given module.
            Uses update_with_dict() behind the scenes.
        """
        return self.update_with_dict(module.__dict__)


    @classmethod
    def from_module(cls, module):
        """
            Create an instance of SettingsContainer with values based
            on the one in the passed module.
        """
        settings = cls()
        settings.update_with_module(module)
        return settings


    def update_with_file(self, filepath):
        """
            Update settings with values from the given module file.
            Uses update_with_dict() behind the scenes.
        """
        settings = run_path(filepath)
        return self.update_with_dict(settings)


settings = SettingsContainer()


def to_ascii(utext):
    """ Take a unicode string and return ascii bytes.

        Try to replace non ASCII char by similar ASCII char. If it can't,
        replace it with "?".
    """
    return unicodedata.normalize('NFKD', utext).encode('ascii', "replace")


# Make sure to always specify encoding when using open in Python 2 or 3
safe_open = partial(codecs.open, encoding="utf8")


def as_unicode(obj):
    """ Return the unicode representation of an object """
    try:
        return unicode(obj)
    except NameError:
        return str(obj)
