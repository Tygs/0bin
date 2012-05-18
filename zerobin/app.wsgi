
import os, sys

# make sure the zerobin module is in the PYTHON PATH and importable
ZEROBIN_PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, ZEROBIN_PARENT_DIR)

# create the wsgi callable
from zerobin.routes import get_app
settings, application = get_app(compressed_static=True)