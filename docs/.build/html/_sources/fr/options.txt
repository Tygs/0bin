=======
Options
=======

Le comportement de 0bin peut être ajusté à l'aide d'options passées depuis un
fichier de configuration ou directement à la ligne de commande. Certains
paramètres sont uniquement disponibles dans le fichier de configuration.

Si une option n'est pas passée, 0bin utilise la valeur par
défaut présente dans le fichier zerobin/default_settings.py.

Ligne de commande
==================

--host et --port
-------------------

L'hôte et le port sur lesquels écouter les requêtes entrantes. En général
127.0.0.1 et 8000 pour écouter localement, ou 0.0.0.0 et 80 pour
écouter les requêtes extérieures.

Défaut : 127.0.0.1 et 8000

Équivalent du fichier de configuration : HOST et PORT


--debug
----------

Afffiche un listing d'informations utiles pour déboguer quand quelque chose
se passe mal à la place d'une page d'erreur 500.

En mode debug, le serveur recharge aussi automatiquement tout fichier Python
modifié.

Défaut : False

Équivalent du fichier de configuration : DEBUG

.. _user-and-group-fr:

--user et --group
-------------------

L'utilisateur et le groupe que le serveur essayera d'adopter après le démarrage.

Utile quand on lance la commande avec les droits admin afin de pouvoir
écouter sur le port 80, mais qu'on souhaite, pour des raisons de sécurité, que
le processus n'aie pas accès aux fichiers protégés du système.

--group prend de --user s'il n'est pas précisé.

Défaut : Aucun

Équivalent du fichier de configuration : USER et GROUP

--settings-file
-----------------

Chemin vers le fichier de configuration, si vous souhaitez en utiliser un.

Défaut : Aucun

Équivalent du fichier de configuration : Aucun


--compressed-static
--------------------

Sert les versions minifiées des fichiers statiques (css et js). À utiliser en
production pour un site plus rapide.

Défaut : False

Équivalent du fichier de configuration : COMPRESSED_STATIC_FILES

--version et --help
--------------------

Affiche l'aide ou la version de 0bin.

Défaut : Aucun

Équivalent du fichier de configuration : Aucun

Exemples
----------

Production : ::

  sudo zerobin --host 0.0.0.0 --port 80 --user foo --compressed-static

Développement : ::

  zerobin --debug --serve-static

Fichier de configuration
========================

Le fichier configuration doit être un fichier Python ordinaire, généralement
appelé settings.py. On l'utilise ainsi : ::

  zerobin --settings-file '/chemin/vers/settings.py'

Toutes les autres options passées via la ligne de commande auront priorité sur les options
du fichier de configuration. Le fichier zerobin/default_settings.py peut servir
d'exemple pour créer son propre fichier de configuration, il est largement commenté.

DEBUG
-----

Afffiche un listing d'informations utiles pour déboguer quand quelque chose
se passe mal à la place d'une page d'erreur 500.

En mode debug, le serveur recharge aussi automatiquement tout fichier Python
modifié.

Défaut : False

Équivalent en ligne de commande : --debug

.. _static-root-fr:

STATIC_FILES_ROOT
------------------

Chemin absolu du dossier dans lequel 0bin va chercher les fichiers statiques
(css, js et images).

Défaut : dossier "static" dans le dossier "zerobin"

Équivalent en ligne de commande : Aucun

COMPRESSED_STATIC_FILES
-------------------------

Sert les versions minifiées des fichiers statiques (css et js). À utiliser en
production pour un site plus rapide.

Défaut : False

Équivalent en ligne de commande : --compressed-static

PASTE_FILES_ROOT
-----------------

Chemin absolu du dossier dans lequel 0bin va sauvegarder les pastes.

Défaut : dossier "static/content" dans le dossier "zerobin"

Équivalent en ligne de commande : Aucun

.. _template-dirs-fr:

TEMPLATE_DIRS
--------------

Liste des chemins absolus des dossiers qui contiennent les templates que 0bin
utilise pour générer les pages du site. Les premiers éléments de la liste
ont priorité sur les suivants.

Si vous voulez utiliser vos propres templates, ajoutez le dossier qui les
contient au début de la liste : ::

  from zerobin.defauls_settings import TEMPLATE_DIRS

  TEMPLATE_DIRS = (
      '/chemin/version/votre/dossier/de/templates',
  ) + TEMPLATE_DIRS

Défaut : dossier "view" dans le dossier "zerobin"

Équivalent en ligne de commande : Aucun


HOST et PORT
-------------------

L'hôte et le port sur lesquels écouter les requêtes entrantes. En général
127.0.0.1 et 8000 pour écouter localement, ou 0.0.0.0 et 80 pour
écouter les requêtes extérieures.

Défaut : 127.0.0.1 et 8000

Équivalent du fichier de configuration : --host et --port

USER et GROUP
-------------------

L'utilisateur et le groupe que le serveur essayera d'adopter après le démarrage.

Utile quand on lance la commande avec les droits admin afin de pouvoir
écouter sur le port 80, mais qu'on souhaite, pour des raisons de sécurité, que
le processus n'aie pas accès au fichiers système.

GROUP prend de USER s'il n'est pas précisé.

Défaut : Aucun

Équivalent en ligne de commande : --user et --group

MENU
------

Une liste de paires 'Nom' + 'Liens' à utiliser pour construire le menu qui
est en haut de chaque page.

Le lien peut être un lien relatif, absolu, ou une adresse email.

Toute addresse email sera automatiquement protégée contre le spam.

Défaut : ::

  MENU = (
      ('Home', '/'),
      ('Download 0bin', 'https://github.com/sametmax/0bin'),
      ('Contact', 'mailto:your@email.com') # email
  )

Équivalent en ligne de commande : Aucun

MAX_SIZE
---------

Valeur approximative de limite de taille d'un paste.

Défaut : 500 000 octets (500 ko)

Équivalent en ligne de commande : Aucun
