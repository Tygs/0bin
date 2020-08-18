from zerobin.routes import get_app

# Remember you can set the following environment variables to configure
# how get_app() setup the 0bin:
#
# - ZEROBIN_DEBUG =
# - ZEROBIN_DATA_DIR
# - ZEROBIN_CONFIG_DIR

settings, app = get_app()
