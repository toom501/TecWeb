#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import html, etree
import sys
import httplib
import json


# proxy
proxyHost = "217.29.167.157"
# proxy port
proxyPort = "80"
indexToStart = 0
url = json.load(sys.stdin) # link dell'articolo in formato http://www.example.com/path/of/file
# in base a http o https scelgo a quale indice inziare per ricavare dominio e path
if (url.find("https://") == 0):
	indexToStart = 8
else :
	indexToStart = 7
# data contiene il dominio+path
data = url[indexToStart:]
domain = data[:data.index("/")]
path = data[data.index("/"):]
# eseguo connessione HTTP al dominio
#conn = httplib.HTTPConnection(domain)
# eseguo una GET al path riferito a dominio
#conn.request("GET", path)
conn = httplib.HTTPConnection (domain) #(proxyHost, proxyPort)										
conn.request("GET", path)#url)
res = conn.getresponse()
body = res.read()
# ottengo il formato html della stringa contente l'html della pagina
tree = html.fromstring(body)

if (domain == "www.dlib.org"):
	xpath = "//table[3]//table[5]//td[2]"
elif (data.find(".unibo.it") >= 0):
	xpath = "//div[@id=\"content\"]"
else :
	xpath = "//body"
try:
	tree2 = tree.xpath(xpath)[0]
except IndexError:
	tree2 = tree.xpath("//body")[0]

# elimino il banner dei cookie presente in alcune pagine unibo.it
for cookie in tree2.xpath("//div[@id=\"cookiesAlert\"]"):
    cookie.getparent().remove(cookie)

# ogni <script> presente dentro il path viene rimosso per evitare problemi nel caricamento del documento. In genere il problema avveniva con Google Analitics.
for script in tree2.xpath("//script"):
    script.getparent().remove(script)     

tree2.make_links_absolute(url, resolve_base_href=True)
response = etree.tostring(tree2, method="html")

# ritorno un json contenente la lista dei link html della pagina
print "Content-Type: application/json\n\n"
json.dump(response, sys.stdout, indent=2)
