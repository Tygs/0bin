============
Nginx setup
============

.. Note::
    You need to have followed the :doc:`easy install <./easy_install>` first.

Nginx is a very popular choice to serve a Python project:

- It's fast.
- It's lightweight.
- Configuration files are simple.

If you have your own server, it's the best choice. If not, try the
 :doc:`easiest setup <./easy_install>`, or the :doc:`Apache <./apache_install>` setup.

Nginx doesn't run any Python process, it only serve requests from outside to
the Python server.

Therefor there are two steps:

- Run the Python process.
- Run Nginx.

You will benefit from having:

- the possibility to have several projects listening to the port 80;
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

In PHP, when you edit a file, the changes are immediately visible. In Python,
the whole code is often loaded in memory for performance reasons. This means
you have to restart the Python process to see the changes effect. Having a
separate process let you do this without having to restart the server.

Nginx
======

Nginx can be installed with you usual package manager, so we won't cover
installing it.

Vous must create a Nginx configuration file for 0bin. On GNU/Linux, they usually
go into /etc/nginx/conf.d/. Name it zerobin.conf.

The minimal configuration file to run the site is::

    server {
        listen       80;
        server_name www.yourwebsite.com;

        location / {
            proxy_pass http://127.0.0.1:8000;
        }
    }

`proxy_pass` just passes the external request to the Python process.
The port much match the one used by the 0bin process of course.

You can make some adjustements to get a better user experience::

    server {
        listen       80;
        server_name www.yourwebsite.com;

        location /favicon.ico {
            root  /path/to/zerobin/static/img;
        }

        location /static/ {
            root  /path/to/zerobin;
            gzip  on;
            gzip_http_version 1.0;
            gzip_vary on;
            gzip_comp_level 6;
            gzip_proxied any;
            gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
            gzip_buffers 16 8k;
            # Disable gzip for certain browsers.
            gzip_disable ~@~\MSIE [1-6].(?!.*SV1)~@~];
            expires modified +90d;
        }

        location / {
            proxy_pass http://zerobin_cherrypy;
        }
    }

This make Nginx serve the favicon and static files, set the expire HTTP headers
and make sure gzip compression is used with browsers that support it.








