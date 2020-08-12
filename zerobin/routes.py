"""
    Script including controller, rooting, and dependency management.
"""

import os
import sys

import _thread as thread

from urllib.parse import urlparse, parse_qs

from datetime import datetime, timedelta

import bottle
from bottle import (
    Bottle,
    debug,
    static_file,
    view,
    request,
    HTTPResponse,
    redirect,
    abort,
)

from beaker.middleware import SessionMiddleware

from zerobin import __version__
from zerobin.utils import (
    settings,
    SettingsValidationError,
    ensure_var_env,
    check_password,
)
from zerobin.paste import Paste


ensure_var_env()


GLOBAL_CONTEXT = {
    "settings": settings,
    "VERSION": __version__,
    "pastes_count": Paste.get_pastes_count(),
    "refresh_counter": datetime.now(),
}


app = Bottle()

ADMIN_LOGIN_URL = settings.ADMIN_URL + "login/"


@app.route("/")
@view("home")
def index():
    return GLOBAL_CONTEXT


@app.get("/faq/")
@view("faq")
def faq():
    return GLOBAL_CONTEXT


@app.get(settings.ADMIN_URL)
@app.post(settings.ADMIN_URL)
@view("admin")
def admin():
    session = request.environ.get("beaker.session")
    if not session or not session.get("is_authenticated"):
        redirect(ADMIN_LOGIN_URL)

    paste_id = request.forms.get("paste", "")
    if paste_id:
        try:
            if "/paste/" in paste_id:
                paste_id = urlparse(paste_id).path.split("/paste/")[-1]
            paste = Paste.load(paste_id)
            paste.delete()
        except (TypeError, ValueError, FileNotFoundError):
            return {
                "status": "error",
                "message": f"Cannot find paste '{paste_id}'",
                **GLOBAL_CONTEXT,
            }

        return {"status": "ok", "message": "Paste deleted", **GLOBAL_CONTEXT}

    return {"status": "ok", "message": "" ** GLOBAL_CONTEXT}


@app.get(ADMIN_LOGIN_URL)
@app.post(ADMIN_LOGIN_URL)
@view("login")
def login():

    password = request.forms.get("password")
    if password:
        if not check_password(password):
            return {"status": "error", "message": "Wrong password", **GLOBAL_CONTEXT}

        session = request.environ.get("beaker.session")
        session["is_authenticated"] = True
        session.save()

        redirect(settings.ADMIN_URL)

    return {"status": "ok", **GLOBAL_CONTEXT}


@app.post(settings.ADMIN_URL + "logout/")
@view("logout")
def logout():
    session = request.environ.get("beaker.session")
    session["is_authenticated"] = False
    session.save()
    redirect("/")


@app.post("/paste/create")
def create_paste():

    try:
        body = parse_qs(request.body.read(int(settings.MAX_SIZE * 1.1)))
    except ValueError:
        return {"status": "error", "message": "Wrong data payload."}

    try:
        content = "".join(x.decode("utf8") for x in body[b"content"])
    except (UnicodeDecodeError, KeyError):
        return {
            "status": "error",
            "message": "Encoding error: the paste couldn't be saved.",
        }

    if '{"iv":' not in content:  # reject silently non encrypted content
        return {"status": "error", "message": "Wrong data payload."}

    # check size of the paste. if more than settings return error
    # without saving paste.  prevent from unusual use of the
    # system.  need to be improved
    if 0 < len(content) < settings.MAX_SIZE:
        expiration = body.get(b"expiration", [b"burn_after_reading"])[0]
        paste = Paste(
            expiration=expiration.decode("utf8"),
            content=content,
            uuid_length=settings.PASTE_ID_LENGTH,
        )
        paste.save()

        # display counter
        if settings.DISPLAY_COUNTER:

            # increment paste counter
            paste.increment_counter()

            # if refresh time elapsed pick up new counter value
            now = datetime.now()
            timeout = GLOBAL_CONTEXT["refresh_counter"] + timedelta(
                seconds=settings.REFRESH_COUNTER
            )
            if timeout < now:
                GLOBAL_CONTEXT["pastes_count"] = Paste.get_pastes_count()
                GLOBAL_CONTEXT["refresh_counter"] = now

        return {"status": "ok", "paste": paste.uuid, "owner_key": paste.owner_key}

    return {
        "status": "error",
        "message": "Serveur error: the paste couldn't be saved. " "Please try later.",
    }


@app.get("/paste/:paste_id")
@view("paste")
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
                keep_alive = paste.expiration.split("#")[1]
                keep_alive = datetime.strptime(keep_alive, "%Y-%m-%d %H:%M:%S.%f")
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

    return {"paste": paste, "keep_alive": keep_alive, **GLOBAL_CONTEXT}


@app.delete("/paste/:paste_id")
def delete_paste(paste_id):

    try:
        paste = Paste.load(paste_id)
    except (TypeError, ValueError):
        return error404(ValueError)

    if paste.owner_key != request.forms.get("owner_key", None):
        return HTTPResponse(status=403, body="Wrong owner key")

    paste.delete()

    return {
        "status": "ok",
        "message": "Paste deleted",
    }


@app.error(404)
@view("404")
def error404(code):
    return GLOBAL_CONTEXT


@app.get("/static/<filename:path>")
def server_static(filename):
    return static_file(filename, root=settings.STATIC_FILES_ROOT)


def get_app(debug=None, settings_file="", compressed_static=None, settings=settings):
    """
        Return a tuple (settings, app) configured using passed
        parameters and/or a setting file.
    """

    settings_file = settings_file or os.environ.get("ZEROBIN_SETTINGS_FILE")

    if settings_file:
        settings.update_with_file(os.path.realpath(settings_file))

    if settings.PASTE_ID_LENGTH < 4:
        raise SettingsValidationError("PASTE_ID_LENGTH cannot be lower than 4")

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


app = SessionMiddleware(
    app,
    {
        "session.type": "file",
        "session.cookie_expires": 300,
        "session.data_dir": settings.SESSIONS_DIR,
        "session.auto": True,
    },
)
