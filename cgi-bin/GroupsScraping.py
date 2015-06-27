#!/usr/bin/env python
# -*- coding: utf-8 -*-
print 
from lxml import html
import httplib
import json
import sys


conn = httplib.HTTPConnection("vitali.web.cs.unibo.it")										
conn.request("GET","/TechWeb15/ProgettoDelCorso")
res = conn.getresponse()
body = res.read()

groups = []
my_page = html.fromstring(body)

for row in my_page.xpath("//table//tr[position()>1]"):														
    groupID = row.xpath("th[@class='twikiFirstCol']//font/node()")  #group = row.xpath("th[1]//font/text()")
    groupName = row.xpath("th[2]//font/node()")
    ident = ''.join(groupID)
    name = ''.join(groupName)
    my_row = [{"id": ident, "name": name}]
    groups += my_row
    
#print groups

#print groups
#with open('../html/project/json/listaGruppi.json', 'w') as outfile:
#    json.dump(groups, outfile)

#print "Content-Type: application/json\n\n"
json.dump(groups, sys.stdout, indent=2)
	

