from zerobin.paste import Paste
from clize import run
import re

paste_url = re.compile('/paste/(?P<paste_id>.*)#(?P<key>.*)')

def unpack_paste(paste):
    """Take either the ID or the URL of a paste, and return its ID"""

    try_url = paste_url.search(paste)

    if try_url:
        return try_url.group('paste_id')
    return paste


def remove_paste(*paste_list, quiet:'q'=False):
    """
    Remove pastes, given its ID or its URL

    paste_list: Liste of paste, given by ID or URL

    quiet: Don't print anything
    """

    for paste_uuid in map(unpack_paste, paste_list):
        try:
            Paste.load(paste_uuid).delete()
        
        except ValueError:
            if not quiet:
                print('Paste {} doesn\'t exist'.format(paste_uuid))

        else:
            if not quiet:
                print('Paste {} is removed'.format(paste_uuid))

def main():
    run(remove_paste)

if __name__ == "__main__":
    main()
