# -*- coding: utf-8 -*-

import os
import hashlib
import locale

from datetime import datetime, timedelta

from utils import settings


class Paste(object):
    """
        A paste objet to deal with the file opening/parsing/saving and the
        calculation of the expiration date.
    """

    DIR_CACHE = set()

    DURATIONS = {
        u'1_day': 24 * 3600,
        u'1_month': 30 * 24 * 3600,
        u'never': 365 * 24 * 3600 * 100,
    }


    def __init__(self, uuid=None, uuid_length=None,
                 content=None, expiration=None):

        self.content = content
        self.expiration = expiration

        if isinstance(self.content, unicode):
            self.content = self.content.encode('utf8')

        self.expiration = self.get_expiration(expiration)

        if not uuid:
            uuid = hashlib.sha1(self.content)\
                .digest().encode('base64').rstrip('=\n').replace('/', '-')
            if uuid_length: uuid = uuid[:uuid_length]
        self.uuid = uuid


    def get_expiration(self, expiration):
        """
            Return a tuple with the date at which the Paste will expire
            or if it should be destroyed after first reading.

            Do not modify the value if it's already a date object or
            if it's burn_after_reading
        """

        if (isinstance(expiration, datetime) or
                self.is_burn_notice):
            return expiration

        try:
            return datetime.now() + timedelta(seconds=self.DURATIONS[expiration])
        except KeyError:
            return u'burn_after_reading'


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


    @classmethod
    def load_from_file(cls, path):
        """
            Return an instance of the paste object with the content of the
            given file.
        """
        try:
            paste = open(path)
            uuid = os.path.basename(path)
            expiration = paste.next().strip()
            content = paste.next().strip()
            if "burn_after_reading" not in str(expiration):
                expiration = datetime.strptime(expiration, '%Y-%m-%d %H:%M:%S.%f')

        except StopIteration:
            raise TypeError(u'File %s is malformed' % path)
        except (IOError, OSError):
            raise ValueError(u'Can not open paste from file %s' % path)

        return Paste(uuid=uuid, expiration=expiration, content=content)


    @classmethod
    def load(cls, uuid):
        """
            Return an instance of the paste object with the content of the
            file matching this uuid. Use load_from_file() and get_path()
        """
        return cls.load_from_file(cls.get_path(uuid))


    def increment_counter(self):
        """
            Increment pastes counter
        """

        # simple counter incrementation
        # using lock file to prevent multi access to the file
        # could be improved.


        path = settings.PASTE_FILES_ROOT
        counter_file = os.path.join(path, 'counter')
        lock_file = os.path.join(path, 'counter.lock')

        if not os.path.isfile(lock_file):
            try:
                #make lock file
                flock = open(lock_file, "w")
                flock.write('lock')
                flock.close()

                # init counter (first time)
                if not os.path.isfile(counter_file):
                    fcounter = open(counter_file, "w")
                    fcounter.write('1')
                    fcounter.close()

                # get counter value
                fcounter = open(counter_file, "r")
                counter_value = fcounter.read(50)
                fcounter.close()

                try:
                    counter_value = long(counter_value) + 1
                except ValueError:
                    counter_value = 1

                # write new value to counter
                fcounter = open(counter_file, "w")
                fcounter.write(str(counter_value))
                fcounter.close()

                #remove lock file
                os.remove(lock_file)
            finally:
                if os.path.isfile(lock_file):
                    #remove lock file
                    os.remove(lock_file)



    def save(self):
        """
            Save the content of this paste to a file.
        """
        head, tail = self.uuid[:2], self.uuid[2:4]

        # the static files are saved in project_dir/static/xx/yy/uuid
        # xx and yy are generated from the uuid (see get_path())
        # we need to check if they are created before writting
        # but since we want to prevent to many writes, we create
        # an in memory cache that will hold the result of this check fo
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
        if self.expiration == "burn_after_reading":
            self.expiration = self.expiration + '#%s' % datetime.now()

        # write the paste
        with open(self.path, 'w') as f:
            f.write(unicode(self.expiration) + '\n')
            f.write(self.content + '\n')

        return self


    @classmethod
    def get_pastes_count(cls):
        """
            Return the number of created pastes.
            (must have option DISPLAY_COUNTER enabled for the pastes to be
             be counted)
        """
        try:
            locale.setlocale(locale.LC_ALL, 'en_US')
        except:
            pass
        counter_file = os.path.join(settings.PASTE_FILES_ROOT, 'counter')
        try:
            count = long(open(counter_file).read(50))
        except (IOError, OSError):
            count = 0

        return locale.format("%d", long(count), grouping=True)


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
            return 'in %s s' % expiration

        if expiration < 60 * 60:
            return 'in %s m' % int(expiration / 60)

        if expiration < 60 * 60 * 24:
            return 'in %s h' % int(expiration / (60 * 60))

        if expiration < 60 * 60 * 24 * 10:
            return 'in %s days(s)' % int(expiration / (60 * 60 * 24))

        return 'the %s' % self.expiration.strftime('%m/%d/%Y')


    def delete(self):
        """
            Delete the paste file.
        """
        os.remove(self.path)

    @property
    def is_alive(self):
        """
        Return True if the paste is alive.
        False if it may be deleted
        """
        now = datetime.now()
        # keep alive false by default
        keep_alive = False
        # Delete the paste if it expired:
        if self.is_burn_notice:
            # burn_after_reading contains the paste creation date
            # if this read appends 10 seconds after the creation date
            # we don't delete the paste because it means it's the redirection
            # to the paste that happens during the paste creation
            try:
                keep_alive = self.expiration.split('#')[1]
                keep_alive = datetime.strptime(keep_alive,
                                               '%Y-%m-%d %H:%M:%S.%f')
                keep_alive = now < keep_alive + timedelta(seconds=10)
            except IndexError:
                keep_alive = False
        else:
            keep_alive = now < self.expiration

        return keep_alive


    @classmethod
    def purge(cls, path=settings.PASTE_FILES_ROOT):
        """
            Purge the content folder
            Return the number of paste deleted.
        """
        # we don't want to read 'counter' files
        ignore_files = ['counter', ]
        # keep a count on purged pastes
        deleted_paste = 0

        if os.path.exists(path):
            for folder, _ , files in os.walk(path):
                for fname in files:
                    if fname in ignore_files:
                        continue
                    if Paste._purge_file(os.path.join(folder, fname)):
                        deleted_paste += 1
        return deleted_paste

    @property
    def is_burn_notice(self):
        return  'burn_after_reading' in str(self.expiration)

    @classmethod
    def _purge_file(cls, fname):
        """
            Purges the given file if expired.
        """
        paste = Paste.load_from_file(fname)
        # Burn after reading will always returns paste.is_alive == False
        # We don't want to kill them now
        if not paste.is_burn_notice and not paste.is_alive:
            paste.delete()
            return True
        return False

