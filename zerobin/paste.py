import os
import hashlib
import base64
import lockfile
import json

from datetime import datetime, timedelta

import bleach

from zerobin.utils import settings


class Paste(object):
    """
        A paste object to deal with the file opening/parsing/saving and the
        calculation of the expiration date.
    """

    DIR_CACHE: set = set()

    DURATIONS = {
        "1_day": 24 * 3600,
        "1_month": 30 * 24 * 3600,
        "never": 365 * 24 * 3600 * 100,
    }

    def __init__(
        self,
        uuid=None,
        uuid_length=None,
        content=None,
        expiration=None,
        title="",
        btc_tip_address="",
    ):

        self.content = content
        self.expiration = self.get_expiration(expiration)
        self.title = bleach.clean(title, strip=True)[:60]
        self.btc_tip_address = bleach.clean(btc_tip_address, strip=True)[:50]

        if not uuid:
            # generate the uuid from the decoded content by hashing it
            # and turning it into base64, with some characters strippped
            uuid = hashlib.sha1(self.content.encode("utf8"))
            uuid = base64.b64encode(uuid.digest()).decode()
            uuid = uuid.rstrip("=\n").replace("/", "-")

            if uuid_length:
                uuid = uuid[:uuid_length]
        self.uuid = uuid

    def get_expiration(self, expiration):
        """
            Return a date at which the Paste will expire
            or if it should be destroyed after first reading.

            Do not modify the value if it's already a date object or
            if it's burn_after_reading
        """

        try:
            return datetime.now() + timedelta(seconds=self.DURATIONS[expiration])
        except KeyError:
            return expiration

    @classmethod
    def build_path(cls, *dirs):
        """
            Generic static content path builder. Return a path to
            a location in the static content file dir.
        """
        return os.path.join(settings.PASTE_FILES_ROOT, *dirs)

    @classmethod
    def get_path(cls, uuid):
        """
            Return the file path of a paste given uuid
        """
        return cls.build_path(uuid[:2], uuid[2:4], uuid)

    @property
    def path(self):
        """
            Return the file path for this path. Use get_path().
        """
        return self.get_path(self.uuid)

    @property
    def owner_key(self):
        """
            Return a key that gives you admin rights on this paste
        """
        payload = (settings.SECRET_KEY + self.uuid).encode("ascii")
        return hashlib.sha256(payload).hexdigest()

    @classmethod
    def load_from_file(cls, path):
        """
            Return an instance of the paste object with the content of the
            given file.
        """
        try:
            with open(path) as paste:
                uuid = os.path.basename(path)
                expiration = next(paste).strip()
                content = next(paste).strip()
                try:
                    metadata = json.loads(next(paste).strip())
                except (StopIteration, json.decoder.JSONDecodeError):
                    metadata = {}
                if "burn_after_reading" not in expiration:
                    expiration = datetime.strptime(expiration, "%Y-%m-%d %H:%M:%S.%f")

        except StopIteration:
            raise TypeError("File %s is malformed" % path)
        except (IOError, OSError):
            raise ValueError("Can not open paste from file %s" % path)

        return Paste(
            uuid=uuid,
            expiration=expiration,
            content=content,
            title=" ".join(metadata.get("title", "").split()),
            btc_tip_address=" ".join(metadata.get("btc_tip_address", "").split()),
        )

    @classmethod
    def load(cls, uuid):
        """
            Return an instance of the paste object with the content of the
            file matching this uuid. Use load_from_file() and get_path()
        """
        return cls.load_from_file(cls.get_path(uuid))

    def increment_counter(self):
        """
            Increment pastes counter.

            It uses a lock file to prevent multi access to the file.
        """
        path = settings.PASTE_FILES_ROOT
        counter_file = os.path.join(path, "counter")

        with lockfile.LockFile(counter_file):
            # Read the value from the counter
            try:
                with open(counter_file, "r") as fcounter:
                    counter_value = int(fcounter.read(50)) + 1
            except (ValueError, IOError, OSError):
                counter_value = 1

            # write new value to counter
            with open(counter_file, "w") as fcounter:
                fcounter.write(str(counter_value))

    def save(self):
        """
            Save the content of this paste to a file.
        """
        head, tail = self.uuid[:2], self.uuid[2:4]

        # the static files are saved in project_dir/static/xx/yy/uuid
        # xx and yy are generated from the uuid (see get_path())
        # we need to check if they are created before writting
        # but since we want to prevent too many writes, we create
        # an in memory cache that will hold the result of this check for
        # each worker. If the dir is not in cache, we check the FS, and
        # if the dir is not in there, we create the dir
        if head not in self.DIR_CACHE:

            self.DIR_CACHE.add(head)

            if not os.path.isdir(self.build_path(head)):
                os.makedirs(self.build_path(head, tail))
                self.DIR_CACHE.add((head, tail))

        if (head, tail) not in self.DIR_CACHE:
            path = self.build_path(head, tail)
            self.DIR_CACHE.add((head, tail))
            if not os.path.isdir(path):
                os.mkdir(path)

        # add a timestamp to burn after reading to allow
        # a quick period of time where you can redirect to the page without
        # deleting the paste
        if "burn_after_reading" == self.expiration:
            expiration = self.expiration + "#%s" % datetime.now()  # TODO: use UTC dates
        else:
            expiration = str(self.expiration)

        # write the paste
        with open(self.path, "w") as f:
            f.write(expiration + "\n")
            f.write(self.content + "\n")
            metadata = {}
            if self.title:
                metadata["title"] = self.title
            if self.btc_tip_address:
                metadata["btc_tip_address"] = self.btc_tip_address
            f.write(json.dumps(metadata) + "\n")

        return self

    @classmethod
    def get_pastes_count(cls):
        """
            Return the number of created pastes.
            (must have option DISPLAY_COUNTER enabled for the pastes to be
             be counted)
        """
        counter_file = os.path.join(settings.PASTE_FILES_ROOT, "counter")
        try:
            count = int(open(counter_file).read(50))
        except (IOError, OSError):
            count = 0

        return "{0:,}".format(count)

    @property
    def humanized_expiration(self):
        """
            Return the expiration date in a human friendly format.

            In 3 minutes, or in 3 days or the 23/01/2102
        """
        try:
            expiration = self.expiration - datetime.now()
            # in_seconds doesn't exist in python 2.6
            expiration = expiration.days * 24 * 60 * 60 + expiration.seconds

        except TypeError:
            return None

        if expiration < 60:
            return "in %s s" % expiration

        if expiration < 60 * 60:
            return "in %s m" % int(expiration / 60)

        if expiration < 60 * 60 * 24:
            return "in %s h" % int(expiration / (60 * 60))

        if expiration < 60 * 60 * 24 * 10:
            return "in %s days(s)" % int(expiration / (60 * 60 * 24))

        return "the %s" % self.expiration.strftime("%m/%d/%Y")

    def delete(self):
        """
            Delete the paste file.
        """
        os.remove(self.path)

    @classmethod
    def iter_all(cls, on_error=lambda e: e):
        for p in settings.PASTE_FILES_ROOT.rglob("*"):
            if p.is_file() and "counter" not in str(p):
                try:
                    yield Paste.load_from_file(p)
                except (TypeError, ValueError) as e:
                    on_error(e)

    @property
    def has_expired(self):
        try:
            return self.expiration < datetime.now()
        except TypeError:
            return False
