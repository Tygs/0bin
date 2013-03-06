============
Options
============

0bin's behavior can be adjusted with options passed using a configuration
file or directly using the command line. Some parameters are only available
in the configuration file.

If an option is not passed, 0bin will use the default value from the file
zerobin/default_settings.py.


Command line
==================

--host and --port
-------------------

The host and port on which to listen for incomming request. Usually 127.0.0.1
and 8000 to listen locally or 0.0.0.0 and 80 to listen from the outside.

Default: 127.0.0.1 and 8000

Setting file : HOST and PORT


--debug
----------

Display a listing of useful debugging information when something goes wrong
instead of showing the 500 error page.

In debug mode, the server also reload automatically any modified Python file;

Default: False

Configuration file equivalent: DEBUG

.. _user-and-group-en:

--user and --group
-------------------

The user and group the server will adopt after start up.

Useful when you run the command with admin rights to be able to listen to the
port 80, but you wish that the process do not have access to protected files.

--group is set to --user if not passed.

Default: None

Configuration file equivalent: USER and GROUP

--settings-file
-----------------

Path to the configuration file, if you use any.

Default: None

Configuration file equivalent: None


--compressed-static
--------------------

Serve minified static files (css and js). Use it in production to get a faster
web site.

Default: False

Configuration file equivalent: COMPRESSED_STATIC_FILES

--version and --help
--------------------

Display the help or the version of 0bin.

Default: None

Configuration file equivalent: None

Examples
----------

Production::

  sudo zerobin --host 0.0.0.0 --port 80 --user foo --compressed-static

Developpement::

  zerobin --debug --serve-static


Configuration file
====================

The configuration file should be an ordinary Python file, usually named
settings.py. It's used this way::

  zerobin --settings-file '/path/to/settings.py'

Any options passed to the command line will have priority on the ones in
the configuration file. The zerobin/default_settings.py can be used as an
example to create your own file. It's heavily commented.


DEBUG
-----

Display a listing of useful debugging information when something goes wrong
instead of showing the 500 error page.

In debug mode, the server also reload automatically any modified Python file;


Default: False

Command line equivalent: --debug

.. _static-root-en:

STATIC_FILES_ROOT
------------------

Asbolute path to the directory where 0bin is going to look for static files
(css, js and images).

Default:  "static" directory in the "zerobin" directory

Command line equivalent: None

COMPRESSED_STATIC_FILES
-------------------------

Serve minified static files (css and js). Use it in production to get a faster
web site.

Default: False

Command line equivalent: --compressed-static

PASTE_FILES_ROOT
-----------------

Absolute path to the directory in which 0bin is going to look save pastes.

Default: "static/content" direcotry in the "zerobin" directory

Command line equivalent: None

.. _template-dirs-en:

TEMPLATE_DIRS
--------------

List of absolute path to directories containing templates that 0bin uses to
generate the web site pages. The first list items have priotity on the later.

If you wish to use your own templates, add the directory containing them
at the beginning of the list::

  from zerobin.defauls_settings import TEMPLATE_DIRS

  TEMPLATE_DIRS = (
      '/directy/path/to/your/templates',
  ) + TEMPLATE_DIRS

Default:  "view" directory in the "zerobin" directory

Command line equivalent: None

HOST and PORT
-------------------


The host and port on which to listen for incomming request. Usually 127.0.0.1
and 8000 to listen locally or 0.0.0.0 and 80 to listen from the outside.

Default: 127.0.0.1 and 8000

Configuration file equivalent: --host and --port

USER and GROUP
-------------------

The user and group the server will adopt after start up.

Useful when you run the command with admin rights to be able to listen to the
port 80, but you wish that the process do not have access to protected files.

GROUP is set to USER if not passed.

Default: None

Configuration file equivalent: --user and --group

MENU
------

A list of 'name' + 'link' pairs used to buld the menu at the top of each page.

You can use a relative or absolute link, and even an email address.

Any email address will be automatically protected against spam.

Default::

  MENU = (
      ('Home', '/'),
      ('Download 0bin', 'https://github.com/sametmax/0bin'),
      ('Contact', 'mailto:your@email.com') # email
  )


Command line equivalent: None

MAX_SIZE
---------

Approximative value for a paste size limite.

Valeur approximative de limite de taille d'un paste.

Default = 500000 octets (500 ko)

Command line equivalent: None
