import time
import os
import glob
import tempfile
import codecs
import unicodedata
import hashlib
import secrets
from functools import partial

from zerobin import default_settings

try:
    from zerobin.privilege import drop_privileges_permanently, coerce_user, coerce_group
except (AttributeError):
    pass  # privilege does't work on several plateforms


from runpy import run_path


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

            lock_files = glob.glob(os.path.join(tempfile.gettempdir(), "bottle.*.lock"))
            for lock_file in lock_files:
                os.chown(lock_file, user, group)

            drop_privileges_permanently(user, group, ())
        except Exception:
            print("Failed to drop privileges. Running with current user.")


class SettingsValidationError(Exception):
    pass


class SettingsContainer(object):
    """
        Singleton containing the settings for the whole app
    """

    _instance = None

    def __new__(cls, *args, **kwargs):

        if not cls._instance:
            cls._instance = super(SettingsContainer, cls).__new__(cls, *args, **kwargs)
            cls._instance.update_with_module(default_settings)
        return cls._instance

    def update_with_dict(self, dict):
        """
            Update settings with values from the given mapping object.
            (Taking only variable with uppercased name)
        """
        for name, value in dict.items():
            if name.isupper():
                setattr(self, name, value)
        return self

    def update_with_module(self, module):
        """
            Update settings with values from the given module.
            Uses update_with_dict() behind the scenes.
        """
        return self.update_with_dict(module.__dict__)

    @classmethod
    def from_module(cls, module):
        """
            Create an instance of SettingsContainer with values based
            on the one in the passed module.
        """
        settings = cls()
        settings.update_with_module(module)
        return settings

    def update_with_file(self, filepath):
        """
            Update settings with values from the given module file.
            Uses update_with_dict() behind the scenes.
        """
        settings = run_path(filepath)
        return self.update_with_dict(settings)


settings = SettingsContainer()


def to_ascii(utext):
    """ Take a unicode string and return ascii bytes.

        Try to replace non ASCII char by similar ASCII char. If it can't,
        replace it with "?".
    """
    return unicodedata.normalize("NFKD", utext).encode("ascii", "replace")


# Make sure to always specify encoding when using open in Python 2 or 3
safe_open = partial(codecs.open, encoding="utf8")


def as_unicode(obj):
    """ Return the unicode representation of an object """
    try:
        return unicode(obj)
    except NameError:
        return str(obj)


def ensure_var_env():
    """ Ensure all the variable things we generate are available.

        This will make sure we have:

        - a var dir
        - a content dir
        - a secret key
        - an admin URL
    """

    settings.VAR_DIR.mkdir(exist_ok=True, parents=True)
    settings.PASTE_FILES_ROOT = settings.VAR_DIR / "content"
    settings.PASTE_FILES_ROOT.mkdir(exist_ok=True)
    settings.SESSIONS_DIR = settings.VAR_DIR / "sessions"
    settings.SESSIONS_DIR.mkdir(exist_ok=True)

    secret_key_file = settings.VAR_DIR / "secret_key"
    if not secret_key_file.is_file():
        secret_key_file.write_text(secrets.token_urlsafe(64))
    settings.SECRET_KEY = secret_key_file.read_text()

    admin_password_file = settings.VAR_DIR / "admin_password"
    if not secret_key_file.is_file():
        admin_password_file.write_text(
            "No password set. Use the set_admin_passord command. Don't write this file by hand."
        )
    settings.ADMIN_PASSWORD_FILE = admin_password_file

    payload = ("admin" + settings.SECRET_KEY).encode("ascii")
    settings.ADMIN_URL = "/admin/" + hashlib.sha256(payload).hexdigest() + "/"


def hash_password(password):
    return hashlib.scrypt(
        password.encode("utf8"),
        salt=settings.SECRET_KEY.encode("ascii"),
        n=16384,
        r=8,
        p=1,
        dklen=32,
    )


def check_password(password):
    try:
        return settings.ADMIN_PASSWORD_FILE.read_bytes() == hash_password(password)
    except (FileNotFoundError, AttributeError):
        return False

