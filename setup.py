#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os

from setuptools import setup, find_packages

# DISTUTILS_DEBUG = True # uncomment only to debug errors when running setup.py


# BEFORE FAILLING MISERABLY:
#
# If you get any encoding error, it's most probably a known distutils bugs
# use strip_non_ascii(youstring) to replace non ascii caracters
# http://bugs.python.org/issue13114
# Either upgrade your Python, or use this function
# I don't know any other good way to do this, sorry
# This function expect unicode, use decode() before applying
strip_non_ascii = lambda s: normalize('NFKD', s).encode('ascii','ignore')




######################### STEP 1: choose a source root dir #####################

# A string: the relative path to the directory where lie the code you wish to distribute
# It's recommanded for that directory to be localted at the same level
# that this file (setup.py)
# Ideally, it should be the directory that you wish to be available in
# the PYTHONPATH after install
# E.G: 'my_super_project'
src_directory = 'zerobin'



####### STEP 2: list all non python files you wish to distribute as well #######

# The manifest contains instructions to tell which non python file setuptools
# should include in the distribution. It one command on each line, among:

# include pat1 pat2 ...: include all files matching any of the listed patterns
#                        in the root directory
# exclude pat1 pat2 ...: exclude all files matching any of the listed patterns
#                        in the root directory
# recursive-include dir pat1 pat2 ...: include all files under dir matching
#                                      any of the listed patterns
# recursive-exclude dir pat1 pat2 ...: exclude all files under dir matching
#                                      any of the listed patterns
# global-include pat1 pat2 ...: include all files anywhere in the source
#                               tree matching — & any of the listed patterns
# global-exclude pat1 pat2 ...: exclude all files anywhere in the source
#                               tree matching — & any of the listed patterns
# prune dir: exclude all files under dir
# graft dir: include all files under dir

# Add a line here for each command:

open('MANIFEST.in', 'w').write('\n'.join((

    "include *.rst *.tx",
    "recursive-include %s *.png *.jpg *.gif *.ico" % src_directory,
    "recursive-include %s *.css *.js *.swf" % src_directory,
    "recursive-include %s *.tpl" % src_directory
)))



######################### STEP 3: set your project metadata ####################

setup(

    ########################
    # Mandatory parameters #
    ########################


    # A string with the of the project in PyPi
    name="zerobin",

    # A string with the version of the project, using
    # the notation major.minor[.patch[.sub]].
    # More defails: http://peak.telecommunity.com/DevCenter/setuptools#id6
    # E.G: "0.1", or "1.11.04", or "2"
    version="0.1",

    # An iterable of strings with the names of all packages to be included
    # for distribution. setup() will not recurse over this package, so it
    # should explicitly mention ALL package files, directory and sub packages.
    # E.G: ['stuff', 'foo', foo.bar']
    #
    # You usually just want your main package and all sub package, which
    # is what find_packages() returns:
    #
    # find_packages (where='.', exclude=())
    #
    # Return a list all Python packages found within directory 'where'
    #
    # 'where' should be supplied as a "cross-platform" (i.e. URL-style) path; it
    # will be converted to the appropriate local path syntax.  'exclude' is a
    # sequence of package names to exclude; '*' can be used as a wildcard in the
    # names, such that 'foo.*' will exclude all subpackages of 'foo' (but not
    # 'foo' itself).
    # E.G : find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
    # or something more complicated like
    packages=find_packages(exclude=["libs", "libs.*"]),


    ##########################################################################
    # Parameters you definitly should fill even if they are optional         #
    # You need to either fill or comment them, or setup.py install will fail #
    ##########################################################################


    # A string containing your first and last name.
    # There is no way to put several authors so use
    # an organisation name and profile a "contributors" file
    # This information will be public, so be careful.
    author="Sam et Max",

    # A string with a valid email.
    # Warning: this information will be easily discoverable by spambots.
    author_email="lesametlemax@gmail.com",

    # A string describing what this code does in one short sentence.
    # E.G: "This stuff foo a bar with attitude"
    description="An client side encrypted pastebin",

    # A long string giving a quick overview of the whole code
    # It's common to just dump the README here, so it's the default value
    # but you can replace it with whatever you want
    # It will be used by Pypi to build the web page for your package
    #
    # If something fails with a unicode error, easiest fix is
    # strip_non_ascii(open('README.rst').read().decode('yourencoding'))
    long_description=open('README.rst').read(),

    # An iterable of strings being the name of dependancies for this code
    # Each item should be a module name as published on pypi, and should
    # You can require a specific version.
    # be available in pypi
    # E.G: ["gunicorn", "docutils >= 0.3", "BeautifulSoup==1.1", "lxml==0.5a7"]
    install_requires=[
        'cherrypy',
        'bottle',
        'clize',
        'privilege'
    ],


    ###########################################################################
    # Parameters you may want to fill or change                               #
    # It's ok if don't touch them, but they are useful for certain use cases  #
    # so you should at least read them                                        #
    ###########################################################################


    # If set to True, this tells setuptools to automatically include any data files it
    # finds inside your package directories, that are either under CVS or Subversion
    # control, or which are specified by your MANIFEST.in file.
    #
    # If will include any non Python file that is in a directly in a package
    # directory (like README and else) but not the ones in a subdirectory of
    # of a package (so no use for web static files, images, etc)
    #
    # You WANT that set to True because it will copy files from the MANIFEST.in
    include_package_data=True,

    ## An optional string being the URL of the official website for this code
    ## A lot of people just put the URL of the code repository or the doc
    ## E.G: 'http://github.com/username/ProjectName'
    # url=,

    ## A iterable of strings being the relative paths to executable which you
    ## you wish to install in the system path
    ## For exemple, if you want you code to provide the command "myadmin.py"
    ## ['root/relative/path/to/script/myadmin.py']
    ## To avoid repeating, you probably something like
    ## [os.path.join(src_directory, script) for script in
    ##     ['src_directory/relative/path/to/script_1.py',
    ##     'src_directory/relative/path/to/script_2.py'  ]]
    # scripts=,

    ## Iterable of strings being names of modules you wish to include as well
    ## It's more accurate than a package
    ## espcially usefull if you have lonelly modules at the root level
    # E.G: ['mod1', 'pkg.mod2'] if you have mod1.py and pkg/mod2.py
    # py_modules= ,

    ## A mapping package/directory, so you can choose where setuptools will
    ## import packages listed in the `packages` parameter
    ## The key is the name of the package, the value is the directory being the
    ## package
    ## An empty string being the root where all package will be.
    ##
    ## E.G:
    ## If all your packages are in './lib' and you declared `packages = ['foo', 'foo.bar']`,
    ## then you want to tell setuptools that './lib' is the root: {'': 'lib'}
    ##
    ## If you have a package 'stuff', but it's named 'thing' on the filesystem,
    ## and you declared `packages = ['stuff', 'stuff.func']`, you can tell
    ## setuptools that the "thing" dir is the "stuff" package: {'stuff': 'thing'}
    ##
    ## If you get get missing package after settings this, it's because
    ## find_package() use value from this settings to tweak accordingly
    # package_dir= ,

    ## Iterable of string bein URLs
    ## If your project depends on packages that aren't registered in PyPI, you may
    ## still be able to depend on them, as long as they are available for download
    ## as an egg, in the standard distutils sdist format, or as a single .py file.
    ##
    ## The URLs must be either:
    ##
    ## direct download URLs, or
    ## the URLs of web pages that contain direct download links
    ## E.G: ["http://peak.telecommunity.com/snapshots/"],
    dependency_links=[
        'http://www.subspacefield.org/security/privilege/code/privilege/'
    ],

    ## List of strings being the name of EXTERNAL modules you embed in your
    ## code and therefor, that you provide
    ## E.G: ['clize', 'peewee']
    # provides=,

    # Iterable of string being metadata. You can't add yours and pypi is picky
    # about the syntax, so just uncomment the one you want to set.
    # It is adviced to at least provide "Operating System" and "Licence"
    # Incompatibel with 2.2.3- or 2.3-
    classifiers=[
        'Programming Language :: Python',
        # "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        # "Development Status :: 7 - Inactive",
        # "Environment :: Console",
        # "Environment :: Console :: Curses",
        # "Environment :: Console :: Framebuffer",
        # "Environment :: Console :: Newt",
        # "Environment :: Console :: svgalib",
        # "Environment :: Handhelds/PDA's",
        # "Environment :: MacOS X",
        # "Environment :: MacOS X :: Aqua",
        # "Environment :: MacOS X :: Carbon",
        # "Environment :: MacOS X :: Cocoa",
        # "Environment :: No Input/Output (Daemon)",
        # "Environment :: Other Environment",
        # "Environment :: Plugins",
        # "Environment :: Web Environment",
        # "Environment :: Web Environment :: Buffet",
        # "Environment :: Web Environment :: Mozilla",
        # "Environment :: Web Environment :: ToscaWidgets",
        # "Environment :: Win32 (MS Windows)",
        # "Environment :: X11 Applications",
        # "Environment :: X11 Applications :: Gnome",
        # "Environment :: X11 Applications :: GTK",
        # "Environment :: X11 Applications :: KDE",
        # "Environment :: X11 Applications :: Qt",
        # "Framework :: BFG",
        # "Framework :: Buildout",
        # "Framework :: Buildout :: Extension",
        # "Framework :: Buildout :: Recipe",
        # "Framework :: Chandler",
        # "Framework :: CherryPy",
        # "Framework :: CubicWeb",
        # "Framework :: Django",
        # "Framework :: IDLE",
        # "Framework :: Paste",
        # "Framework :: Plone",
        # "Framework :: Plone :: 3.2",
        # "Framework :: Plone :: 3.3",
        # "Framework :: Plone :: 4.0",
        # "Framework :: Plone :: 4.1",
        # "Framework :: Plone :: 4.2",
        # "Framework :: Plone :: 4.3",
        # "Framework :: Pylons",
        # "Framework :: Setuptools Plugin",
        # "Framework :: Trac",
        # "Framework :: Tryton",
        # "Framework :: TurboGears",
        # "Framework :: TurboGears :: Applications",
        # "Framework :: TurboGears :: Widgets",
        # "Framework :: Twisted",
        # "Framework :: ZODB",
        # "Framework :: Zope2",
        # "Framework :: Zope3",
        # "Intended Audience :: Customer Service",
        # "Intended Audience :: Developers",
        # "Intended Audience :: Education",
        # "Intended Audience :: End Users/Desktop",
        # "Intended Audience :: Financial and Insurance Industry",
        # "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Information Technology",
        # "Intended Audience :: Legal Industry",
        # "Intended Audience :: Manufacturing",
        # "Intended Audience :: Other Audience",
        # "Intended Audience :: Religion",
        # "Intended Audience :: Science/Research",
        # "Intended Audience :: System Administrators",
        # "Intended Audience :: Telecommunications Industry",
        # "License :: Aladdin Free Public License (AFPL)",
        # "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        # "License :: DFSG approved",
        # "License :: Eiffel Forum License (EFL)",
        # "License :: Free For Educational Use",
        # "License :: Free For Home Use",
        # "License :: Free for non-commercial use",
        # "License :: Freely Distributable",
        # "License :: Free To Use But Restricted",
        # "License :: Freeware",
        # "License :: Netscape Public License (NPL)",
        # "License :: Nokia Open Source License (NOKOS)",
        # "License :: OSI Approved",
        # "License :: OSI Approved :: Academic Free License (AFL)",
        # "License :: OSI Approved :: Apache Software License",
        # "License :: OSI Approved :: Apple Public Source License",
        # "License :: OSI Approved :: Artistic License",
        # "License :: OSI Approved :: Attribution Assurance License",
        # "License :: OSI Approved :: BSD License",
        # "License :: OSI Approved :: Common Public License",
        # "License :: OSI Approved :: Eiffel Forum License",
        # "License :: OSI Approved :: European Union Public Licence 1.0 (EUPL 1.0)",
        # "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
        # "License :: OSI Approved :: GNU Affero General Public License v3",
        # "License :: OSI Approved :: GNU Free Documentation License (FDL)",
        # "License :: OSI Approved :: GNU General Public License (GPL)",
        # "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        # "License :: OSI Approved :: IBM Public License",
        # "License :: OSI Approved :: Intel Open Source License",
        # "License :: OSI Approved :: ISC License (ISCL)",
        # "License :: OSI Approved :: Jabber Open Source License",
        # "License :: OSI Approved :: MIT License",
        # "License :: OSI Approved :: MITRE Collaborative Virtual Workspace License (CVW)",
        # "License :: OSI Approved :: Motosoto License",
        # "License :: OSI Approved :: Mozilla Public License 1.0 (MPL)",
        # "License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)",
        # "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        # "License :: OSI Approved :: Nethack General Public License",
        # "License :: OSI Approved :: Nokia Open Source License",
        # "License :: OSI Approved :: Open Group Test Suite License",
        # "License :: OSI Approved :: Python License (CNRI Python License)",
        # "License :: OSI Approved :: Python Software Foundation License",
        # "License :: OSI Approved :: Qt Public License (QPL)",
        # "License :: OSI Approved :: Ricoh Source Code Public License",
        # "License :: OSI Approved :: Sleepycat License",
        # "License :: OSI Approved :: Sun Industry Standards Source License (SISSL)",
        # "License :: OSI Approved :: Sun Public License",
        # "License :: OSI Approved :: University of Illinois/NCSA Open Source License",
        # "License :: OSI Approved :: Vovida Software License 1.0",
        # "License :: OSI Approved :: W3C License",
        # "License :: OSI Approved :: X.Net License",
        "License :: OSI Approved :: zlib/libpng License",
        # "License :: OSI Approved :: Zope Public License",
        # "License :: Other/Proprietary License",
        # "License :: Public Domain",
        # "License :: Repoze Public License",
        # "Natural Language :: Afrikaans",
        # "Natural Language :: Arabic",
        # "Natural Language :: Bengali",
        # "Natural Language :: Bosnian",
        # "Natural Language :: Bulgarian",
        # "Natural Language :: Catalan",
        # "Natural Language :: Chinese (Simplified)",
        # "Natural Language :: Chinese (Traditional)",
        # "Natural Language :: Croatian",
        # "Natural Language :: Czech",
        # "Natural Language :: Danish",
        # "Natural Language :: Dutch",
        "Natural Language :: English",
        # "Natural Language :: Esperanto",
        # "Natural Language :: Finnish",
        # "Natural Language :: French",
        # "Natural Language :: Galician",
        # "Natural Language :: German",
        # "Natural Language :: Greek",
        # "Natural Language :: Hebrew",
        # "Natural Language :: Hindi",
        # "Natural Language :: Hungarian",
        # "Natural Language :: Icelandic",
        # "Natural Language :: Indonesian",
        # "Natural Language :: Italian",
        # "Natural Language :: Japanese",
        # "Natural Language :: Javanese",
        # "Natural Language :: Korean",
        # "Natural Language :: Latin",
        # "Natural Language :: Latvian",
        # "Natural Language :: Macedonian",
        # "Natural Language :: Malay",
        # "Natural Language :: Marathi",
        # "Natural Language :: Norwegian",
        # "Natural Language :: Panjabi",
        # "Natural Language :: Persian",
        # "Natural Language :: Polish",
        # "Natural Language :: Portuguese",
        # "Natural Language :: Portuguese (Brazilian)",
        # "Natural Language :: Romanian",
        # "Natural Language :: Russian",
        # "Natural Language :: Serbian",
        # "Natural Language :: Slovak",
        # "Natural Language :: Slovenian",
        # "Natural Language :: Spanish",
        # "Natural Language :: Swedish",
        # "Natural Language :: Tamil",
        # "Natural Language :: Telugu",
        # "Natural Language :: Thai",
        # "Natural Language :: Turkish",
        # "Natural Language :: Ukranian",
        # "Natural Language :: Urdu",
        # "Natural Language :: Vietnamese",
        # "Operating System :: BeOS",
        # "Operating System :: MacOS",
        # "Operating System :: MacOS :: MacOS 9",
        # "Operating System :: MacOS :: MacOS X",
        # "Operating System :: Microsoft",
        # "Operating System :: Microsoft :: MS-DOS",
        # "Operating System :: Microsoft :: Windows",
        # "Operating System :: Microsoft :: Windows :: Windows 3.1 or Earlier",
        # "Operating System :: Microsoft :: Windows :: Windows 95/98/2000",
        # "Operating System :: Microsoft :: Windows :: Windows CE",
        # "Operating System :: Microsoft :: Windows :: Windows NT/2000",
        # "Operating System :: OS/2",
        # "Operating System :: OS Independent",
        # "Operating System :: Other OS",
        # "Operating System :: PalmOS",
        # "Operating System :: PDA Systems",
        # "Operating System :: POSIX",
        # "Operating System :: POSIX :: AIX",
        # "Operating System :: POSIX :: BSD",
        # "Operating System :: POSIX :: BSD :: BSD/OS",
        # "Operating System :: POSIX :: BSD :: FreeBSD",
        # "Operating System :: POSIX :: BSD :: NetBSD",
        # "Operating System :: POSIX :: BSD :: OpenBSD",
        # "Operating System :: POSIX :: GNU Hurd",
        # "Operating System :: POSIX :: HP-UX",
        # "Operating System :: POSIX :: IRIX",
        # "Operating System :: POSIX :: Linux",
        # "Operating System :: POSIX :: Other",
        # "Operating System :: POSIX :: SCO",
        # "Operating System :: POSIX :: SunOS/Solaris",
        # "Operating System :: Unix",
        # "Programming Language :: Ada",
        # "Programming Language :: APL",
        # "Programming Language :: ASP",
        # "Programming Language :: Assembly",
        # "Programming Language :: Awk",
        # "Programming Language :: Basic",
        # "Programming Language :: C",
        # "Programming Language :: C#",
        # "Programming Language :: C++",
        # "Programming Language :: Cold Fusion",
        # "Programming Language :: Cython",
        # "Programming Language :: Delphi/Kylix",
        # "Programming Language :: Dylan",
        # "Programming Language :: Eiffel",
        # "Programming Language :: Emacs-Lisp",
        # "Programming Language :: Erlang",
        # "Programming Language :: Euler",
        # "Programming Language :: Euphoria",
        # "Programming Language :: Forth",
        # "Programming Language :: Fortran",
        # "Programming Language :: Haskell",
        # "Programming Language :: Java",
        # "Programming Language :: JavaScript",
        # "Programming Language :: Lisp",
        # "Programming Language :: Logo",
        # "Programming Language :: ML",
        # "Programming Language :: Modula",
        # "Programming Language :: Objective C",
        # "Programming Language :: Object Pascal",
        # "Programming Language :: OCaml",
        # "Programming Language :: Other",
        # "Programming Language :: Other Scripting Engines",
        # "Programming Language :: Pascal",
        # "Programming Language :: Perl",
        # "Programming Language :: PHP",
        # "Programming Language :: Pike",
        # "Programming Language :: Pliant",
        # "Programming Language :: PL/SQL",
        # "Programming Language :: PROGRESS",
        # "Programming Language :: Prolog",
        # "Programming Language :: Python :: 2",
        # "Programming Language :: Python :: 2.3",
        # "Programming Language :: Python :: 2.4",
        # "Programming Language :: Python :: 2.5",
        # "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        # "Programming Language :: Python :: 2 :: Only",
        # "Programming Language :: Python :: 3",
        # "Programming Language :: Python :: 3.0",
        # "Programming Language :: Python :: 3.1",
        # "Programming Language :: Python :: 3.2",
        # "Programming Language :: Python :: 3.3",
        # "Programming Language :: Python :: Implementation",
        # "Programming Language :: Python :: Implementation :: CPython",
        # "Programming Language :: Python :: Implementation :: IronPython",
        # "Programming Language :: Python :: Implementation :: Jython",
        # "Programming Language :: Python :: Implementation :: PyPy",
        # "Programming Language :: Python :: Implementation :: Stackless",
        # "Programming Language :: REBOL",
        # "Programming Language :: Rexx",
        # "Programming Language :: Ruby",
        # "Programming Language :: Scheme",
        # "Programming Language :: Simula",
        # "Programming Language :: Smalltalk",
        # "Programming Language :: SQL",
        # "Programming Language :: Tcl",
        # "Programming Language :: Unix Shell",
        # "Programming Language :: Visual Basic",
        # "Programming Language :: XBasic",
        # "Programming Language :: YACC",
        # "Programming Language :: Zope",
        # "Topic :: Adaptive Technologies",
        # "Topic :: Artistic Software",
        # "Topic :: Communications",
        # "Topic :: Communications :: BBS",
        # "Topic :: Communications :: Chat",
        # "Topic :: Communications :: Chat :: AOL Instant Messenger",
        # "Topic :: Communications :: Chat :: ICQ",
        # "Topic :: Communications :: Chat :: Internet Relay Chat",
        # "Topic :: Communications :: Chat :: Unix Talk",
        # "Topic :: Communications :: Conferencing",
        # "Topic :: Communications :: Email",
        # "Topic :: Communications :: Email :: Address Book",
        # "Topic :: Communications :: Email :: Email Clients (MUA)",
        # "Topic :: Communications :: Email :: Filters",
        # "Topic :: Communications :: Email :: Mailing List Servers",
        # "Topic :: Communications :: Email :: Mail Transport Agents",
        # "Topic :: Communications :: Email :: Post-Office",
        # "Topic :: Communications :: Email :: Post-Office :: IMAP",
        # "Topic :: Communications :: Email :: Post-Office :: POP3",
        # "Topic :: Communications :: Fax",
        # "Topic :: Communications :: FIDO",
        # "Topic :: Communications :: File Sharing",
        # "Topic :: Communications :: File Sharing :: Gnutella",
        # "Topic :: Communications :: File Sharing :: Napster",
        # "Topic :: Communications :: Ham Radio",
        # "Topic :: Communications :: Internet Phone",
        # "Topic :: Communications :: Telephony",
        # "Topic :: Communications :: Usenet News",
        # "Topic :: Database",
        # "Topic :: Database :: Database Engines/Servers",
        # "Topic :: Database :: Front-Ends",
        # "Topic :: Desktop Environment",
        # "Topic :: Desktop Environment :: File Managers",
        # "Topic :: Desktop Environment :: Gnome",
        # "Topic :: Desktop Environment :: GNUstep",
        # "Topic :: Desktop Environment :: K Desktop Environment (KDE)",
        # "Topic :: Desktop Environment :: K Desktop Environment (KDE) :: Themes",
        # "Topic :: Desktop Environment :: PicoGUI",
        # "Topic :: Desktop Environment :: PicoGUI :: Applications",
        # "Topic :: Desktop Environment :: PicoGUI :: Themes",
        # "Topic :: Desktop Environment :: Screen Savers",
        # "Topic :: Desktop Environment :: Window Managers",
        # "Topic :: Desktop Environment :: Window Managers :: Afterstep",
        # "Topic :: Desktop Environment :: Window Managers :: Afterstep :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: Applets",
        # "Topic :: Desktop Environment :: Window Managers :: Blackbox",
        # "Topic :: Desktop Environment :: Window Managers :: Blackbox :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: CTWM",
        # "Topic :: Desktop Environment :: Window Managers :: CTWM :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: Enlightenment",
        # "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Epplets",
        # "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR15",
        # "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR16",
        # "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR17",
        # "Topic :: Desktop Environment :: Window Managers :: Fluxbox",
        # "Topic :: Desktop Environment :: Window Managers :: Fluxbox :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: FVWM",
        # "Topic :: Desktop Environment :: Window Managers :: FVWM :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: IceWM",
        # "Topic :: Desktop Environment :: Window Managers :: IceWM :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: MetaCity",
        # "Topic :: Desktop Environment :: Window Managers :: MetaCity :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: Oroborus",
        # "Topic :: Desktop Environment :: Window Managers :: Oroborus :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: Sawfish",
        # "Topic :: Desktop Environment :: Window Managers :: Sawfish :: Themes 0.30",
        # "Topic :: Desktop Environment :: Window Managers :: Sawfish :: Themes pre-0.30",
        # "Topic :: Desktop Environment :: Window Managers :: Waimea",
        # "Topic :: Desktop Environment :: Window Managers :: Waimea :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: Window Maker",
        # "Topic :: Desktop Environment :: Window Managers :: Window Maker :: Applets",
        # "Topic :: Desktop Environment :: Window Managers :: Window Maker :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: XFCE",
        # "Topic :: Desktop Environment :: Window Managers :: XFCE :: Themes",
        # "Topic :: Documentation",
        # "Topic :: Education",
        # "Topic :: Education :: Computer Aided Instruction (CAI)",
        # "Topic :: Education :: Testing",
        # "Topic :: Games/Entertainment",
        # "Topic :: Games/Entertainment :: Arcade",
        # "Topic :: Games/Entertainment :: Board Games",
        # "Topic :: Games/Entertainment :: First Person Shooters",
        # "Topic :: Games/Entertainment :: Fortune Cookies",
        # "Topic :: Games/Entertainment :: Multi-User Dungeons (MUD)",
        # "Topic :: Games/Entertainment :: Puzzle Games",
        # "Topic :: Games/Entertainment :: Real Time Strategy",
        # "Topic :: Games/Entertainment :: Role-Playing",
        # "Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games",
        # "Topic :: Games/Entertainment :: Simulation",
        # "Topic :: Games/Entertainment :: Turn Based Strategy",
        # "Topic :: Home Automation",
        # "Topic :: Internet",
        # "Topic :: Internet :: File Transfer Protocol (FTP)",
        # "Topic :: Internet :: Finger",
        # "Topic :: Internet :: Log Analysis",
        # "Topic :: Internet :: Name Service (DNS)",
        # "Topic :: Internet :: Proxy Servers",
        # "Topic :: Internet :: WAP",
        # "Topic :: Internet :: WWW/HTTP",
        # "Topic :: Internet :: WWW/HTTP :: Browsers",
        # "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        # "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
        # "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards",
        # "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",
        # "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Page Counters",
        # "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        # "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        # "Topic :: Internet :: WWW/HTTP :: Session",
        # "Topic :: Internet :: WWW/HTTP :: Site Management",
        # "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
        # "Topic :: Internet :: WWW/HTTP :: WSGI",
        # "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        # "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        # "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
        # "Topic :: Internet :: Z39.50",
        # "Topic :: Multimedia",
        # "Topic :: Multimedia :: Graphics",
        # "Topic :: Multimedia :: Graphics :: 3D Modeling",
        # "Topic :: Multimedia :: Graphics :: 3D Rendering",
        # "Topic :: Multimedia :: Graphics :: Capture",
        # "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera",
        # "Topic :: Multimedia :: Graphics :: Capture :: Scanners",
        # "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
        # "Topic :: Multimedia :: Graphics :: Editors",
        # "Topic :: Multimedia :: Graphics :: Editors :: Raster-Based",
        # "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
        # "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        # "Topic :: Multimedia :: Graphics :: Presentation",
        # "Topic :: Multimedia :: Graphics :: Viewers",
        # "Topic :: Multimedia :: Sound/Audio",
        # "Topic :: Multimedia :: Sound/Audio :: Analysis",
        # "Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
        # "Topic :: Multimedia :: Sound/Audio :: CD Audio",
        # "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Playing",
        # "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Ripping",
        # "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Writing",
        # "Topic :: Multimedia :: Sound/Audio :: Conversion",
        # "Topic :: Multimedia :: Sound/Audio :: Editors",
        # "Topic :: Multimedia :: Sound/Audio :: MIDI",
        # "Topic :: Multimedia :: Sound/Audio :: Mixers",
        # "Topic :: Multimedia :: Sound/Audio :: Players",
        # "Topic :: Multimedia :: Sound/Audio :: Players :: MP3",
        # "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
        # "Topic :: Multimedia :: Sound/Audio :: Speech",
        # "Topic :: Multimedia :: Video",
        # "Topic :: Multimedia :: Video :: Capture",
        # "Topic :: Multimedia :: Video :: Conversion",
        # "Topic :: Multimedia :: Video :: Display",
        # "Topic :: Multimedia :: Video :: Non-Linear Editor",
        # "Topic :: Office/Business",
        # "Topic :: Office/Business :: Financial",
        # "Topic :: Office/Business :: Financial :: Accounting",
        # "Topic :: Office/Business :: Financial :: Investment",
        # "Topic :: Office/Business :: Financial :: Point-Of-Sale",
        # "Topic :: Office/Business :: Financial :: Spreadsheet",
        # "Topic :: Office/Business :: Groupware",
        # "Topic :: Office/Business :: News/Diary",
        # "Topic :: Office/Business :: Office Suites",
        # "Topic :: Office/Business :: Scheduling",
        # "Topic :: Other/Nonlisted Topic",
        # "Topic :: Printing",
        # "Topic :: Religion",
        # "Topic :: Scientific/Engineering",
        # "Topic :: Scientific/Engineering :: Artificial Intelligence",
        # "Topic :: Scientific/Engineering :: Artificial Life",
        # "Topic :: Scientific/Engineering :: Astronomy",
        # "Topic :: Scientific/Engineering :: Atmospheric Science",
        # "Topic :: Scientific/Engineering :: Bio-Informatics",
        # "Topic :: Scientific/Engineering :: Chemistry",
        # "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        # "Topic :: Scientific/Engineering :: GIS",
        # "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        # "Topic :: Scientific/Engineering :: Image Recognition",
        # "Topic :: Scientific/Engineering :: Information Analysis",
        # "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        # "Topic :: Scientific/Engineering :: Mathematics",
        # "Topic :: Scientific/Engineering :: Medical Science Apps.",
        # "Topic :: Scientific/Engineering :: Physics",
        # "Topic :: Scientific/Engineering :: Visualization",
        # "Topic :: Security",
        # "Topic :: Security :: Cryptography",
        # "Topic :: Sociology",
        # "Topic :: Sociology :: Genealogy",
        # "Topic :: Sociology :: History",
        # "Topic :: Software Development",
        # "Topic :: Software Development :: Assemblers",
        # "Topic :: Software Development :: Bug Tracking",
        # "Topic :: Software Development :: Build Tools",
        # "Topic :: Software Development :: Code Generators",
        # "Topic :: Software Development :: Compilers",
        # "Topic :: Software Development :: Debuggers",
        # "Topic :: Software Development :: Disassemblers",
        # "Topic :: Software Development :: Documentation",
        # "Topic :: Software Development :: Embedded Systems",
        # "Topic :: Software Development :: Internationalization",
        # "Topic :: Software Development :: Interpreters",
        # "Topic :: Software Development :: Libraries",
        # "Topic :: Software Development :: Libraries :: Application Frameworks",
        # "Topic :: Software Development :: Libraries :: Java Libraries",
        # "Topic :: Software Development :: Libraries :: Perl Modules",
        # "Topic :: Software Development :: Libraries :: PHP Classes",
        # "Topic :: Software Development :: Libraries :: Pike Modules",
        # "Topic :: Software Development :: Libraries :: pygame",
        # "Topic :: Software Development :: Libraries :: Python Modules",
        # "Topic :: Software Development :: Libraries :: Ruby Modules",
        # "Topic :: Software Development :: Libraries :: Tcl Extensions",
        # "Topic :: Software Development :: Localization",
        # "Topic :: Software Development :: Object Brokering",
        # "Topic :: Software Development :: Object Brokering :: CORBA",
        # "Topic :: Software Development :: Pre-processors",
        # "Topic :: Software Development :: Quality Assurance",
        # "Topic :: Software Development :: Testing",
        # "Topic :: Software Development :: Testing :: Traffic Generation",
        # "Topic :: Software Development :: User Interfaces",
        # "Topic :: Software Development :: Version Control",
        # "Topic :: Software Development :: Version Control :: CVS",
        # "Topic :: Software Development :: Version Control :: RCS",
        # "Topic :: Software Development :: Version Control :: SCCS",
        # "Topic :: Software Development :: Widget Sets",
        # "Topic :: System",
        # "Topic :: System :: Archiving",
        # "Topic :: System :: Archiving :: Backup",
        # "Topic :: System :: Archiving :: Compression",
        # "Topic :: System :: Archiving :: Mirroring",
        # "Topic :: System :: Archiving :: Packaging",
        # "Topic :: System :: Benchmark",
        # "Topic :: System :: Boot",
        # "Topic :: System :: Boot :: Init",
        # "Topic :: System :: Clustering",
        # "Topic :: System :: Console Fonts",
        # "Topic :: System :: Distributed Computing",
        # "Topic :: System :: Emulators",
        # "Topic :: System :: Filesystems",
        # "Topic :: System :: Hardware",
        # "Topic :: System :: Hardware :: Hardware Drivers",
        # "Topic :: System :: Hardware :: Mainframes",
        # "Topic :: System :: Hardware :: Symmetric Multi-processing",
        # "Topic :: System :: Installation/Setup",
        # "Topic :: System :: Logging",
        # "Topic :: System :: Monitoring",
        # "Topic :: System :: Networking",
        # "Topic :: System :: Networking :: Firewalls",
        # "Topic :: System :: Networking :: Monitoring",
        # "Topic :: System :: Networking :: Monitoring :: Hardware Watchdog",
        # "Topic :: System :: Networking :: Time Synchronization",
        # "Topic :: System :: Operating System",
        # "Topic :: System :: Operating System Kernels",
        # "Topic :: System :: Operating System Kernels :: BSD",
        # "Topic :: System :: Operating System Kernels :: GNU Hurd",
        # "Topic :: System :: Operating System Kernels :: Linux",
        # "Topic :: System :: Power (UPS)",
        # "Topic :: System :: Recovery Tools",
        # "Topic :: System :: Shells",
        # "Topic :: System :: Software Distribution",
        # "Topic :: System :: Systems Administration",
        # "Topic :: System :: Systems Administration :: Authentication/Directory",
        # "Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP",
        # "Topic :: System :: Systems Administration :: Authentication/Directory :: NIS",
        # "Topic :: System :: System Shells",
        # "Topic :: Terminals",
        # "Topic :: Terminals :: Serial",
        # "Topic :: Terminals :: Telnet",
        # "Topic :: Terminals :: Terminal Emulators/X Terminals",
        # "Topic :: Text Editors",
        # "Topic :: Text Editors :: Documentation",
        # "Topic :: Text Editors :: Emacs",
        # "Topic :: Text Editors :: Integrated Development Environments (IDE)",
        # "Topic :: Text Editors :: Text Processing",
        # "Topic :: Text Editors :: Word Processors",
        # "Topic :: Text Processing",
        # "Topic :: Text Processing :: Filters",
        # "Topic :: Text Processing :: Fonts",
        # "Topic :: Text Processing :: General",
        # "Topic :: Text Processing :: Indexing",
        # "Topic :: Text Processing :: Linguistic",
        # "Topic :: Text Processing :: Markup",
        # "Topic :: Text Processing :: Markup :: HTML",
        # "Topic :: Text Processing :: Markup :: LaTeX",
        # "Topic :: Text Processing :: Markup :: SGML",
        # "Topic :: Text Processing :: Markup :: VRML",
        # "Topic :: Text Processing :: Markup :: XML",
        # "Topic :: Utilities",

    ],

    ## A string or list of strings specifying what other distributions need to be
    ## present in order for the setup script to run. setuptools will attempt to obtain
    ## these (even going so far as to download them using EasyInstall) before
    ## processing the rest of the setup script or commands. This argument is needed if
    ## you are using distutils extensions as part of your build process; for example,
    ## extensions that process setup() arguments and turn them into EGG-INFO metadata
    ## files.
    ##
    ## (Note: projects listed in setup_requires will NOT be automatically installed on
    ## (the system where the setup script is being run. They are simply downloaded to
    ## (the setup directory if they're not locally available already. If you want them
    ## (to be installed, as well as being available when the setup script is run, you
    ## (should add them to install_requires and setup_requires.)
    # setup_requires = ,


    #########################################################################
    # Optional parameters you probably don't care about and can leave as-is #
    #########################################################################


    ## A dictionary mapping package names to lists of glob patterns that should be
    ## excluded from your package directories. You can use this to trim back any excess
    ## files included by include_package_data.
    # exclude_package_data = ,

    ## A dictionary mapping package names to lists of glob patterns. You do
    ## not need to use this option if you are using include_package_data, unless you
    ## need to add e.g. files that are generated by your setup script and build
    ## process. (And are therefore not in source control or are files that you don't
    ## want to include in your source distribution.)
    # package_data = ,

    ## A boolean (True or False) flag specifying whether the project can be safely
    ## installed and run from a zip file. If this argument is not supplied, the
    ## bdist_egg command will have to analyze all of your project's contents for
    ## possible problems each time it buids an egg.
    # zip_safe = ,

    ## A dictionary mapping entry point group names to strings or lists of strings
    ## defining the entry points. Entry points are used to support dynamic discovery of
    ## services or plugins provided by a project. See Dynamic Discovery of Services and
    ## Plugins for details and examples of the format of this argument. In addition,
    ## this keyword is used to support Automatic Script Creation.
    ##
    ## Use if you want to add new command or argument to setup.py
    ## More details: http://peak.telecommunity.com/DevCenter/setuptools#id52
    ## It can also be used to created commands like `scripts` does, but
    ## in a more cross platform way
    ## More defails: http://peak.telecommunity.com/DevCenter/setuptools#id9
    entry_points = {
        'console_scripts': [
            'zerobin = zerobin.routes:main',
       ]
    }

    ## A list of strings naming the project's "namespace packages". A namespace package
    ## is a package that may be split across multiple project distributions. For
    ## example, Zope 3's zope package is a namespace package, because subpackages like
    ## zope.interface and zope.publisher may be distributed separately. The egg runtime
    ## system can automatically merge such subpackages into a single parent package at
    ## runtime, as long as you declare them in each project that contains any
    ## subpackages of the namespace package, and as long as the namespace package's
    ## __init__.py does not contain any code. See the section below on Namespace
    ## Packages for more information.
    # namespace_packages = ,

    ## A string naming a unittest.TestCase subclass (or a package or module containing
    ## one or more of them, or a method of such a subclass), or naming a function that
    ## can be called with no arguments and returns a unittest.TestSuite. If the named
    ## suite is a module, and the module has an additional_tests() function, it is
    ## called and the results are added to the tests to be run. If the named suite is a
    ## package, any submodules and subpackages are recursively added to the overall
    ## test suite.
    ##
    ## Specifying this argument enables use of the test command to run the specified
    ## test suite, e.g. via setup.py test. See the section on the test command below
    ## for more details.
    # test_suite = ,

    ## If your project's tests need one or more additional packages besides those
    ## needed to install it, you can use this option to specify them. It should be a
    ## string or list of strings specifying what other distributions need to be present
    ## for the package's tests to run. When you run the test command, setuptools will
    ## attempt to obtain these (even going so far as to download them
    ## usingEasyInstall). Note that these required projects will not be installed on
    ## the system where the tests are run, but only downloaded to the project's setup
    ## directory if they're not already installed locally.
    # tests_require = ,

    ## If you would like to use a different way of finding tests to run than what
    ## setuptools normally uses, you can specify a module name and class name in this
    ## argument. The named class must be instantiable with no arguments, and its
    ## instances must support the loadTestsFromNames() method as defined in the Python
    ## unittest module's TestLoader class. Setuptools will pass only one test "name" in
    ## the names argument: the value supplied for the test_suite argument. The loader
    ## you specify may interpret this string in any way it likes, as there are no
    ## restrictions on what may be contained in a test_suite string.
    ##
    ## The module name and class name must be separated by a :. The default value of
    ## this argument is "setuptools.command.test:ScanningLoader". If you want to use
    ## the default unittestbehavior, you can specify "unittest:TestLoader" as your
    ## test_loader argument instead. This will prevent automatic scanning of submodules
    ## and subpackages.
    ##
    ## The module and class you specify here may be contained in another package, as
    ## long as you use the tests_require option to ensure that the package containing
    ## the loader class is available when the test command is run.
    # test_loader = ,

    ## A list of strings naming resources that should be extracted together, if any of
    ## them is needed, or if any C extensions included in the project are imported.
    ## This argument is only useful if the project will be installed as a zipfile, and
    ## there is a need to have all of the listed resources be extracted to the
    ## filesystem as a unit. Resources listed here should be '/'-separated paths,
    ## relative to the source root, so to list a resource foo.png in package bar.baz,
    ## you would include the string bar/baz/foo.png in this argument.
    ##
    ## If you only need to obtain resources one at a time, or you don't have any C
    ## extensions that access other files in the project (such as data files or shared
    ## libraries), you probably do NOT need this argument and shouldn't mess with it.
    ## For more details on how this argument works, see the section below on Automatic
    ## Resource Extraction.
    # eager_resources = ,

    ## defined for compiled extensions. Not tested yet, so can't document
    ## doc here: http://docs.python.org/distutils/setupscript.html#extension-names-and-packages
    # ext_package = ,
    # ext_modules = ,

    ## Like for `user` and `user_email`, but or a serarate maintener
    # maintainer = ,
    # maintainer_email = ,

    ## Like `url`, but where the package should be downloaded from
    ## imcompatible with 2.2.3- or 2.3-
    # download_url = ,

    ## An iterable of string being the names of the platforms the code targets
    ## Use only if you can find it in "classifier"
    # platforms = ,

    ## A string with the name of the licence this code is distributed under
    ## E.G: 'GNU General Public License (GPL), Version 2'
    ## Use only if you can find the licence in "classifier"
    # license= ,

    ## setup() is just a wrapper to create instance of setuptools.Distribution
    ## you can here specify another class to use instead
    # distclass = ,

    ## setup() is just a wrapper to create instance of setuptools.Command
    ## you can here specify another class to use instead
    # cmdclass = ,

    ## A list of strings, or a coma separated string
    ## Anymetadata that match PEP 314 (http://www.python.org/dev/peps/pep-0314/)
    # keywords = ,

    ## Mapping of strings, each key is a package, each is a list of strings
    ## being a glob match pattern of data files to include from the package.
    ##
    ## It's usually better to use the manifest template instead of this parameter.
    ##
    ## E.G: {'foo': ['data/*.json']}
    # package_data=,

    ## Itérable of tuples, each tuple containing a directory path string, and
    ## a list of files path strings from this directory to include.
    ##
    ## The data_files option can be used to specify additional files needed by the
    ## module distribution: configuration files, message catalogs, data files,
    ## anything which doesn’t fit in the previous categories.
    ##
    ## It's usually better to use the manifest template instead of this parameter.
    ##
    ## E.G: [('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
    ##       ('config', ['cfg/data.cfg']),
    ##       ('/etc/init.d', ['init-script'])]
    # data_files = ,


    ## A mapping of strings / iterable, the key being the name of a extra
    ## feature, and the iterable containing dependancy names.
    ## Sometimes a project has "recommended" dependencies, that are not required
    ## for all uses of the project. For example, a project might offer optional PDF
    ## output if ReportLab is installed, and reStructuredText support if docutils
    ## is installed. These optional features are called "extras", and setuptools
    ## allows you to define their requirements as well.
    ##
    ## E.G: {'PDF':  ["ReportLab>=1.2", "RXP"],  'reST': ["docutils>=0.3"]}
    # extras_require = ,


)

















