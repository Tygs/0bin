#!/usr/bin/env python3


"""
    Main script including runserver and delete-paste.
"""

import sys
import re
import secrets
import _thread as thread

from zerobin.utils import settings, SettingsValidationError, drop_privileges
from zerobin.routes import get_app
from zerobin.paste import Paste

from bottle import run

import clize


def runserver(
    *,
    host="",
    port="",
    debug=None,
    user="",
    group="",
    settings_file="",
    compressed_static=None,
    version=False,
    paste_id_length=None,
    server="cherrypy",
):
    if version:
        print("0bin V%s" % settings.VERSION)
        sys.exit(0)

    settings.HOST = host or settings.HOST
    settings.PORT = port or settings.PORT
    settings.USER = user or settings.USER
    settings.GROUP = group or settings.GROUP
    settings.PASTE_ID_LENGTH = paste_id_length or settings.PASTE_ID_LENGTH
    settings.DEBUG = bool(debug) if debug is not None else settings.DEBUG

    settings.VAR_DIR.mkdir(exist_ok=True, parents=True)
    settings.PASTE_FILES_ROOT.mkdir(exist_ok=True, parents=True)

    secret_key_file = settings.VAR_DIR / "secret_key"
    if not secret_key_file.is_file():
        secret_key_file.write_text(secrets.token_urlsafe(64))
    settings.SECRET_KEY = secret_key_file.read_text()

    try:
        _, app = get_app(debug, settings_file, compressed_static, settings=settings)
    except SettingsValidationError as err:
        print("Configuration error: %s" % err.message, file=sys.stderr)
        sys.exit(1)

    thread.start_new_thread(drop_privileges, (settings.USER, settings.GROUP))

    if settings.DEBUG:
        run(
            app, host=settings.HOST, port=settings.PORT, reloader=True, server=server,
        )
    else:
        run(app, host=settings.HOST, port=settings.PORT, server=server)


# The regex parse the url and separate the paste's id from the decription key
# After the '/paste/' part, there is several caracters, identified as
# the uuid of the paste. Followed by a '#', the decryption key of the paste.
paste_url = re.compile("/paste/(?P<paste_id>.*)#(?P<key>.*)")


def unpack_paste(paste):
    """Take either the ID or the URL of a paste, and return its ID"""

    try_url = paste_url.search(paste)

    if try_url:
        return try_url.group("paste_id")
    return paste


def delete_paste(*pastes, quiet=False):
    """
    Remove pastes, given its ID or its URL

    quiet: Don't print anything

    pastes: List of pastes, given by ID or URL
    """

    for paste_uuid in map(unpack_paste, pastes):
        try:
            Paste.load(paste_uuid).delete()

            if not quiet:
                print("Paste {} is removed".format(paste_uuid))

        except ValueError:
            if not quiet:
                print("Paste {} doesn't exist".format(paste_uuid))


def main():
    subcommands = [runserver, delete_paste]
    subcommand_names = [
        clize.util.name_py2cli(name)
        for name in clize.util.dict_from_names(subcommands).keys()
    ]
    if len(sys.argv) < 2 or sys.argv[1] not in subcommand_names:
        sys.argv.insert(1, subcommand_names[0])
    clize.run(runserver, delete_paste)

