=========================
Personnaliser l'apparence
=========================

0bin possède un support de theming complet, mais pour le moment mal intégré.

Si vous souhaitez créer votre propre theme, il vous faut créer des templates
similaires à ceux par défault présents dans zerobin/view, et
ajouter le chemin du dossier contenant ces templates au
:ref:`fichier de configuration <template-dirs-fr>`..

Vous aurez également besoin de copier les fichiers statiques présent
dans zerobin/static dans un nouveau dossier, puis les modifier. Et signifier
que vous utilisez ce dossier dans le :ref:`fichier de configuration <static-root-fr>`.

Vous pouvez bien entendu également éditez tous les fichier directement par
souci de simplicité.

Attention cependant, le code javascript est très dépendant des ID et classes
du HTML, qui ne sont pour le moment pas très bien organisés.

Si vous avez de sérieux besoin de theming, contactez-nous, afin que nous
améliorons le support.
