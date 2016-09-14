=======================================
Outil en ligne de commande zerobinpaste
=======================================

zerobinpaste est un simple outil CLI (similaire à pastebinit ou wgetpaste) à utiliser
avec des fichiers ou des redirections shell dans le terminal ou des scripts simples.

Exemple de cas d'utilisation : ::

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

Les liens produits peuvent être ensuite copier-coller sur un channel IRC
ou autre.

L'outil produit le chiffrement lui-même sur la machine et la clé (après le hash)
n'est jamais envoyée au serveur ou nulle part ailleurs excepté la sortie standard
de l'outil (ex : le terminal).

L'outil doit être buildé avec `node.js`_ séparément (voir plus bas).


Usage
=====

Au minimum, il faut préciser le site pastebin (l'url principale d'où on posterait
dans le navigateur) doit être spécifié à l'outil via l'option -u (--url) (on peut
le simplifier avec un alias shell - ex : ``alias zp='zerobinpaste -u http://some.0bin.site``)
ou dans le fichier de configuration "~/.zerobinpasterc" (format json).

| Les arguments positionels sont interprétés comme des fichiers à uploader et chiffrer.
| Si aucun argument n'est passé, le script tentera de lire stdin.

Le fichier de configuration le plus simple pourrait ressembler à ça : ::

    {"url": "http://some.0bin.site"}

Toute option (dans sa forme longue, ex : "url pour --url) utilisable en ligne de commande
peut être spécifiée ici.

Lancez l'outil avec -h ou --help pour voir la liste des paramètres supportés.


Build / Installation
====================

En bref : ::

    0bin% cd tools
    0bin/tools% make
    ...
    0bin/tools% cp zerobinpaste ~/bin   # install to PATH

La commande "npm" (packagée and installée avec node.js) est requise pour télécharger
les dépendances indispensables à la production de l'éxécutable.

Utilisez "make" dans le dossier "tools" pour produire une version non-minifiée de "zerobinpaste".

La commande ``make ugly`` peut être utilisée à la place de ``make`` pour créer une version minifiée
(requiert l'installation de uglifyjs_, script produit environ 25% plus petit en taille).

Le script "zerobinpaste" ainsi produit a seulement besoin de node.js (et la commande "node") pour
s'exécuter et peut être placé n'importe où dans le PATH système (ex : "~/bin", "/usr/local/bin")
afin d'être exécuté en tapant simplement "zerobinpaste".


Pourquoi node.js et pas Python
==============================

Malheureusement, il est assez difficile et peu fiable de répliquer un protocole
chiffrement non trivial et non documenté tel que celui de certaines méthodes
de SJCL_, et la moindre erreur garantie de produire un paste illisible.

L'implémentation actuelle utilise le même code JavaScript (via le moteur V8 de node.js)
que le navigateur, du coup il est simple et robuste.

Il est prévu de supporter plus tard un schéma de chiffrement plus configurable, moins
complexe et plus courant, permettant à des clients non-JavaScript de fonctioner également.

Voir le `pull request concerné`_ pour plus de détails.

.. _node.js: http://nodejs.org/
.. _uglifyjs: https://github.com/mishoo/UglifyJS
.. _SJCL: http://crypto.stanford.edu/sjcl/
.. _pull request concerné: https://github.com/sametmax/0bin/pull/39
