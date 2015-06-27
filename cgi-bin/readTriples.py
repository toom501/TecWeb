#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import sys
from SPARQLWrapper import SPARQLWrapper
import rdflib


sparql = SPARQLWrapper("http://localhost:3030/ds/query", returnFormat="json")

#rdf = rdflib.Graph()
#rdf.load("graphScraping.owl")
#result = rdf.query("""
sparql.setQuery("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>


SELECT  ?end ?start ?id ?predicate ?mail ?name
WHERE {
  ?b0 <http://www.w3.org/ns/oa#hasTarget> ?b1;
    <http://www.w3.org/ns/oa#hasBody> ?b2;
    <http://www.w3.org/ns/oa#annotatedBy> ?user.
    
  ?b1 <http://www.w3.org/ns/oa#hasSource> ?art;
  	<http://www.w3.org/ns/oa#hasSelector> ?b3.

   ?b3 <http://www.w3.org/ns/oa#end> ?end;
    <http://www.w3.org/ns/oa#start> ?start;
    rdf:value ?id.
  ?b2 rdf:predicate ?predicate.
  
  ?user <http://schema.org/mail> ?mail;
    <http://xmlns.com/foaf/0.1/name> ?name.
  
}

""")

# ritorno un json contenente la query 

print "Content-Type: application/json\n\n"
json.dump(sparql.query().convert(), sys.stdout, indent=2)

	
