#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os
import zerobin

from setuptools import setup, find_packages

src_directory = 'zerobin'

open('MANIFEST.in', 'w').write('\n'.join((

    "include *.rst *.tx",
    "recursive-include %s *.png *.jpg *.gif *.ico" % src_directory,
    "recursive-include %s *.css *.js *.swf" % src_directory,
    "recursive-include %s *.tpl" % src_directory
)))


setup(

    name="zerobin",
    version=zerobin.__version__,
    packages=find_packages(exclude=["libs", "libs.*"]),
    author="Sam et Max",
    author_email="lesametlemax@gmail.com",
    description="An client side encrypted pastebin",
    long_description=open('README.rst').read(),
    install_requires=[
        'cherrypy',
        'bottle',
        'clize',
        'lockfile',
    ],
    include_package_data=True,
    dependency_links=[
        'http://www.subspacefield.org/security/privilege/code/privilege/'
    ],
    classifiers=[
        'Programming Language :: Python',
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: zlib/libpng License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
    ],
    entry_points = {
        'console_scripts': [
            'zerobin = zerobin.cmd:main',
       ]
    }

)

















