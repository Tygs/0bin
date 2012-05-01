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


def drop_privileges():
    time.sleep(5)
    if settings.USER:
        settings.GROUP = settings.GROUP or settings.USER
        try:
            user = coerce_user(settings.USER)
            group = coerce_group(settings.GROUP)

            lock_files =  glob.glob(os.path.join(tempfile.gettempdir(),
                                                 'bottle.*.lock'))
            for lock_file in lock_files:
                os.chown(lock_file, user, group)

            drop_privileges_permanently(settings.USER, settings.GROUP, ())
        except Exception:
            print "Failed to drop privileges. Running with current user."