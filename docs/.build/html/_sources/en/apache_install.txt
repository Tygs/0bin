=============
Apache setup
=============

.. Note::
    You need to have followed the :doc:`easy install <./easy_install>` first.

Apache is heavier than :doc:`Nginx <./nginx_install>`. But it's also much more famous:

- more people will be able to help you on forums;
- your hosting will most probably support Apache;
- the configuration file syntax is familiar to a lot of people.

An Apache setup is still much more robust and secure than an easy installation.

Une installation apache est aussi beaucoup plus solide et sécurisé qu'une
installation facile. You'll benefit from having:

- the possibility to have several projects listening to the port 80;
- several Apache module at your disposal (like requests throttling);
- Apache robustness in front end: it's secure, and there is much less chance
  it will crash under heavy load;
- your web site processes won't run with admin rights, even if
  :ref:`--user <user-and-group-en>` doesn't
  work on your OS.


Mod_wsgi
==========

The modern Web Python servers all work the same way, following an norm for
interfacing: WSGI.

This is the most performante solution, and the best to use. But it will require
the setup of the Apache module mod_wsgi. If you don't know how to do this, or
if you can't do it (E.G: your hosting won't let you), you need to go for
the CGI setup.

First, make sure you have mod_wsgi installed and enable by running (as admin)::

    a2enmod wsgi

This enable mod_wsgi. It it doesn't, install it first (on ubuntu, the package
is libapache2-mod-wsgi).

Then create an Apache configuration file, usually in /etc/apache/sites-available/.
Name it zerobin::

    <VirtualHost *:80>
        ServerName www.yourwebsite.com

        WSGIDaemonProcess zerobin user=www-data group=www-data processes=1 threads=5
        WSGIScriptAlias / /path/to/zerobin/app.wsgi

        <Directory /path/to/zerobin/zerobin/>
            WSGIProcessGroup zerobin
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>
    </VirtualHost>

Activate the website (as admin)::

    a2ensite zerobin

And reload the apache configuration (as admin)::

    service apache2 reload

You'll note that we refer to a file named app.wsgi. It's a Python file
creating the application Apache is going to use to start the Python process::

    import os, sys

    # make sure the zerobin module is in the PYTHON PATH and importable
    ZEROBIN_PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, ZEROBIN_PARENT_DIR)

    # create the wsgi callable
    from zerobin.routes import get_app
    settings, application = get_app(compressed_static=True)

You can of course create your own, as the `get_app` function is the only
way to pass settings to 0bin with this setup. You would do this by creating
a configuration file and passing it to the function::

    import os, sys

    ZEROBIN_PARENT_DIR = '/path/to/zerobin/parent/dir'
    sys.path.insert(0, ZEROBIN_PARENT_DIR)

    from zerobin.routes import get_app
    settings, application = get_app(settings_file='/path/to/settings.py')

CGI
===

You can also run 0bin using CGI, but infortunaly we didn't have time to cover
it yet. Please contact us if you ever get the need to use it.
