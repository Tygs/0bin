=========================
Installation avec Apache
=========================

Apache est plus lent, plus lourd, et plus complexe à mettre en oeuvre que Nginx.
Mais il est aussi beaucoup plus connu:

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
  --user ne fonctionne pas sur votre OS.

Apache s'installe avec votre gestionnaire de paquet habituel, nous ne couvrierons
pas cette partie.

Mod_wsgi
==========

Les serveurs Web Python modernes fonctionnent tous de la même manière, en suivant
une norme d'interfaçage: WSGI.

C'est la solution la plus performante, et celle recommandée. Mais elle demande
l'installation du modle Apache mod_wsgi. Si vous ne savez pas comment faire,
ou si vous ne pouvez pas le faire (par exemple sur un hébergement mutualisé
qui ne le propose pas), il vous faudra choisir l'installation CGI.


Mod_CGI
==========

Cette installation est considérée comme relativement lente. Mais vous bénéficierez
tout de même de la robustesse d'Apache