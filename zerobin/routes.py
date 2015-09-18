#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, absolute_import, print_function

"""
    Script including controller, rooting, and dependency management.
"""

import os
import sys

try:
    import thread
except ImportError:
    import _thread as thread

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from datetime import datetime, timedelta

# add project dir and libs dir to the PYTHON PATH to ensure they are
# importable
from zerobin.utils import (settings, SettingsValidationError,
                           drop_privileges, dmerge)

import bottle
from bottle import (Bottle, run, static_file, view, request)

from zerobin.paste import Paste


app = Bottle()
GLOBAL_CONTEXT = {
    'settings': settings,
    'pastes_count': Paste.get_pastes_count(),
    'refresh_counter': datetime.now()
}


@app.route('/')
@view('home')
def index():
    return GLOBAL_CONTEXT


@app.route('/faq/')
@view('faq')
def faq():
    return GLOBAL_CONTEXT


@app.route('/paste/create', method='POST')
def create_paste():
    try:
        body = urlparse.parse_qs(request.body.read(int(settings.MAX_SIZE * 1.1)))
    except ValueError:
        return {'status': 'error', 'message': "Wrong data payload."}

    try:

        content = "".join(x.decode('utf8') for x in body[b'content'])
    except (UnicodeDecodeError, KeyError):
        return {'status': 'error',
                'message': "Encoding error: the paste couldn't be saved."}

    if '{"iv":' not in content:  # reject silently non encrypted content
        return {'status': 'error', 'message': "Wrong data payload."}

    # check size of the paste. if more than settings return error
    # without saving paste.  prevent from unusual use of the
    # system.  need to be improved
    if 0 < len(content) < settings.MAX_SIZE:
        expiration = body.get(b'expiration', ['burn_after_reading'])[0]
        paste = Paste(expiration=expiration.decode('utf8'), content=content,
                      uuid_length=settings.PASTE_ID_LENGTH)
        paste.save()

        # display counter
        if settings.DISPLAY_COUNTER:

            #increment paste counter
            paste.increment_counter()

            # if refresh time elapsed pick up new counter value
            now = datetime.now()
            timeout = (GLOBAL_CONTEXT['refresh_counter']
                       + timedelta(seconds=settings.REFRESH_COUNTER))
            if timeout < now:
                GLOBAL_CONTEXT['pastes_count'] = Paste.get_pastes_count()
                GLOBAL_CONTEXT['refresh_counter'] = now

        return {'status': 'ok', 'paste': paste.uuid}

    return {'status': 'error',
            'message': "Serveur error: the paste couldn't be saved. "
                       "Please try later."}


@app.route('/paste/:paste_id')
@view('paste')
def display_paste(paste_id):

    now = datetime.now()
    keep_alive = False
    try:
        paste = Paste.load(paste_id)
        # Delete the paste if it expired:
        if not isinstance(paste.expiration, datetime):
            # burn_after_reading contains the paste creation date
            # if this read appends 10 seconds after the creation date
            # we don't delete the paste because it means it's the redirection
            # to the paste that happens during the paste creation
            try:
                keep_alive = paste.expiration.split('#')[1]
                keep_alive = datetime.strptime(keep_alive,
                                               '%Y-%m-%d %H:%M:%S.%f')
                keep_alive = now < keep_alive + timedelta(seconds=10)
            except IndexError:
                keep_alive = False
            if not keep_alive:
                paste.delete()

        elif paste.expiration < now:
            paste.delete()
            raise ValueError()

    except (TypeError, ValueError):
        return error404(ValueError)

    context = {'paste': paste, 'keep_alive': keep_alive}
    return dmerge(context, GLOBAL_CONTEXT)


@app.error(404)
@view('404')
def error404(code):
    return GLOBAL_CONTEXT


@app.route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root=settings.STATIC_FILES_ROOT)


def get_app(debug=None, settings_file='',
            compressed_static=None, settings=settings):
    """
        Return a tuple (settings, app) configured using passed
        parameters and/or a setting file.
    """

    settings_file = settings_file or os.environ.get('ZEROBIN_SETTINGS_FILE')

    if settings_file:
        settings.update_with_file(os.path.realpath(settings_file))

    if settings.PASTE_ID_LENGTH < 4:
        raise SettingsValidationError('PASTE_ID_LENGTH cannot be lower than 4')

    if compressed_static is not None:
        settings.COMPRESSED_STATIC_FILES = compressed_static

    if debug is not None:
        settings.DEBUG = debug

    # make sure the templates can be loaded
    for d in reversed(settings.TEMPLATE_DIRS):
        bottle.TEMPLATE_PATH.insert(0, d)

    if settings.DEBUG:
        bottle.debug(True)

    return settings, app
