==============================
zerobinpaste command-line tool
==============================

zerobinpaste is a simple CLI tool (analogous to pastebinit or wgetpaste) to use
with files or shell redirection in terminal or simple scripts.

Example use-cases might look like::

    % zerobinpaste README.rst
    http://some.0bin.site/paste/0cc3d8a8...

    % grep error /var/log/syslog | zerobinpaste
    http://some.0bin.site/paste/81fd1324...

    % zerobinpaste docs/en/*.rst
    easy_install.rst http://some.0bin.site/paste/9adc576a...
    apache_install.rst http://some.0bin.site/paste/01408cbd...
    options.rst http://some.0bin.site/paste/921b2768...
    ...


    % ps axlf | zerobinpaste | mail -s "Process tree on $(date)" root

Produced links can then be copy-pasted to some IRC channel or used in whatever
other conceivable way.

Tool does encryption by itself on the client machine and key (after hashmark) is
never sent to server or anywhere but the tool's stdout stream (e.g. terminal).

Tool has to be built with `node.js`_ separately (see below).


Usage
=====

At least the pastebin site (main URL where you'd paste stuff with the browser)
has to be specified for the tool to use either via -u (--url) option (can be
simplified with shell alias - e.g. ``alias zp='zerobinpaste -u http://some.0bin.site``)
or in the "~/.zerobinpasterc" configuration file (json format).

| Non-option arguments are interpreted as files to upload/paste contents of.
| If no arguments are specified, data to paste will be read from stdin stream.

Simple configuration file may look like this:

    {"url": "http://some.0bin.site"}

Any options (in the long form, e.g. "url" for --url above) that are allowed on
the command-line can be specified there.

Run the tool with -h or --help option to see full list of supported parameters.


Build / Installation
====================

In essence:

		0bin% cd tools
		0bin/tools% make
		...
		0bin/tools% cp zerobinpaste ~/bin   # install to PATH

"npm" binary (packaged and installed with node.js) is required to pull in build
dependencies, if necessary, and "node" binary is required for produced binary to
run.

Use "make" in "tools" path to produce non-minified runnable "zerobinpaste"
script there.

``make ugly`` command can be used instead of ``make`` to create "minified"
version (using/installing uglifyjs_, about 25% smaller in size).

Resulting "zerobinpaste" script requires only node.js ("node" binary) installed
to run and can be placed in any of the PATH dirs (e.g. "~/bin",
"/usr/local/bin") to be run just as "zerobinpaste".


Why node.js and not python
==========================

Unfortunately, it's fairly complex and unreliable to replicate non-trivial and
undocumented encryption protocol that SJCL_ convenience methods employ, and any
mistake in encryption is guaranteed to produce unreadable paste.

Current implementation uses same JavaScript code (and V8 node.js engine) that
browsers do, hence can be fairly simple and robust.

Future development plans include supporting configurable, less complex and more
widespread encryption schemas, allowing for simplier non-javascript client as
well.

See `related pull request`_ for more details.


.. _node.js: http://nodejs.org/
.. _uglifyjs: https://github.com/mishoo/UglifyJS
.. _SJCL: http://crypto.stanford.edu/sjcl/
.. _related pull request: https://github.com/sametmax/0bin/pull/39
