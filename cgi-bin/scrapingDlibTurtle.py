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


RASCH = Namespace("http://vitali.web.cs.unibo.it/raschietto/person/")
#px_AU =         "prefix au:        <http://description.org/schema/>"
#px_BIF =        "prefix bif:       <http://www.openlinksw.com/schema/sparql/extensions#>"
#px_CITO =       "prefix cito:      <http://purl.org/spar/cito/>"
#px_DBPEDIA =    "prefix dbpedia:   <http://dbpedia.org/resource/>"
DCTERMS = Namespace("http://purl.org/dc/terms/")
FABIO =      Namespace("http://purl.org/spar/fabio/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
FRBR = Namespace("http://purl.org/vocab/frbr/core#")
OA = Namespace("http://www.w3.org/ns/oa#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
SCHEMA = Namespace("http://schema.org/")
#SEM =        "prefix sem:       <http://www.ontologydesignpatterns.org/cp/owl/semiotics.owl#>"  
#px_SKOS =       "prefix skos:      <http://www.w3.org/2004/02/skos/core#>"
#px_XML =        "prefix xml:       <http://www.w3.org/XML/1998/namespace>"
#px_XSD =        "prefix xsd:       <http://www.w3.org/2001/XMLSchema#>"
DLIB = Namespace("http://www.dlib.org/dlib/november14")
articolo = "/beel/11beel.html"
#articolo = json.load(sys.stdin)   #/../.. .html
rivista = "/dlib/november14"
conn = httplib.HTTPConnection("dlib.org")										
conn.request("GET",rivista+articolo)
res = conn.getresponse()
body = res.read()

my_page = html.fromstring(body)
"""
bla = []
for i in range(0,10):
	authors = my_page.xpath("//p[@class='blue'][2]/text()")[i].encode("utf8").strip()
	if "@" in authors:
		continue
	bla += [authors]
print bla
for i in bla:
	end = len(i)
"""

doi = my_page.xpath("//p[@class='blue'][2]/text()")[9].encode("utf8").strip()
print doi

authorString = my_page.xpath("//p[@class='blue'][2]/text()")[0].encode("utf8").strip()
anc = my_page.xpath("//p[@class='blue'][2]")[0]
for ancestor in anc.iterancestors():
	#print ancestor.index(ancestor.getchild())
	print ancestor.tag
auth = []
authors = authorString.split(' ')    #suddivido la stringa in una lista di parole 
for word in authors :
	if word.startswith("and") != True :
		auth += [word]			#prendo le parole prima di "and"
	else :
		break
auth1 = auth[0][0]				#prima lettera prima parola
firstauthor = auth[0]+" "+auth[1]		#nome e cognome
auth1b = auth1.lower()				#prima lettera nome in minuscolo
auth2 = auth[1].lower()				#
	
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

#def creaAnnotAut()
annotation = BNode()
target = BNode()
selector = BNode()
author = BNode()
url= ""
valore = "id"
start = 0
end = len(authorString)
nome = "Autore"
time = str(datetime.datetime.now())
rdf = rdflib.Graph()
rdf.add((annotation, RDF.type, OA.Annotation))
rdf.add((annotation, RDFS.label, Literal("Autore")))
rdf.add((annotation, OA.hasTarget, target))
rdf.add((target, RDF.type, OA.SpecificResource))
rdf.add((target, OA.hasSource, DLIB[articolo]))
rdf.add((target, OA.hasSelector, selector))
rdf.add((selector, RDF.type, OA.FragmentSelector))
rdf.add((selector, RDF.value, Literal(valore)))
rdf.add((selector, OA.start, Literal(start)))
rdf.add((selector, OA.end, Literal(end)))
rdf.add((annotation, OA.hasBody, author))
rdf.add((annotation, OA.annotatedBy, URIRef("mailto:web@unibo.it")))
rdf.add((annotation, OA.annotatedAt, Literal(time)))
rdf.add((author, RDF.type, RDF.Statement))
rdf.add((author, RDF.subject, FABIO.Work))
rdf.add((author, RDF.predicate, DCTERMS.creator))
rdf.add((author, RDF.object, RASCH[idauth]))
rdf.add((author, RDFS.label, Literal("un autore del documento è "+firstauthor)))
rdf.add((RASCH[idauth], RDFS.label, Literal(firstauthor)))
rdf.add((URIRef("mailto:web@unibo.it"), FOAF.name, Literal("webscraping")))
rdf.add((URIRef("mailto:web@unibo.it"), SCHEMA.mail, Literal("webscraping@unibo.it")))

#print rdf.serialize(format="n3")
rdf.serialize("graph.owl", format="pretty-xml")

print "Content-Type: application/json; charset=utf-8"
print 
