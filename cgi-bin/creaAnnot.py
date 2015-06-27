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
from rdflib import plugin


RASCH = Namespace("http://vitali.web.cs.unibo.it/raschietto/person/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
FABIO = Namespace("http://purl.org/spar/fabio/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
FRBR = Namespace("http://purl.org/vocab/frbr/core#")
OA = Namespace("http://www.w3.org/ns/oa#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
SCHEMA = Namespace("http://schema.org/")
PRISM = Namespace("http://prismstandard.org/namespaces/basic/2.0/")
SEM = Namespace("http://www.ontologydesignpatterns.org/cp/owl/semiotics.owl#")
CITO = Namespace("http://purl.org/spar/cito/")
DEO = Namespace("http://vitali.web.cs.unibo.it/raschietto/deo/")
SRO = Namespace("http://vitali.web.cs.unibo.it/raschietto/sro/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DEOLESS = Namespace("http://vitali.web.cs.unibo.it/raschietto/")
###################################################################### switch case 
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False
########################################################################


#rdf = rdflib.Graph(store='Sleepycat')
# first time create the store:
#rdf.open('/home/web/ltw1514/cgi-bin', create = True)

rdf = rdflib.Graph()

data = []
#data = json.load(sys.stdin)
data = ["hasAuthor","articolo.html","id",0,123,"nome autore","nome creatore","mailcreatore@unibo.it","http://www.dlib.org/dlib/november14/"]

tipo = data[0]
prefix = data[8]
SITE = Namespace(prefix)


def creaAnnotAutore(articolo, valore, start, end, authorName, creatorName, creatorMail):
	annotation = BNode()
	target = BNode()
	selector = BNode()
	author = BNode()
	#url= ""
	#valore = "id"
	#start = 0
	#end = len(authorString)
	time = str(datetime.datetime.now())
	idauth = "idauth"
	res = re.sub('.html', '',articolo) 
	exp = res+"_ver1"
	
	rdf.add((annotation, RDF.type, OA.Annotation))
	rdf.add((annotation, RDFS.label, Literal("Autore")))
	rdf.add((annotation, OA.hasTarget, target))
	rdf.add((target, RDF.type, OA.SpecificResource))
	rdf.add((target, OA.hasSource, SITE[articolo]))
	rdf.add((target, OA.hasSelector, selector))
	rdf.add((selector, RDF.type, OA.FragmentSelector))
	rdf.add((selector, RDF.value, Literal(valore)))
	rdf.add((selector, OA.start, Literal(start, datatype=XSD.nonNegativeInteger)))
	rdf.add((selector, OA.end, Literal(end, datatype=XSD.nonNegativeInteger)))
	rdf.add((annotation, OA.hasBody, author))
	rdf.add((annotation, OA.annotatedBy, URIRef("mailto:"+creatorMail)))
	rdf.add((annotation, OA.annotatedAt, Literal(time)))
	rdf.add((author, RDF.type, RDF.Statement))
	rdf.add((author, RDF.subject, SITE[res]))              #
	rdf.add((author, RDF.predicate, DCTERMS.creator))
	rdf.add((author, RDF.object, RASCH[idauth]))
	rdf.add((author, RDFS.label, Literal("un autore del documento e' "+authorName)))
	rdf.add((SITE[res], RDF.type, FABIO.Work))		#
	rdf.add((SITE[res], FABIO.hasPortrayal, SITE[articolo])) #
	rdf.add((SITE[res], FRBR.realization, SITE[exp]))        #
	rdf.add((RASCH[idauth], RDFS.label, Literal(authorName)))

	rdf.add((URIRef("mailto:"+creatorMail), FOAF.name, Literal(creatorName)))
	rdf.add((URIRef("mailto:"+creatorMail), SCHEMA.mail, Literal(creatorMail)))
	
	rdf.add((SITE[exp], RDF.type, FABIO.Expression))		#
	rdf.add((SITE[exp], FABIO.hasRepresentation, SITE[articolo]))	#
	rdf.add((SITE[articolo], RDF.type, FABIO.Item))			#

##################################################################################################
def creaAnnotDate(articolo, valore, start, end, dateSelection, creatorName, creatorMail):
	annotation = BNode()
	target = BNode()
	selector = BNode()
	date = BNode()
	time = str(datetime.datetime.now())
	res = re.sub('.html', '',articolo)
	exp = res+"_ver1"
	
	rdf.add((annotation, RDF.type, OA.Annotation))
	rdf.add((annotation, RDFS.label, Literal("Data")))
	rdf.add((annotation, OA.hasTarget, target))
	rdf.add((target, RDF.type, OA.SpecificResource))
	rdf.add((target, OA.hasSource, SITE[articolo]))
	rdf.add((target, OA.hasSelector, selector))
	rdf.add((selector, RDF.type, OA.FragmentSelector))
	rdf.add((selector, RDF.value, Literal(valore)))
	rdf.add((selector, OA.start, Literal(start, datatype=XSD.nonNegativeInteger)))
	rdf.add((selector, OA.end, Literal(end, datatype=XSD.nonNegativeInteger)))
	rdf.add((annotation, OA.hasBody, date))
	rdf.add((annotation, OA.annotatedBy, URIRef("mailto:"+creatorMail)))
	rdf.add((annotation, OA.annotatedAt, Literal(time)))
	rdf.add((date, RDF.type, RDF.Statement))
	rdf.add((date, RDF.subject, SITE[exp]))		#
	rdf.add((date, RDF.predicate, FABIO.hasPublicationYear))
	rdf.add((date, RDF.object, Literal(dateSelection, datatype=XSD.date)))
	rdf.add((URIRef("mailto:"+creatorMail), FOAF.name, Literal(creatorName)))
	rdf.add((URIRef("mailto:"+creatorMail), SCHEMA.mail, Literal(creatorMail)))
	
	rdf.add((SITE[res], RDF.type, FABIO.Work))		#
	rdf.add((SITE[res], FABIO.hasPortrayal, SITE[articolo])) #
	rdf.add((SITE[res], FRBR.realization, SITE[exp]))        #
	rdf.add((SITE[exp], RDF.type, FABIO.Expression))		#
	rdf.add((SITE[exp], FABIO.hasRepresentation, SITE[articolo]))	#
	rdf.add((SITE[articolo], RDF.type, FABIO.Item))			#
	
def creaAnnotTitle(articolo, valore, start, end, titleSelection, creatorName, creatorMail):
	annotation = BNode()
	target = BNode()
	selector = BNode()
	title = BNode()
	time = str(datetime.datetime.now())
	res = re.sub('.html', '',articolo)
	exp = res+"_ver1"
	
	rdf.add((annotation, RDF.type, OA.Annotation))
	rdf.add((annotation, RDFS.label, Literal("Titolo")))
	rdf.add((annotation, OA.hasTarget, target))
	rdf.add((target, RDF.type, OA.SpecificResource))
	rdf.add((target, OA.hasSource, SITE[articolo]))
	rdf.add((target, OA.hasSelector, selector))
	rdf.add((selector, RDF.type, OA.FragmentSelector))
	rdf.add((selector, RDF.value, Literal(valore)))
	rdf.add((selector, OA.start, Literal(start, datatype=XSD.nonNegativeInteger)))
	rdf.add((selector, OA.end, Literal(end, datatype=XSD.nonNegativeInteger)))
	rdf.add((annotation, OA.hasBody, title))
	rdf.add((annotation, OA.annotatedBy, URIRef("mailto:"+creatorMail)))
	rdf.add((annotation, OA.annotatedAt, Literal(time)))
	rdf.add((title, RDF.type, RDF.Statement))
	rdf.add((title, RDF.subject, SITE[exp]))		#
	rdf.add((title, RDF.predicate, DCTERMS.title))
	rdf.add((title, RDF.object, Literal(titleSelection, datatype=XSD.string)))
	rdf.add((URIRef("mailto:"+creatorMail), FOAF.name, Literal(creatorName)))
	rdf.add((URIRef("mailto:"+creatorMail), SCHEMA.mail, Literal(creatorMail)))
	
	rdf.add((SITE[res], RDF.type, FABIO.Work))		#
	rdf.add((SITE[res], FABIO.hasPortrayal, SITE[articolo])) #
	rdf.add((SITE[res], FRBR.realization, SITE[exp]))        #
	rdf.add((SITE[exp], RDF.type, FABIO.Expression))		#
	rdf.add((SITE[exp], FABIO.hasRepresentation, SITE[articolo]))	#
	rdf.add((SITE[articolo], RDF.type, FABIO.Item))			#

def creaAnnotDOI(articolo, valore, start, end, doiSelection, creatorName, creatorMail):
	annotation = BNode()
	target = BNode()
	selector = BNode()
	doi = BNode()
	time = str(datetime.datetime.now())
	res = re.sub('.html', '',articolo)
	exp = res+"_ver1"
	
	rdf.add((annotation, RDF.type, OA.Annotation))
	rdf.add((annotation, RDFS.label, Literal("DOI")))
	rdf.add((annotation, OA.hasTarget, target))
	rdf.add((target, RDF.type, OA.SpecificResource))
	rdf.add((target, OA.hasSource, SITE[articolo]))
	rdf.add((target, OA.hasSelector, selector))
	rdf.add((selector, RDF.type, OA.FragmentSelector))
	rdf.add((selector, RDF.value, Literal(valore)))
	rdf.add((selector, OA.start, Literal(start, datatype=XSD.nonNegativeInteger)))
	rdf.add((selector, OA.end, Literal(end, datatype=XSD.nonNegativeInteger)))
	rdf.add((annotation, OA.hasBody, doi))
	rdf.add((annotation, OA.annotatedBy, URIRef("mailto:"+creatorMail)))
	rdf.add((annotation, OA.annotatedAt, Literal(time)))
	rdf.add((doi, RDF.type, RDF.Statement))
	rdf.add((doi, RDF.subject, SITE[exp]))			#
	rdf.add((doi, RDF.predicate, PRISM.doi))
	rdf.add((doi, RDF.object, Literal(doiSelection, datatype=XSD.string)))
	rdf.add((URIRef("mailto:"+creatorMail), FOAF.name, Literal(creatorName)))
	rdf.add((URIRef("mailto:"+creatorMail), SCHEMA.mail, Literal(creatorMail)))
	
	rdf.add((SITE[res], RDF.type, FABIO.Work))		#
	rdf.add((SITE[res], FABIO.hasPortrayal, SITE[articolo])) #
	rdf.add((SITE[res], FRBR.realization, SITE[exp]))        #
	rdf.add((SITE[exp], RDF.type, FABIO.Expression))		#
	rdf.add((SITE[exp], FABIO.hasRepresentation, SITE[articolo]))	#
	rdf.add((SITE[articolo], RDF.type, FABIO.Item))			#
	
def creaAnnotURL(articolo, valore, start, end, URLSelection, creatorName, creatorMail):
	annotation = BNode()
	target = BNode()
	selector = BNode()
	url = BNode()
	time = str(datetime.datetime.now())
	res = re.sub('.html', '',articolo)
	exp = res+"_ver1"
	
	rdf.add((annotation, RDF.type, OA.Annotation))
	rdf.add((annotation, RDFS.label, Literal("URL")))
	rdf.add((annotation, OA.hasTarget, target))
	rdf.add((target, RDF.type, OA.SpecificResource))
	rdf.add((target, OA.hasSource, SITE[articolo]))
	rdf.add((target, OA.hasSelector, selector))
	rdf.add((selector, RDF.type, OA.FragmentSelector))
	rdf.add((selector, RDF.value, Literal(valore)))
	rdf.add((selector, OA.start, Literal(start, datatype=XSD.nonNegativeInteger)))
	rdf.add((selector, OA.end, Literal(end, datatype=XSD.nonNegativeInteger)))
	rdf.add((annotation, OA.hasBody, url))
	rdf.add((annotation, OA.annotatedBy, URIRef("mailto:"+creatorMail)))
	rdf.add((annotation, OA.annotatedAt, Literal(time)))
	rdf.add((url, RDF.type, RDF.Statement))
	rdf.add((url, RDF.subject, SITE[exp]))			#
	rdf.add((url, RDF.predicate, FABIO.hasURL))
	rdf.add((url, RDF.object, Literal(URLSelection, datatype=XSD.anyURI)))
	rdf.add((URIRef("mailto:"+creatorMail), FOAF.name, Literal(creatorName)))
	rdf.add((URIRef("mailto:"+creatorMail), SCHEMA.mail, Literal(creatorMail)))
	
	rdf.add((SITE[res], RDF.type, FABIO.Work))		#
	rdf.add((SITE[res], FABIO.hasPortrayal, SITE[articolo])) #
	rdf.add((SITE[res], FRBR.realization, SITE[exp]))        #
	rdf.add((SITE[exp], RDF.type, FABIO.Expression))		#
	rdf.add((SITE[exp], FABIO.hasRepresentation, SITE[articolo]))	#
	rdf.add((SITE[articolo], RDF.type, FABIO.Item))			#
	
def creaAnnotRhetoric(articolo, valore, start, end, rhetoricSelection, creatorName, creatorMail):   #aggiungere variabile rhetoric che indica il tipo di selezione: introduction,abstract,conclusion....
	annotation = BNode()
	target = BNode()
	selector = BNode()
	rhetoric = BNode() #variabile
	time = str(datetime.datetime.now())
	res = re.sub('.html', '',articolo)
	exp = res+"_ver1"
	sel = articolo+"#"+valore+"-"+start+"-"+end
	
	rdf.add((annotation, RDF.type, OA.Annotation))
	rdf.add((annotation, RDFS.label, Literal("Retorica")))
	rdf.add((annotation, OA.hasTarget, target))
	rdf.add((target, RDF.type, OA.SpecificResource))
	rdf.add((target, OA.hasSource, SITE[articolo]))
	rdf.add((target, OA.hasSelector, selector))
	rdf.add((selector, RDF.type, OA.FragmentSelector))
	rdf.add((selector, RDF.value, Literal(valore)))
	rdf.add((selector, OA.start, Literal(start, datatype=XSD.nonNegativeInteger)))
	rdf.add((selector, OA.end, Literal(end, datatype=XSD.nonNegativeInteger)))
	rdf.add((annotation, OA.hasBody, rhetoric))
	rdf.add((annotation, OA.annotatedBy, URIRef("mailto:"+creatorMail)))
	rdf.add((annotation, OA.annotatedAt, Literal(time)))
	rdf.add((rhetoric, RDF.type, RDF.Statement))
	rdf.add((rhetoric, RDF.subject, SITE[sel]))    #parametro?
	rdf.add((rhetoric, RDF.predicate, SEM.denotes))
	rdf.add((rhetoric, RDF.object, DEO.Introduction))			#deo namespace? Introduction variabile?
	rdf.add((rhetoric, RDFS.label, Literal(rhetoric)))
	rdf.add((URIRef("mailto:"+creatorMail), FOAF.name, Literal(creatorName)))
	rdf.add((URIRef("mailto:"+creatorMail), SCHEMA.mail, Literal(creatorMail)))
	
	rdf.add((SITE[res], RDF.type, FABIO.Work))		#
	rdf.add((SITE[res], FABIO.hasPortrayal, SITE[articolo])) #
	rdf.add((SITE[res], FRBR.realization, SITE[exp]))        #
	rdf.add((SITE[exp], RDF.type, FABIO.Expression))		#
	rdf.add((SITE[exp], FABIO.hasRepresentation, SITE[articolo]))	#
	rdf.add((SITE[articolo], RDF.type, FABIO.Item))			#
	
	rdf.add((DEO.Introduction, RDF.type, SKOS.Concept))
	rdf.add((DEO.Introduction, SKOS.prefLabel, Literal(rhetoric)))
	rdf.add((DEO.Introduction, SKOS.topConceptOf, DEOLESS.deo))
	
def creaAnnotComment(articolo, valore, start, end, commentSelection, creatorName, creatorMail):		#mettere aposto
	annotation = BNode()
	target = BNode()
	selector = BNode()
	comment = BNode()
	time = str(datetime.datetime.now())
	res = re.sub('.html', '',articolo)
	exp = res+"_ver1"
	sel = articolo+"#"+valore+"-"+start+"-"+end
	
	rdf.add((annotation, RDF.type, OA.Annotation))
	rdf.add((annotation, RDFS.label, Literal("Commento")))
	rdf.add((annotation, OA.hasTarget, target))
	rdf.add((target, RDF.type, OA.SpecificResource))
	rdf.add((target, OA.hasSource, SITE[articolo]))
	rdf.add((target, OA.hasSelector, selector))
	rdf.add((selector, RDF.type, OA.FragmentSelector))
	rdf.add((selector, RDF.value, Literal(valore)))
	rdf.add((selector, OA.start, Literal(start, datatype=XSD.nonNegativeInteger)))
	rdf.add((selector, OA.end, Literal(end, datatype=XSD.nonNegativeInteger)))
	rdf.add((annotation, OA.hasBody, comment))
	rdf.add((annotation, OA.annotatedBy, URIRef("mailto:"+creatorMail)))
	rdf.add((annotation, OA.annotatedAt, Literal(time)))
	rdf.add((comment, RDF.type, RDF.Statement))
	rdf.add((comment, RDF.subject, SITE[sel]))    #parametro?
	rdf.add((comment, RDF.predicate, SCHEMA.comment))
	rdf.add((comment, RDF.object, Literal(commentSelection, datatype=XSD.string)))
	#rdf.add((comment, RDFS.label, Literal("Commento")))
	rdf.add((URIRef("mailto:"+creatorMail), FOAF.name, Literal(creatorName)))
	rdf.add((URIRef("mailto:"+creatorMail), SCHEMA.mail, Literal(creatorMail)))
	
	rdf.add((SITE[res], RDF.type, FABIO.Work))		#
	rdf.add((SITE[res], FABIO.hasPortrayal, SITE[articolo])) #
	rdf.add((SITE[res], FRBR.realization, SITE[exp]))        #
	rdf.add((SITE[exp], RDF.type, FABIO.Expression))		#
	rdf.add((SITE[exp], FABIO.hasRepresentation, SITE[articolo]))	#
	rdf.add((SITE[articolo], RDF.type, FABIO.Item))			#
	
def creaAnnotCites(articolo, valore, start, end, citeSelection, creatorName, creatorMail):   #mettere aposto
	annotation = BNode()
	target = BNode()
	selector = BNode()
	cite = BNode() #variabile
	time = str(datetime.datetime.now())
	res = re.sub('.html', '',articolo)
	exp = res+"_ver1"
	sel = articolo+"#"+valore+"-"+start+"-"+end
	cit = exp+"_cited3"
	titolo = "titolo articolo" #parametro
	
	rdf.add((annotation, RDF.type, OA.Annotation))
	rdf.add((annotation, RDFS.label, Literal("Citazione")))
	rdf.add((annotation, OA.hasTarget, target))
	rdf.add((target, RDF.type, OA.SpecificResource))
	rdf.add((target, OA.hasSource, SITE[articolo]))
	rdf.add((target, OA.hasSelector, selector))
	rdf.add((selector, RDF.type, OA.FragmentSelector))
	rdf.add((selector, RDF.value, Literal(valore)))
	rdf.add((selector, OA.start, Literal(start, datatype=XSD.nonNegativeInteger)))
	rdf.add((selector, OA.end, Literal(end, datatype=XSD.nonNegativeInteger)))
	rdf.add((annotation, OA.hasBody, cite))
	rdf.add((annotation, OA.annotatedBy, URIRef("mailto:"+creatorMail)))
	rdf.add((annotation, OA.annotatedAt, Literal(time)))
	rdf.add((cite, RDF.type, RDF.Statement))
	rdf.add((cite, RDF.subject, SITE[exp]))    #parametro?
	rdf.add((cite, RDF.predicate, CITO.cites))
	rdf.add((cite, RDF.object, SITE[cit]))     #?
	rdf.add((cite, RDFS.label, Literal("questo articolo cita '"+titolo+"'")))
	rdf.add((URIRef("mailto:"+creatorMail), FOAF.name, Literal(creatorName)))
	rdf.add((URIRef("mailto:"+creatorMail), SCHEMA.mail, Literal(creatorMail)))
	rdf.add((SITE[cit], RDFS.label, Literal(citeSelection)))
	
	rdf.add((SITE[res], RDF.type, FABIO.Work))		#
	rdf.add((SITE[res], FABIO.hasPortrayal, SITE[articolo])) #
	rdf.add((SITE[res], FRBR.realization, SITE[exp]))        #
	rdf.add((SITE[exp], RDF.type, FABIO.Expression))		#
	rdf.add((SITE[exp], FABIO.hasRepresentation, SITE[articolo]))	#
	rdf.add((SITE[articolo], RDF.type, FABIO.Item))			#
	
	
#############################################################################################################################
for case in switch(tipo):
    if case('hasAuthor'):
        creaAnnotAutore(data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        break
    if case('hasPublicationYear'):
        creaAnnotDate(data[1], data[2], data[3], data[4], data[5], data[6], data[7])			#S: fabio:Expression P: fabio:hasPublicationYear O: xsd:date

        break
    if case('hasTitle'):
        creaAnnotTitle(data[1], data[2], data[3], data[4], data[5], data[6], data[7])				#S: fabio:Expression P: dcterms:title O: xsd:string

        break
    if case('hasDOI'): 
        creaAnnotDOI(data[1], data[2], data[3], data[4], data[5], data[6], data[7])			#S: fabio:Expression P: prism:doi O: xsd:string

        break
    if case('hasURL'):
        creaAnnotURL(data[1], data[2], data[3], data[4], data[5], data[6], data[7])			#S: fabio:Expression P: fabio:hasURL O: xsd:anyURL

        break
    if case('hasComment'):
        creaAnnotComment(data[1], data[2], data[3], data[4], data[5], data[6], data[7])		#S: frammento di fabio:Expression P: schema:comment O: xsd:string

        break
    if case('denotesRhetoric'):
        creaAnnotRhetoric(data[1], data[2], data[3], data[4], data[5], data[6], data[7])	#S: frammento di fabio:Expression P: sem:denotes O: skos:Concept

        break
    if case('cites'):
        creaAnnotCites(data[1], data[2], data[3], data[4], data[5], data[6], data[7])		#S: fabio:Expression P: cito:cites O: fabio:Expression

        break
    if case(): # default
        print "switch error"
        # No need to break here, it'll stop anyway




#print rdf.serialize(format="n3")
#rdf.serialize("graphAuthLocal.owl", format="pretty-xml")

#print rdf   #rdf nell'IOmemory
#print rdf.serialize()

# when done!
#rdf.close()

#update 
rdf.serialize("graphAuth.ttl")
print 
