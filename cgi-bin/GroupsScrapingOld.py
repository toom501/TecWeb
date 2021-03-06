#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
import httplib
import json
# enable debugging
import cgitb
cgitb.enable()

conn = httplib.HTTPConnection("vitali.web.cs.unibo.it")										
conn.request("GET","/TechWeb15/ProgettoDelCorso")
res = conn.getresponse()
body = res.read()

groups = []
my_page = html.fromstring(body)

for row in my_page.xpath("//table//tr[position()>1]"):														
    groupID = row.xpath("th[@class='twikiFirstCol']//font/text()")   #group = row.xpath("th[1]//font/text()")
    groupName = row.xpath("th[2]//font/text()")
    print (groupID, groupName)
    my_row = [{"id": groupID, "name": groupName }]
    groups += my_row 
    #print(groups)

with open('../html/project/json/listaGruppi.json', 'w') as outfile:
    json.dump(groups, outfile)

print "Content-Type: application/json; charset=utf-8"
print 