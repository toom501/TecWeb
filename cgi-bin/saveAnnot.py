#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import json
import urllib2
# enable debugging
import cgitb
cgitb.enable()

path = "../html/project/json/"

data = json.load(sys.stdin)
link = data['nomeFile']
# creo il path ralativo dove andare a salvare le annotazioni
url = (path, link)
urlF = "".join(url)
# apro un file e ci salvo le parti che estraggo
with open(urlF, 'w') as outfile:
   json.dump(data, outfile, indent=4, separators=(',', ': '))


print "Content-type: application/json\n\n";
print 




