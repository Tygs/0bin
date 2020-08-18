"""
    Script including controller, rooting, and dependency management.
"""

import os

from distutils.util import strtobool

from urllib.parse import urlparse

from datetime import datetime, timedelta

import bottle
from bottle import (
    Bottle,
    static_file,
    view,
    request,
    HTTPResponse,
    redirect,
)

from beaker.middleware import SessionMiddleware

from zerobin import __version__
from zerobin.utils import (
    SettingsValidationError,
    ensure_app_context,
    check_password,
    settings,
)
from zerobin.paste import Paste


ensure_app_context()


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

@app.route("/buy_bitcoin")
@view("buy_bitcoin")
def index():
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

    return {"status": "ok", "message": "", **GLOBAL_CONTEXT}


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

    # Reject what is too small, too big, or what does not seem encrypted to
    # limit a abuses
    content = request.forms.get("content", "")
    if '{"iv":' not in content or not (0 < len(content) < settings.MAX_SIZE):
        return {"status": "error", "message": "Wrong data payload."}

    expiration = request.forms.get("expiration", "burn_after_reading")
    title = request.forms.get("title", "")
    btc_tip_address = request.forms.get("btcTipAddress", "")

    paste = Paste(
        expiration=expiration,
        content=content,
        uuid_length=settings.PASTE_ID_LENGTH,
        title=title,
        btc_tip_address=btc_tip_address,
    )
    paste.save()

    # If refresh time elapsed pick up, update the counter
    if settings.DISPLAY_COUNTER:

        paste.increment_counter()

        now = datetime.now()
        timeout = GLOBAL_CONTEXT["refresh_counter"] + timedelta(
            seconds=settings.REFRESH_COUNTER
        )
        if timeout < now:
            GLOBAL_CONTEXT["pastes_count"] = Paste.get_pastes_count()
            GLOBAL_CONTEXT["refresh_counter"] = now

    return {"status": "ok", "paste": paste.uuid, "owner_key": paste.owner_key}


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


def get_app(debug=None, config_dir="", data_dir=""):
    """
        Return a tuple (settings, app) configured using passed
        parameters and/or a setting file.
    """

    data_dir = data_dir or os.environ.get("ZEROBIN_DATA_DIR")
    config_dir = config_dir or os.environ.get("ZEROBIN_CONFIG_DIR")

    ensure_app_context(config_dir=config_dir, data_dir=data_dir)

    if debug is None:
        settings.DEBUG = bool(
            strtobool(os.environ.get("ZEROBIN_DEBUG", str(settings.DEBUG)))
        )
    else:
        settings.DEBUG = debug

    settings.DISPLAY_COUNTER = bool(
        os.environ.get("ZEROBIN_DISPLAY_COUNTER", settings.DISPLAY_COUNTER)
    )
    settings.REFRESH_COUNTER = int(
        os.environ.get("ZEROBIN_REFRESH_COUNTER", settings.REFRESH_COUNTER)
    )
    settings.MAX_SIZE = int(os.environ.get("ZEROBIN_MAX_SIZE", settings.MAX_SIZE))
    settings.PASTE_ID_LENGTH = int(
        os.environ.get("ZEROBIN_PASTE_ID_LENGTH", settings.PASTE_ID_LENGTH)
    )

    if settings.PASTE_ID_LENGTH < 4:
        raise SettingsValidationError("PASTE_ID_LENGTH cannot be lower than 4")

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
