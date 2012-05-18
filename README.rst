0bin
====

0bin is a client side encrypted pastebin that can run without a database.

* Try it: `0bin.net <http://0bin.net>`_
* Get the `source on github <https://github.com/sametmax/0bin>`_
* `Report a bug <https://github.com/sametmax/0bin/issues>`_

0bin allows anybody to host a pastebin while welcoming any type of content to
be pasted in it. The idea is that one can (probably...) not be legally entitled
to `moderate the pastebin content`_ as he/she has no way to decrypt it.

It's an Python implementation of the
`zerobin project`_. It's easy to
install even if you know nothing about Python.

For now tested with IE9, and the last opera, safari, chrome and FF.

How it works
=============

When creating the paste:

- the browser generate a random key;
- the pasted content is encrypted with this key using AES256;
- the encrypted pasted content is sent to the server;
- the browser receives the paste URL and add the key in the URL hash (#).

When reading the paste:

- the browser makes the GET request to the paste URL;
- because the key is in the hash, the key is not part of the request;
- browser gets the encrypted content et decrypt it using the key;
- the pasted decrypted content is displayed and code is colored.

Key points:

- because the key is in the hash, the key is never sent to the server;
- therefor it won't appear in the server logs;
- all operations, including code coloration, must happens on the client;
- the server is no more than a fancy recipient for the encrypted data.

Other features
======================

- automatic code coloration (no need to specify);
- pastebin expiration: 1 day, 1 month or never;
- burn after reading: the paste is destroyed after the first reading;
- clone paste: you can't edit a paste, but you can duplicate any of them;
- code upload: if a file is too big, you can upload it instead of using copy/paste;
- copy paste to clipboard in a click;
- get paste short URL in a click;
- own previous pastes history;
- visual hash of a paste to easily tell it appart from others in a list.

Technologies used
==================

- Python_
- `The Bottle Python Web microframework`_
- SJCL_ (js crypto tools)
- jQuery_
- Bootstrap_, the Twitter HTML5/CSS3 framework
- VizHash.js_ to create visual hashes from pastes
- Cherrypy_ (server only)


Known issues
============

- 0bin uses several HTML5/CSS3 features that are not widely supported. In that case we handle the degradation as gracefully as we can.
- The "copy to clipboard" feature is buggy under linux. It's flash, so we won't fix it. Better wait for the HTML5 clipboard API to be implemented in major browsers.
- The pasted content size limit check is not accurate. It's just a safety net, so we thinks it's ok.
- Some url shorteners and other services storing URLs break the encryption key. We will sanitize the URL as much as we can, but there is a limit to what we can do.

What does 0bin not implement?
=================================

* Request throttling. It would be inefficient to do it at the app level, and web servers have robust implementations for it.
* Hash collision prevention: the ratio "probability it happens/consequence seriousness" `is not worth it`_
* Comments: it was initially planed. But comes with a lot of issues so we chose to focus on lower handing fruits.


.. _moderate the pastebin content: http://www.zdnet.com/blog/security/pastebin-to-hunt-for-hacker-pastes-anonymous-cries-censorship/11336
.. _zerobin project: https://github.com/sebsauvage/ZeroBin/
.. _Python: https://en.wikipedia.org/wiki/Python_(programming_language)
.. _The Bottle Python Web microframework: http://bottlepy.org/
.. _SJCL: http://crypto.stanford.edu/sjcl/
.. _jQuery: http://jquery.com/
.. _Bootstrap: http://twitter.github.com/bootstrap/
.. _VizHash.js: https://github.com/sametmax/VizHash.js
.. _Cherrypy: http://www.cherrypy.org/ (server only)
.. _is not worth it: http://stackoverflow.com/questions/201705/how-many-random-elements-before-md5-produces-collisions