from zerobin import ROOT_DIR

# Path to the directory that will contains all variable content, such
# as pastes, the secret key, etc
VAR_DIR = ROOT_DIR.parent / "var"

# debug will get you error messages and auto reload
# don't set this to True in production
DEBUG = False

# Should the application serve static files on it's own ?
# If yes, set the absolute path to the static files.
# If no, set it to None
# In dev this is handy, in prod you probably want the HTTP servers
# to serve it, but it's OK for small traffic to set it to True in prod too.
STATIC_FILES_ROOT = ROOT_DIR / "static"

# If True, will link the compressed verion of the js and css files,
# otherwise, will use the ordinary files
COMPRESSED_STATIC_FILES = False

# A tuple of absolute paths of directory where to look the template for
# the first one will be the first to be looked into
# if you want to override, it needs to be it a directory at the begining of
# this tuple. By default, custom_views is meant for that purpose.
TEMPLATE_DIRS = (
    VAR_DIR / "custom_views",
    ROOT_DIR / "views",
)

# Port and host the embeded python server should be using
# You can also specify them using the --host and --port script options
# which have priority on these settings
HOST = "127.0.0.1"
PORT = "8000"

# User and group the server should run as. Set to None if it should be the
# current user. Some OS don't support it and if so, it will be ignored.
USER = None
GROUP = None

# Display a tiny counter for pastes created.
# Be carreful if your site have to many pastes this can hurt your hard drive performances.
# Refresh counter interval. Default to every minute after a paste.
DISPLAY_COUNTER = True
REFRESH_COUNTER = 60 * 1  # Fill this if you want to
ADMIN_CREDENTIALS = {
    "username": None,
    "password": None,
}


# Names/links to insert in the menu bar.
# Any link with "mailto:" will be escaped to prevent spam
MENU = (
    ("Home", "/"),  # internal link. First link will be highlited
    ("Download 0bin", "https://github.com/sametmax/0bin"),  # external link
    ("Faq", "/faq/"),  # faq
    ("Contact", "mailto:your@email.com"),  # email
)

# limit size of pasted text in bytes. Be careful allowing too much size can
# slow down user's browser
MAX_SIZE = 1024 * 500

# length of base64-like paste-id string in the url, int from 4 to 27 (length of sha1 digest)
# total number of unique pastes can be calculated as 2^(6*PASTE_ID_LENGTH)
# for PASTE_ID_LENGTH=8, for example, it's 2^(6*8) = 281 474 976 710 656
PASTE_ID_LENGTH = 8

