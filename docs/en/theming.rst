=======
Theming
=======

0bin comes a complete theming support, but for now it's not well ingrated.

If you wish to create your own theme, you'll need to create template similar
to the ones in zerobin/view, and add the path to the director containing them
to the settings file.

You'll also need to copy static files from zerobin/static to a new direcotry
where you can edit them. And you need to add this directory in the
settings file too.

Of course, if you look for something simple, you can just edit all files in place/

But be careful, the javascript code is tightly coupled with HTML ID and classes,
and they are not very well organized for now.

If you have serious theming needs, please contact us so we improve the support.


