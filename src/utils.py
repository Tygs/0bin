# -*- coding: utf-8 -*-

import time
import sys
import os
import settings
import glob
import tempfile


try:
    from privilege import drop_privileges_permanently, coerce_user, coerce_group
except (AttributeError):
    pass # privilege does't work on several plateform


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

            lock_files =  glob.glob(os.path.join(tempfile.gettempdir(),
                                                 'bottle.*.lock'))
            for lock_file in lock_files:
                os.chown(lock_file, user, group)

            drop_privileges_permanently(user, group, ())
        except Exception:
            print "Failed to drop privileges. Running with current user."


def dmerge(*args):
    """
        return new directionay being the sum of all merged dictionaries passed as arguments
    """

    dictionary = {}

    for arg in args:
        dictionary.update(arg)

    return dictionary
