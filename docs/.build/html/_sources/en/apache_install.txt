=============
Apache setup
=============

Apache is slower, heavier and more complicated to setup than Nginx. But it's also
much more famous:

- more people will be able to help you on forums;
- your hosting will most probably support Apache;
- the configuration file syntax is familiar to a lot of people.

An Apache setup is still much more robust and secure than an easy installation.

Une installation apache est aussi beaucoup plus solide et sécurisé qu'une
installation facile. You'll benefit from having:

- the possiblity to have several projects listening to the port 80;
- several Apache module at your disposal (like requests throttling);
- Apache robustness in front end: it's secure, and there is much less chance
  it will crash under heavy load;
- your web site processes won't run with admin rights, even if --user doesn't
  work on your OS.


Mod_wsgi
==========

The modern Web Python servers all work the same way, following an norm for
interfacing: WSGI.

This is the most performante solution, and the best to use. But it will require
the setup of the Apache module mod_wsgi. If you don't know how to do this, or
if you can't do it (E.G: your hosting won't let you), you need to go for
the CGI setup.

==========

This setup is considered as slow, but you will still benefit from Apache
robustness.