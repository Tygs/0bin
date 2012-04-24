# -*- coding: utf-8 -*-

import os

from bottle import route, run, static_file, debug, view

DEBUG = True
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FILES_ROOT = os.path.join(ROOT_DIR, 'static')


@route('/')
@view('home')
def index():
    return {}


@route('/static/<filename:re:.*>')
def server_static(filename):
    return static_file(filename, root=STATIC_FILES_ROOT)


if __name__ == "__main__":
    if DEBUG:
        debug(True)
        run(host='localhost', port=8080, reloader=True)
    else:
        run(host='localhost', port=8080)