=========================
Installation avec Apache
=========================

.. Note::
    Vous devez avoir suivi :doc:`l'installation facile <./easy_install>` avant.

Apache est plus lourd que :doc:`Nginx <./nginx_install>` mais il
est aussi beaucoup plus connu:

- plus de gens pourront vous aider les fora;
- votre hébergeur propose surement Apache;
- la syntaxe des fichiers de configuration est familière pour beaucoup.

Une installation apache est aussi beaucoup plus solide et sécurisé qu'une
installation facile. Vous bénéficierez:

- de la possibilité d'avoir plusieurs projets écoutant sur le prot 80;
- de plusieurs modules Apache à votre disposition (comme la limitation
  du nombre de requêtes);
- de la solidité d'Apache en front end: il est sécurité, et il y a peu de chance
  qu'il crash sous une forte charge;
- les processus de votre site ne tournent pas avec les droits admin, même si
  :ref:`--user <user-and-group-fr>` ne fonctionne pas sur votre OS.

Apache s'installe avec votre gestionnaire de paquet habituel, nous ne couvrierons
pas cette partie.

Mod_wsgi
==========

Les serveurs Web Python modernes fonctionnent tous de la même manière, en suivant
une norme d'interfaçage: WSGI.

C'est la solution la plus performante, et celle recommandée. Mais elle demande
l'installation du model Apache mod_wsgi. Si vous ne savez pas comment faire,
ou si vous ne pouvez pas le faire (par example sur un hébergement mutualisé
qui ne le propose pas), il vous faudra choisir l'installation CGI.

Premièrement, assurez-vous d'avoir mod_wsgi installé et chargé (en tant qu'admin)::

    a2enmod wsgi

Ceci va activer mod_wsgi. Si cela ne marche pas, il faudra l'installer d'abord (
sur ubuntu, le paquet est libapache2-mod-wsgi)

Ensuite, il faut créer un fichier de configuration Apache, généralement dans
/etc/apache/sites-available/. Nommez le zerobin::

    <VirtualHost *:80>
        ServerName www.votersiteweb.com

        WSGIDaemonProcess zerobin user=www-data group=www-data processes=1 threads=5
        WSGIScriptAlias / /chemin/vers/zerobin/app.wsgi

        <Directory /chemin/vers/zerobin/>
            WSGIProcessGroup zerobin
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>
    </VirtualHost>

Activez le site web (en tant qu'admin)::

    a2ensite zerobin

Et rechargez la configuration d'Apache (en tant qu'admin)::

    service apache2 reload

Vous aurez noté que l'on fait référence à un fichier nommé app.wsgi. C'est un
fichier Python qui créé l'application qu'Apache va utiliser pour lancer le
processus Python::

    import os, sys

    # s'assurer que le module zerobin est dans le PYTHON PATH et importable
    ZEROBIN_PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, ZEROBIN_PARENT_DIR)

    # créer le wsgi callable
    from zerobin.routes import get_app
    settings, application = get_app(compressed_static=True)

Vous pouvez bien sûr créer le votre, puisque la fonction `get_app` et le seul
moyen de passer des paramètres à 0bin avec cette installation. Cela peut se
faire en créant un fichier de configuration et en le passant à la fonction::

    import os, sys

    ZEROBIN_PARENT_DIR = '/chemin/du/dossier/parent/de/zerobin'
    sys.path.insert(0, ZEROBIN_PARENT_DIR)

    from zerobin.routes import get_app
    settings, application = get_app(settings_file='/path/to/settings.py')

CGI
===

Vous pouvez aussi utiliser CGI, mais nous n'avons pas encore eu le temps de
couvrir cette partie. Contactez nous si vous avez besoin de l'utiliser.

