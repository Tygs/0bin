============================
Installation la plus simple
============================

Ces solutions sont simples et supportent le traffic d'un site web personnel.
Pour des solutions plus solides et sécurisées, essayez les installtion Apache
et Nginx.

Installation en 10 secondes (si vous connaissez Python)
========================================================

pip install zerobin
zerobin --host 0.0.0.0 --port 80 --compressed-static # en tant qu'admin


Installation en 30 secondes (pour tous)
=======================================

- Assurez-vous d'avoir Python 2.6 ou 2.7 (`python --version`)
- Télécharger le dernier zip du code source.
- Décompressez tous les fichiers là où vous souhaitez mettre le site.
- Allez dans les dossiers extraits.
- Lancez `python zerobin.py --host 0.0.0.0 --port 80 --compressed-static`
  avec les droits admin.

Sous ubuntu, une line suffit::

    wget stuff && unzip zerobin.zip && cd zerobin && sudo python zerobin.py --host 0.0.0.0 --port 80 --compressed-static

Jetez un oeil aux options de configuration.

Faire tourner 0bin en arrière plan
==================================

0bin ne vient pas avec un moyen intégré pour le faire. Il y a plusieurs
solutions:

Pour un petit site:

Lancer simplement 0bin en processus shell d'arrière plan. Exemple sous GNU/Linux::

  nohup python zerobin.py --host 0.0.0.0 --port 80 --compressed-static &

Ou dans un screen.

Pour les gros sites Web:

- configurer 0bin et Apache;
- configure 0bin avec supervisord (recommandé).

.. Note::

    Vous pouvez même utiliser zerobin sur votre réseau local depuis votre portable.

    Assurez vous que votre parefeu ne bloque pas le port, et lancez::

        python zerobin.py --host 0.0.0.0 --port 8000

    0bin sera maintenant accessible sur http://your.local.ip.address:8000.

    Ça peut être très un moyen très cool pour partager du code dans une entreprise
    ou a un code sprint.
