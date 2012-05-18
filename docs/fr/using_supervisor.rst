====================
Utiliser supervisor
====================

Supervisor est un très bon moyen de gérer des processus Python. Nous n'allons
pas couvrir son installation (qui la plupart du temps se résume à
apt-get install supervisor ou pip install supervisor), mais voici un rapide
résumé de comment l'utiliser:

Créez un fichier de configuration nommé supervisor.ini::

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
    command=/chemin/vers/zerobin/zerobin.py --port 80 --compressed-static
    directory=/chemin/vers/zerobin/
    environment=PYTHONPATH='/chemin/vers/zerobin/'
    user=zerobin
    autostart=true
    autorestart=true

Les 4 premières entrées sont juste de la configuration standard et vous pouvez
les copier telles qu'elles.

La dernière entrée définie un processus (il peut y en avoir plusieurs)
que supervisor doit gérer.

Cela veut dire qu'il va lancer la commande::

     /chemin/vers/zerobin/zerobin.py --port 80 --compressed-static

Et ceci dans le dossier, avec l'environnement et l'utilisateur défini, le tout
en arrière plan en tant que daemon.

`autostart` et `autorestart` permettent simplement de le lancer et de l'oublier:
supervisor redémarera le processus automatiquement en cas d'arrêt impromptu.

La première fois que vous lancez supervisor, passez lui le fichier de configuration::

    supervisord -c /chemin/vers/supervisor.ini

Ensuite vous pouvez gérer les processus avec::

    supervisorctl -c /chemin/vers/supervisor.ini

Cela va démarrer un shell depuis lequel vous pouvez faire un start/stop/restart
sur le service.

Toutes les erreurs seront logguées dans /tmp/zerobin.log.


.. Note::

    Si vous avez installé zerobin dans un virtualenv, vous devriez définir la
    commande pour qu'elle s'éxécute depuis le virtualenv::

        command=/chemin/vers/le/virtualenv/bin/zerobin --port 80 --compressed-static