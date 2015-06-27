#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import html
import httplib
import re
import json
import sys
import datetime


url = json.load(sys.stdin)		# /project/document/articolo.html
x = "../html/project/json/"
docName = re.sub('/project/documents/', '', url, count=1)
docName = re.sub('.html', '', docName, count = 1)
name = docName
docName += "_scraping.json"
x += docName
i = 0
k = 5
my_data = []

def filljson(nome_dict, type, label, subject, predicate, literal, targetid, source, start, end, time, datiid, widget, iddad, pos):
	nome_dict = {}
	nome_dict["annotations"] = ["type"]
	nome_dict["annotations"][0] = {} 
	nome_dict["annotations"][0]["type"] = type
	nome_dict["annotations"][0]["label"] = label
	nome_dict["annotations"][0]["body"] = {}
	nome_dict["annotations"][0]["body"]["subject"] = subject
	nome_dict["annotations"][0]["body"]["predicate"] = predicate
	nome_dict["annotations"][0]["body"]["literal"] = literal
	nome_dict["target"] = {}
	nome_dict["target"]["source"] = source
	nome_dict["target"]["id"] = targetid
	nome_dict["target"]["start"] = int(start)
	nome_dict["target"]["end"] = int(end)
	nome_dict["provenance"] = {}
	nome_dict["provenance"]["author"] = {}
	nome_dict["provenance"]["author"]["name"] = "webscraping"
	nome_dict["provenance"]["author"]["email"] = "webscraping@lela.it"
	nome_dict["provenance"]["time"] = time
	nome_dict["dati"] = {}
	nome_dict["dati"]["id"] = datiid
	nome_dict["dati"]["widget"] = widget
	nome_dict["dati"]["idDad"] = iddad
	nome_dict["dati"]["pos"] = int(pos)
	return nome_dict


############################# scraping Dlib
conn = httplib.HTTPConnection("ltw1514.web.cs.unibo.it")										
conn.request("GET",url)
res = conn.getresponse()
body = res.read()

my_page = html.fromstring(body)
	
time = str(datetime.datetime.now())
	

date = my_page.xpath("//p[@class='blue'][1]")[0].text_content().encode("utf8")
#parent = my_page.xpath("//p[@class='blue'][1]")[0].getparent()
#date = str.replace(date,"\n", " ")
#date = re.sub(' ', '', date, count=10)
#date = re.sub('Table of Contents', '',date, count=1)
end = str(len(date))
date_dict = {}
date_dict = filljson(date_dict, "hasPublicationYear", "", name, "webscraping:hasPublicationYear", date, "bo", date, 0, end, time, "", "", "p-0", 0)


authors = my_page.xpath("//p[@class='blue'][2]")[0].text_content().encode("utf8")
#authors = str.replace(authors,"\n", " ")
end1 = str(len(authors))
authors_dict = {}
authors_dict = filljson(authors_dict, "hasAuthor", "", name, "dcterms:creator", authors, "bo", authors, 0, end1, time, "", "", "p-1", 0)


title = my_page.xpath("//td/h3[2]")[0].text_content().encode("utf8")
end2 = str(len(title))
title_dict = {}
title_dict = filljson(title_dict, "hasTitle", "", name, "dcterms:title", title, "bo", title, 0, end2, time, "", "", "h3-4", 0)



try:
	keywords = my_page.xpath("//p[@class='blue'][5]")[0].text_content().encode("utf8")
except IndexError:
	my_data = date_dict, authors_dict, title_dict
	pass
else:	
	if keywords.startswith("Keywords:") :
		end3 = str(len(keywords))
		keywords_dict = {}
		keywords_dict = filljson(keywords_dict, "denotesRhetoric", "", name, "sem:denotes", keywords, "bo", keywords, 0, end3, time, "", "", "p-4", 0)
		my_data = date_dict,authors_dict, title_dict, keywords_dict
	else :
		my_data = date_dict, authors_dict, title_dict

for h3 in my_page.xpath("//table[1]//td[2]//h3[@class!='blue-space'] | //table[1]//td[2]//h3[not(@*)]"):
	subtitle = h3.xpath("self::h3")[0].text_content().encode("utf8")
	end4 = str(len(subtitle))
	subtitle_dictName = "subtitle"+str(i)+"_dict"
	subtitle_dict = filljson(subtitle_dictName, "denotesRhetoric", "", "", "", "", "bo", subtitle, 0, end4, time, "", "", "h3-"+str(k), 0) #start 3?
	subtitle_tuple = (subtitle_dict,)
	my_data = my_data + subtitle_tuple
	i = i+1
	k = k+1

with open(x, 'w+') as outfile:				#path/nome documento+scraping.json 
	json.dump(my_data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
	
print "Content-Type: application/json; charset=utf-8"
print
