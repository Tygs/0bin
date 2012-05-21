#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4


"""
	Exctract usefull infos from web server logs
"""

import re


# define your web server logs path
LOGS_PATH = "/var/log/nginx/access_0bin.log"


rexp = re.compile('(\d+\.\d+\.\d+\.\d+) - - \[([^\[\]:]+):(\d+:\d+:\d+) -(\d\d\d\d\)] ("[^"]*")(\d+) (-|\d+) ("[^"]*") (".*")\s*\Z')


f = open(LOGS_PATH, 'r') 

for line in f:
    a = rexp.match(line)

    if not a is None:
        # a.group(1) #IP address
        # a.group(2) #day/month/year
        # a.group(3) #time of day
        # a.group(4) #timezone
        # a.group(5) #request
        # a.group(6) #code 200 for success, 404 for not found, etc.
        # a.group(7) #bytes transferred
        # a.group(8) #referrer
        # a.group(9) #browser
        print a.group(8) #referrer

f.close()