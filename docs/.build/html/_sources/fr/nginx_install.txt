========================
Installation avec Nginx
========================

Nginx est un choix très populaire pour servir un projet Python:

- Il est rapide.
- Il est léger.
- Les fichiers de configuration sont très simple.

Si vous avez votre propre serveur, c'est le meilleur choix. Dans le cas contraire,
essayez l'installation la plus simple, ou avec Apache.

Nginx ne lance aucun processus Python, il sert uniquement les requêtes
depuis l'extérieur vers le server Python.

Il y a donc deux étapes:

- Faire tourner le processus Python.
- Faire tourner Nginx.

Ainsi, vous bénéficierez:

- de la possibilité d'avoir plusieurs projets écoutant sur le prot 80;
- de plusieurs modules Nginx à votre disposition (comme la limitation
  du nombre de requêtes);
- de la solidité de Nginx en front end: il est sécurité, et il y a peu de chance
  qu'il crash sous une forte charge;
- les processus de votre site ne tournent pas avec les droits admin, même si
  --user ne fonctionne pas sur votre OS;
- de la capacité de gérer un processus Python sans toucher Nginx ou les autres
  processus. C'est très pratique pour les mises à jour.

Processus Python
==================

Lancez 0bin comme d'habitude, mais cette fois pour écouter sur un host et un port
local. Ex ::

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

Vous devez créer une fichier de configuration Nginx pour 0bin. Sous GNU/Linux,
on les mets en général dans /etc/nginx/conf.d/. Nommez le zerobin.conf.

Le fichier minimal pour faire tourner le site est:

Mais on peut apporter plusieurs améliorations de performance:







