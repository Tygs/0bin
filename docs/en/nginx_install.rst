============
Nginx setup
============

Nginx is a very popular choice to serve a Python project:

- It's fast.
- It's lightweight.
- Configuration files are simple.

If you have your own server, it's the best choice. If not, try the easiest
setup, or the Apache setup.

Nginx doesn't run any Python process, it only serve requests from outside to
the Python server.

Therefor there are two steps:

- Run the Python process.
- Run Nginx.

You will benefit from having:

- the possiblity to have several projects listening to the port 80;
- several Apache module at your disposal (like requests throttling);
- Apache robustness in front end: it's secure, and there is much less chance
  it will crash under heavy load;
- your web site processes won't run with admin rights, even if --user doesn't
  work on your OS;
- the ability to manage a Python process without touching Nginx or the other
  processes. It's very handy for updates.

The Python process
==================

Run 0bin as usual, but this time make it listen to a local port and host. E.G::

    zerobin --host 127.0.0.1 --port 8000

In PHP, when you edit a file, the changes are immediatly visible. In Python,
the whole code is often loaded in memory for performance reasons. This means
you have to restart the Python process to see the changes effect. Having a
separate process let you do this without having to restart the server.

Nginx
======

Nginx can be installed with you usual package manager, so we won't cover
installing it.

Vous must create a Nginx configuration file for 0bin. On GNU/Linux, they usually
go into /etc/nginx/conf.d/. Name it zerobin.conf.

The minimal file to run the site is:

But you can make some adjustement to get better perfomances:








