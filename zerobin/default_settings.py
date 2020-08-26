# Get error messages and auto reload.
# Don't set this to True in production
DEBUG = False

# Port and host for the embedded python server
HOST = "127.0.0.1"
PORT = "3255"

# Names/links to insert in the footer.
#
MENU = (
    ("Github", "https://github.com/Tygs/0bin"),
    ("Faq", "/faq/"),  # You probably want to keep this
    # Any link with "mailto:" will be escaped to limit spam, but displayed
    # correctly to the user using JS.
    ("Contact", "mailto:your@email.com"),
    ("Zerobin Pastebin", "https://www.0bin.net/"),  # Thanks the authors :)
    ("How to buy Bitcoin?", "/buy_bitcoin"),  # Thanks the authors :)
)

# Size limit of the paste content in bytes. Be careful, allowing a size too big can
# slow down the user's browser
MAX_SIZE = 1024 * 1000

# Display a tiny counter for pastes created.
DISPLAY_COUNTER = True
# Refresh counter interval.
REFRESH_COUNTER = 60  # in seconds

# Length of the paste-id string in the url, int from 4 to 27 (length of sha1 digest)
# total number of unique pastes can be calculated as 2^(6*PASTE_ID_LENGTH)
# for PASTE_ID_LENGTH=8, for example, it's 2^(6*8) = 281 474 976 710 656
PASTE_ID_LENGTH = 8
