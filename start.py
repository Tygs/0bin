# -*- coding: utf-8 -*-

"""
    Main script including controller, rooting, dependancy management, and
    server run.
"""

import os
import hashlib

from src import settings, setup_path, Paste

setup_path()

from bottle import (Bottle, route, run, abort,
                    static_file, debug, view, request)


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
        expiration = request.forms.get('expiration', u'burn_after_reading')
        paste = Paste(expiration=expiration, content=content)
        paste.save()

        return paste.uuid

    return ''


@app.route('/paste/:paste_id')
@view('paste')
def display_paste(paste_id):

    try:
        paste = Paste.load(paste_id)
    except (TypeError, ValueError):
        abort(404, u"This paste does't exist or has expired")

    return {'paste': paste}


@app.route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root=settings.STATIC_FILES_ROOT)


if __name__ == "__main__":
    if settings.DEBUG:
        debug(True)
        run(app, host='localhost', port=8080, reloader=True, server="cherrypy")
    else:
        run(app, host='localhost', port=8080, server="cherrypy")