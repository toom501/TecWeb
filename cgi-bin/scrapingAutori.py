#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import html,etree
import httplib
import re
import json
import sys
import datetime
import rdflib
#from rdflib.Namespace import RDF
from rdflib import Namespace
from rdflib import Literal
from rdflib import BNode
from rdflib import URIRef


articolo = "/brook/11brook.html"
#articolo = json.load(sys.stdin)   #/../.. .html
rivista = "/dlib/november14"
conn = httplib.HTTPConnection("dlib.org")										
conn.request("GET",rivista+articolo)
res = conn.getresponse()
body = res.read()

my_page = html.fromstring(body)
k = 1
bla = []
for i in range(0,30):
	if k==1 :
		authors = my_page.xpath("//p[@class='blue'][2]/text()")[i].encode("utf8").strip()
		bla += [authors]
		k = k+1
	else : 
		try:
			authors = my_page.xpath("//p[@class='blue'][2]/text()")[i].encode("utf8").strip()		
			if ","  in authors:
				continue
			if "@" in authors:
				continue
			bla += [authors]
		except IndexError:
			break

print bla

"""

doi = my_page.xpath("//p[@class='blue'][2]/text()")[9].encode("utf8").strip()
print doi

authorString = my_page.xpath("//p[@class='blue'][2]/text()")[0].encode("utf8").strip()
anc = my_page.xpath("//p[@class='blue'][2]")[0]
for ancestor in anc.iterancestors():
	#print ancestor.index(ancestor.getchild())
	print ancestor.tag
auth = []
authors = authorString.split(' ')
for word in authors :
	if word.startswith("and") != True :
		auth += [word]
	else :
		break
auth1 = auth[0][0]
firstauthor = auth[0]+" "+auth[1]
auth1b = auth1.lower()
auth2 = auth[1].lower()
	
idauth = auth1b+"-"+auth2 


#authors = author.rstrip('and')
#authors = my_page.xpath("substring-before(authx, '<br>')").encode("utf8")
#authors = my_page.xpath(substring-before(authx, "<br>")) 
#and substring-before(authx, "<br>"))
#path = my_page.xpath(my_page.getpath(authx))
#au = my_page.xpath("//p[@class='blue'][2]")[0]
#path = getpath(au)
#print bla
#print path

#authors = substring-before(authors, "<br>")
"""
