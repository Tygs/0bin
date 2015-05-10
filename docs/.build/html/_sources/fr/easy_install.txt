============================
Installation la plus simple
============================

Ces solutions sont simples et supportent le traffic d'un site web personnel.
Pour des solutions plus solides et sécurisées, essayez les installation
:doc:`Apache <./apache_install>` et :doc:`Nginx <./nginx_install>`.

Installation en 10 secondes (si vous connaissez Python)
========================================================

Entrez::

    pip install zerobin
    zerobin --host 0.0.0.0 --port 80 --compressed-static # en tant qu'admin


Installation en 30 secondes (pour tous)
=======================================

- Assurez-vous d'avoir Python 2.7 ou 3.4+ (`python --version`)
- Télécharger le dernier `zip du code source <https://github.com/sametmax/0bin/zipball/master>`_.
- Décompressez tous les fichiers là où vous souhaitez mettre le site.
- Allez dans les dossiers extraits.
- Lancez avec les droits admin::

    python zerobin.py --host 0.0.0.0 --port 80 --compressed-static

Sous ubuntu, une line suffit::

    wget stuff && unzip zerobin.zip && cd zerobin && sudo python zerobin.py --host 0.0.0.0 --port 80 --compressed-static

Jetez un oeil aux :doc:`options de configuration <./options>`.

Faire tourner 0bin en arrière plan
==================================

0bin ne vient pas avec un moyen intégré pour le faire. Il y a plusieurs
solutions.

*Pour un petit site:*

Lancer simplement 0bin en processus shell d'arrière plan. Example sous GNU/Linux::

  nohup python zerobin.py --host 0.0.0.0 --port 80 --compressed-static &

Ou dans un screen.

*Pour les gros sites Web:*

- configurer 0bin et :doc:`Apache <./apache_install>`;
- configure 0bin avec :doc:`supervisor <./using_supervisor>` (recommandé).

.. Note::

    Vous pouvez même utiliser zerobin sur votre réseau local depuis votre portable.

    Assurez vous que votre parefeu ne bloque pas le port, et lancez::

        python zerobin.py --host 0.0.0.0 --port 8000

    0bin sera maintenant accessible sur http://votre.addresse.ip.locale:8000.

    Ça peut être très un moyen très cool pour partager du code dans une entreprise
    ou a un code sprint.
