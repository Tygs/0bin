============
Introduction
============

0bin permet à tout à chacun d'héberge un pastebin tout en acceptant que n'importe
quel type de contenu y soit posté. L'idée est qu'une personne ne peut (probablement...)
pas être tenue de `modérer le contenu du pastebin`_ si elle n'a aucun moyen
de le déchiffrer.

C'est une implémentation en Python du `projet zerobin`_, facile à installer même
si on ne connait pas ce langage.

Comment ça marche
====================

A la création du paste:

- le navigateur génère une clé aléatoire;
- le contenu est chiffré avec une clé en utilisat AES256;
- le contenu chiffré est envoyé au serveur;
- le navigateur reçoit l'URL du paste et ajoute la clé dans le hash (#) de l'URL

A la lecture du paste:

- le navigateur fait une requête GET avec l'URL du paste;
- puisque la clé est das le hash, la clé ne fait pas partie de la requête;
- le navigateur récupère le contenu chiffré et le déchiffre en utilisant la clé;
- le contenu est affiché en clair et le code coloré.

Points clés:

- la clé n'est jamais envoyé au serveur car elle est stocké dans le hash;
- et donc la clé n'apparaitra pas dans les logs du serveur;
- toutes les opérations, y compris la coloration syntaxique, se font côté client;
- le serveur n'est rien d'autre d'un conteneur pour les données chiffrée.

Autres fonctionalités
======================

- coloration syntaxique automatique (pas besoin de la spécifier);
- expiration du pastebin: 1 jour, 1 mois, jamais;
- autodesctruction: le paste est détruit à la première lecture;
- clone d'un paste: pas d'édition possible, mais on peut dupliquer un paste;
- upload du code: si le fichier est gros, on peut l'uploader d'un coup
  plutôt qu'utiliser le copier/coller;
- copier dans le presse papier tout le code en un click;
- raccourcir l'url du paste en un click;
- historique des ses propres pastes précédents;
- hash visuel du paste pour l'identifier facilement dans une liste.


Technologies utilisées
=======================

- Python_
- `The Bottle Python Web microframework`_
- SJCL_ (js crypto tools)
- jQuery_
- Bootstrap_, le framework HTML5/CSS3 de Twitter
- VizHash.js_ pour créer les hash visuels des pastes
- Cherrypy_ (serveur uniquement)


Problèmes connus
=================

- 0bin utilise plusieurs fonctionalités HTML5/CSS3 qui ne sont pas
  encore largement supporté. Dans ce cas nous gérons la dégradation le plus
  gracieusement possible.
- La fonction "copier dans le press/papier" est buggée sous Linux. C'est du
  flash donc nous ne le réparerons pas. Il vaut mieux attendre le support
  du presse papier via l'API HTML5.
- La vérification de la limite de ta taille du paste n'est pas précise. c'est
  juste un filet de sécurité, donc nous pensons que ça suffira.
- Quelques raccourcisseurs d'URL et d'autres services cassent la clé de
  chiffrement. Nous essayerons de nettoyer autant que possible mais il y
  a une limite à ce que nous pouvons faire.

Qu'est-ce que 0bin ne fait pas ?
=================================

- Limitation du nombre de requêtes: ce serait peu productif de le faire au
  niveau de l'application alors que les serveurs Web le font tous de manière très
  efficace.
- La prévention de collision de hash: le ratio "occurence/conséquence"
  n'est pas suffisant_.
- Commentaires: c'était prévu. Mais il y a beaucoup de contraintes associées,
  nous avons donc choisi de nous concentrer sur les fonctions avec un meilleur
  rapport qualité/prix.


.. _modérer le contenu du pastebin: http://linuxfr.org/news/zerobin-un-pastebin-securise
.. _projet zerobin: https://github.com/sebsauvage/ZeroBin/
.. _Python: https://en.wikipedia.org/wiki/Python_(programming_language)
.. _The Bottle Python Web microframework: http://bottlepy.org/
.. _SJCL: http://crypto.stanford.edu/sjcl/
.. _jQuery: http://jquery.com/
.. _Bootstrap: http://twitter.github.com/bootstrap/
.. _VizHash.js: https://github.com/sametmax/VizHash.js
.. _Cherrypy: http://www.cherrypy.org/ (server only)
.. _suffisant: http://stackoverflow.com/questions/201705/how-many-random-elements-before-md5-produces-collisions