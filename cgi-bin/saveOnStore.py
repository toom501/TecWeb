#!/usr/bin/python
# -*- coding: utf-8 -*-

import rdflib
import os
import shutil
from SPARQLWrapper import SPARQLWrapper, JSON


def load_graph(rdf_file_path):
    current_graph = rdflib.Graph()
    current_file_path = "tmp_rdf_file.rdf"
    shutil.copyfile(rdf_file_path, current_file_path)
    current_graph.load(current_file_path)
    os.remove(current_file_path)
    return current_graph


my_user = 'ltw1514'
my_pass = "7yhHHlc?"

g = load_graph("graphAuth.owl")

triplestore = "http://vitali.web.cs.unibo.it/raschietto/graph/ltw1514" #?user=%s&pass=%s" % (my_user, my_pass)
#triplestore = "http://localhost:3030/data/query"

query = """
PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

Insert Data 
{ 
  GRAPH <test> 
  { 
    rdf:r a "t"
  }
}
""" #% (triplestore, g.serialize(format="nt"))

sparql = SPARQLWrapper("http://localhost:3030/data/update", returnFormat='json') #?user=%s&pass=%s" % (my_user, my_pass)) # ci va link a server fuseki, molto probalile -> http://localhost:3030
sparql.setQuery(query)
sparql.setMethod('POST')
#q = sparql.query()

print sparql.query()
