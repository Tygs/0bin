0bin
====

Have a try here: <a href="http://0bin.net">0bin.net</a>

0bin is client side encrypted pastebin that can run without a database.

It allows anybody to host a pastebin while welcoming any type of content to be pasted in it. The idea is that one can (probably...) not be legally entitled to <a href="http://www.zdnet.com/blog/security/pastebin-to-hunt-for-hacker-pastes-anonymous-cries-censorship/11336">moderate the pastebin content</a> as he/she has no way to decrypt it.

It's an Python implementation of the <a href="https://github.com/sebsauvage/ZeroBin/">zerobin project</a>.

How it works
=============

When creating the paste:

- the browser generate a random key;
- the pasted content is encrypted with this key using AES256;
- the encrypted pasted content is sent to the server;
- the browser receives the paste URL and add the key in the URL hash.

When reading the paste:

- the browser makes the GET request to the paste URL;
- because the key is in the hash, the key is not part of the request;
- browser gets the enrypted content et decrypt it using the key;
- the pasted content is decrypted and code is colored.

Key points:

- because the key is in the hash, the key is never sent to the server;
- therefor it won't appear in the server logs;
- all operations, including code coloration, must happens on the client;
- the server is no more than a fancy recipient.


Technologies used
==================

- Python
- The Bottle microframework
- SJCL
- jQuery
- Bootstrap
- Cherrypy (server only)

Known issues
============

- 0bin use several HTML5/CSS3 features that are not widely supported. In that case we handle the degradation as gracefully as we can.
- The "copy to clipboard" feature is buggy under linux. It's flash, so we won't fix it. Better wait for the HTML5 clipboard API to be implemented in major browsers.
- The pasted content size limit check is not accurate. It's just a safety net, so we thinks it's ok.
- Some url shorteners and other services storing URLs break the encryption key. We will sanitize the URL as much as we can, but there is a limit to what we can do.

What does 0bin not implement?
=================================

* Request throttling. It would be inefficient to do it at the app level, and web servers have robust implementations.
* Hash collision: the ratio "probability it happens/consequence seriousness" <a href="http://stackoverflow.com/questions/201705/how-many-random-elements-before-md5-produces-collisions">is not worth it</a>
* Comments: for now. It's on the todo list.