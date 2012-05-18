=======
Theming
=======

0bin comes with a complete theming support, but for now it's not well integrated.

If you wish to create your own theme, you'll need to create templates similar
to the ones in zerobin/view, and add the path to the directory containing them
to the :ref:`configuration file <template-dirs-en>`.

You'll also need to copy static files from zerobin/static to a new directory
where you can edit them. And you need to add this directory in the
:ref:`configuration file <static-root-en>` too.

Of course, if you look for something simple, you can just edit all files in place/

But be careful, the javascript code is tightly coupled with HTML ID and classes,
and they are not very well organized for now.

If you have serious theming needs, please contact us so we improve the support.


