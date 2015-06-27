#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import html, etree
import sys
import httplib
import json

# proxy
#proxyHost = "217.29.167.157"
# proxy port
#proxyPort = "80"
# variabile contenente la lista dei link in formato html
listOfLink = []
# variabile contenente la lista degli indirizzi da dove caricare gli articoli
listOfURL = ["www.dlib.org/dlib/november14/11contents.html","www.dlib.org/dlib/january13/01contents.html","rivista-statistica.unibo.it/issue/view/467","almatourism.unibo.it/issue/current","encp.unibo.it/issue/current"]
for url in listOfURL:
	domain = url[:url.index("/")]
	path = url[url.index("/"):]
	# avvio la connessione 
	conn = httplib.HTTPConnection (domain) #(proxyHost, proxyPort) 										
	conn.request("GET", path) #"http://"+url)
	res = conn.getresponse()
	body = res.read()
	# ottengo il formato html della stringa contente l'html della pagina
	tree = html.fromstring(body)
	# documento Dlib -> devo cercare i link in un determinato xpath
	if (domain == "www.dlib.org"):
		xpath = "//table[3]//td[1]//p[@class=\"contents\"]//a"
	else:
		xpath = "//td[@class=\"tocTitle\"]//a"

	# conto quanti link devo caricare
	numberOfLink = len(tree.xpath(xpath))
	# ogni link viene estratto e aggiunto alla lista
	for x in xrange(0, numberOfLink):
		link = tree.xpath(xpath)[x]
		# rendo assoluti i link
		link.make_links_absolute("http://"+domain+path, resolve_base_href=True)
		htmlLink = etree.tostring(link, method="html")
		listOfLink.append(htmlLink)
	
# ritorno un json contenente la lista dei link html della pagina
print "Content-Type: application/json\n\n"
json.dump(listOfLink, sys.stdout, indent=2)
