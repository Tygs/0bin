#!/usr/bin/env python
# coding: utf-8

from zerobin.paste import Paste
from sigtools.modifiers import annotate, autokwoargs
from clize import run
import re

# The regex parse the url and separate the paste's id from the decription key
# After the '/paste/' part, there is several caracters, identified as
# the uuid of the paste. Followed by a '#', the decryption key of the paste.
paste_url = re.compile('/paste/(?P<paste_id>.*)#(?P<key>.*)')

def unpack_paste(paste):
    """Take either the ID or the URL of a paste, and return its ID"""

    try_url = paste_url.search(paste)

    if try_url:
        return try_url.group('paste_id')
    return paste

@annotate(quiet='q')
@autokwoargs
def remove_paste(quiet=False, *pastes):
    """
    Remove pastes, given its ID or its URL

    quiet: Don't print anything

    pastes: List of pastes, given by ID or URL
    """

    for paste_uuid in map(unpack_paste, pastes):
        try:
            Paste.load(paste_uuid).delete()

            if not quiet:
                print('Paste {} is removed'.format(paste_uuid))
        
        except ValueError:
            if not quiet:
                print('Paste {} doesn\'t exist'.format(paste_uuid))


def main():
    run(remove_paste)

if __name__ == "__main__":
    main()
