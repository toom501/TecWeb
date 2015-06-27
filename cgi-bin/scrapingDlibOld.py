#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import html
import httplib
import re
import json
import sys

tip1 = "Date and Volume: "
tip2 = "Authors: "
tip3 = "Title: "

url = json.load(sys.stdin)
#url = JSON.load(sys.stdin.read())		# /project/document/articolo.html
#url = "/project/documents/Annota:_Towards_Enriching_Scientific_Publications_with_Semantics_and_User_Annotations"
x = "../html/project/json/"
docName = re.sub('/project/documents/', '', url, count=1)
docName = re.sub('.html', '', docName, count = 1)
docName += "_scraping.json"
x += docName
 
my_data = []

############################# scraping Dlib
conn = httplib.HTTPConnection("ltw1514.web.cs.unibo.it")										
conn.request("GET",url)
res = conn.getresponse()
body = res.read()

my_page = html.fromstring(body)
	
#print(url,docName,x,my_page)													
date = my_page.xpath("//p[@class='blue'][1]")[0].text_content().encode("utf8")
#date = str.replace(date,"\n", "")
#date = re.sub(' ', '', date, count=10)
#date = re.sub('Table of Contents', '',date, count=1)
authors = my_page.xpath("//p[@class='blue'][2]")[0].text_content().encode("utf8")
#authors = str.replace(authors,"\n", " ")
title = my_page.xpath("//td/h3[2]")[0].text_content().encode("utf8")
keywords = my_page.xpath("//p[@class='blue'][5]")[0].text_content().encode("utf8")





my_data = [tip1+date, tip2+authors, tip3+title, keywords]
#my_data = [{"date": date, "authors": authors, "title": title, "keywords": keywords}]
with open(x, 'w+') as outfile:				#path/nome documento+scraping.json 
	json.dump(my_data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
	
print "Content-Type: application/json; charset=utf-8"
print
