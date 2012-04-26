# -*- coding: utf-8 -*-

import os
import hashlib
import sys

from bottle import (Bottle, route, run, static_file, debug, view, request)

import settings

# ensure we got the project module on the python path to avoid import problems
sys.path.insert(0, os.path.dirname(settings.ROOT_DIR))

from src.paste import Paste

app = Bottle()


@app.route('/')
@view('home')
def index():
    return {}


@app.route('/paste/create', method='POST')
def create_paste():

    try:
        content = unicode(request.forms.get('content', ''), 'utf8')
    except UnicodeDecodeError:
        content = u''

    if content:
        expire_in = request.forms.get('expire_in', u'burn_after_reading')
        paste = Paste(expire_in=expire_in, content=content)
        paste.save()

        return paste.uuid

    return ''


@app.route('/static/<filename:re:.*>')
def server_static(filename):
    return static_file(filename, root=settings.STATIC_FILES_ROOT)


if __name__ == "__main__":
    if settings.DEBUG:
        debug(True)
        run(app, host='localhost', port=8000, reloader=True)
    else:
        run(app, host='localhost', port=8000)