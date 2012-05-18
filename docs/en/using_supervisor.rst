=================
Using supervisor
=================

Supervisor is a very nice way to manage you Python processes. We won't cover
the setup (which is just apt-get install supervisor or pip install supervisor
most of the time), but here is a quick overview on how to use it.

Create a configuration file named supervisor.ini::

    [unix_http_server]
    file=/tmp/supervisor.sock;

    [supervisorctl]
    serverurl=unix:///tmp/supervisor.sock;

    [rpcinterface:supervisor]
    supervisor.rpcinterface_factory=supervisor.rpcinterface:make_main_rpcinterface

    [supervisord]
    logfile=/tmp/zerobin.log
    logfile_maxbytes=50MB
    logfile_backups=2
    loglevel=trace
    pidfile=/tmp/supervisord.pid
    nodaemon=false
    minfds=1024
    minprocs=200
    user=zerobin

    [program:zerobin]
    command=/path/to/zerobin/zerobin.py --port 80 --compressed-static
    directory=/path/to/zerobin/
    environment=PYTHONPATH='/path/to/zerobin/'
    user=zerobin
    autostart=true
    autorestart=true

The 4 first entries are just boiler plate to get you started, you can copy
them verbatim.

The last one define one (you can have many) process supervisor should manage.

It means it will run the command::

     /path/to/zerobin/zerobin.py --port 80 --compressed-static

In the directory, with the environnement and the user you defined.

This command will be ran as a daemon, in the background.

`autostart` and `autorestart` just make it fire and forget: the site will always be
running, even it crashes temporarly or if you retart the machine.

The first time you run supervisor, pass it the configuration file::

    supervisord -c /path/to/supervisor.ini

Then you can manage the process by running::

    supervisorctl -c /path/to/supervisor.ini

It will start a shell from were you can start/stop/restart the service

You can read all errors that might occurs from /tmp/zerobin.log.

.. Note::

    If you installed zerobin in a virtualenv, you may set the command
    to run directly from it::

        command=/path/to/virtualenv/bin/zerobin --port 80 --compressed-static