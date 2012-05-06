# -*- coding: utf-8 -*-

"""
    Main script including controller, rooting, dependancy management, and
    server run.
"""

import sys
import os
import hashlib
import thread
import math

from datetime import datetime, timedelta

import settings
sys.path.insert(0, os.path.dirname(settings.ROOT_DIR))
sys.path.append(os.path.join(settings.ROOT_DIR, 'libs'))

import bottle
from bottle import (Bottle, route, run, abort, error,
                    static_file, debug, view, request)

import clize

from src import settings, Paste, drop_privileges, dmerge

app = Bottle()

global_vars = { 
    'settings' : settings
}


@app.route('/')
@view('home')
def index():  
    return global_vars


@app.route('/paste/create', method='POST')
def create_paste():

    try:
        content = unicode(request.forms.get('content', ''), 'utf8')
    except UnicodeDecodeError:
        return {'status': 'error',
                'message': u"Encoding error: the paste couldn't be saved."}

    if '{"iv":' not in content: # reject silently non encrypted content
        return ''

    if content:
        # check size of the paste. if more than settings return error without saving paste.
        # prevent from unusual use of the system.
        # need to be improved
        if len(content) < settings.MAX_SIZE:
            expiration = request.forms.get('expiration', u'burn_after_reading')
            paste = Paste(expiration=expiration, content=content)
            paste.save()
            return {'status': 'ok',
                    'paste': paste.uuid}

    return {'status': 'error',
            'message': u"Serveur error: the paste couldn't be saved. Please try later."}


@app.route('/paste/:paste_id')
@view('paste')
def display_paste(paste_id):


    now = datetime.now()
    keep_alive = False
    try:
        paste = Paste.load(paste_id)
        # Delete the paste if it expired:
        if 'burn_after_reading' in str(paste.expiration):
            # burn_after_reading contains the paste creation date
            # if this read appends 10 seconds after the creation date
            # we don't delete the paste because it means it's the redirection
            # to the paste that happens during the paste creation
            try:
                keep_alive = paste.expiration.split('#')[1]
                keep_alive = datetime.strptime(keep_alive,'%Y-%m-%d %H:%M:%S.%f')
                keep_alive = now < keep_alive + timedelta(seconds=10)
            except IndexError:
                keep_alive = False
            if not keep_alive:
                paste.delete()

        elif paste.expiration < now:
            paste.delete()
            raise ValueError()

    except (TypeError, ValueError):
        #abort(404, u"This paste doesn't exist or has expired")
        return error404(ValueError)

    context = {'paste': paste, 'keep_alive': keep_alive}

    return dmerge(context, global_vars)


@app.error(404)
@view('404')
def error404(code):
    return global_vars

@clize.clize
def runserver(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG,
              serve_static=settings.DEBUG):

    if serve_static:
        @app.route('/static/<filename:path>')
        def server_static(filename):
            return static_file(filename, root=settings.STATIC_FILES_ROOT)

    thread.start_new_thread(drop_privileges, ())

    if debug:
        bottle.debug(True)
        run(app, host=host, port=port, reloader=True, server="cherrypy")
    else:
        run(app, host=host,  port=port, server="cherrypy")




if __name__ == "__main__":
    clize.run(runserver)


