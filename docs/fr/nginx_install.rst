========================
Installation avec Nginx
========================

.. Note::
    Vous devez avoir suivi :doc:`l'installation facile <./easy_install>` avant.

Nginx est un choix très populaire pour servir un projet Python :

- Il est rapide.
- Il est léger.
- Les fichiers de configuration sont très simples.

Si vous avez votre propre serveur, c'est le meilleur choix. Dans le cas contraire,
essayez  :doc:`l'installation la plus simple <./easy_install>`,
ou avec :doc:`Apache <./apache_install>`.

Nginx ne lance aucun processus Python, il sert uniquement les requêtes
depuis l'extérieur vers le serveur Python.

Il y a donc deux étapes :

- Faire tourner le processus Python.
- Faire tourner Nginx.

Ainsi, vous bénéficierez :

- de la possibilité d'avoir plusieurs projets écoutant sur le port 80 ;
- de plusieurs modules Nginx à votre disposition (comme la limitation
  du nombre de requêtes) ;
- de la solidité de Nginx en front end: il est sécurité, et il y a peu de chance
  qu'il crash sous une forte charge ;
- les processus de votre site ne tournent pas avec les droits admin, même si
  --user ne fonctionne pas sur votre OS ;
- de la capacité de gérer un processus Python sans toucher Nginx ou les autres
  processus. C'est très pratique pour les mises à jour.

Processus Python
==================

Lancez 0bin, comme d'habitude, mais cette fois pour écouter sur un host et un port
local. Ex : ::

    zerobin --host 127.0.0.1 --port 8000

En PHP, quand on édite un fichier, la modificiation est visible immédiatement.
En Python, l'intégralité du code est chargé en mémoire pour des raisons de
performance. Pour cette raison, il faut redémarrer le processus Python pour voir
les changement prendre effet. Avoir un processus séparé permet de le faire
sans avoir à redémarer le serveur.


Nginx
======

Nginx peut être installé avec votre gestionnaire de paquets habituels, donc
nous ne couvrirons pas cette partie.

Vous devez créer un fichier de configuration Nginx pour 0bin. Sous GNU/Linux,
on les met en général dans /etc/nginx/conf.d/. Nommez-le zerobin.conf.

Le fichier de configuration minimal pour faire tourner le site est : ::

    server {
        listen       80;
        server_name www.votresiteweb.com;

        location / {
            proxy_pass http://127.0.0.1:8000;
        }
    }

`proxy_pass` transmet les requêtes aux processus Python. Bien entendu le
port doit correspondre à celui utilisé par 0bin.

On peut apporter plusieurs améliorations à l'expérience utilisateur : ::

    server {
        listen       80;
        server_name www.votresiteweb.com;

        location /favicon.ico {
            root  /chemin/vers/zerobin/static/img;
        }

        location /static/ {
            root  /chemin/vers/zerobin;
            gzip  on;
            gzip_http_version 1.0;
            gzip_vary on;
            gzip_comp_level 6;
            gzip_proxied any;
            gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
            gzip_buffers 16 8k;
            # Disable gzip for certain browsers.
            gzip_disable ~@~\MSIE [1-6].(?!.*SV1)~@~];
            expires modified +90d;
        }

        location / {
            proxy_pass http://zerobin_cherrypy;
        }
    }

Nginx sert maintenant le favicon ainsi que les fichiers statiques,
on a ajouté une date d'expiration dans les en-têtes HTTP
et on s'assure que la compression gzip est utilisée pour les navigateurs
qui la supporte.
