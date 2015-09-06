'''
This file contains the functions relating to the AND,OR,NOT and phrasal queries.. It breaks these queries
into appropriate methods.. Please add code related to them only
'''

from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh import qparser


import os
from django.conf import settings

'''
 function for query parsing of AND type query.. the input is a query string and the output is the parsed query
'''

def query_AND(input_query,directory):
	# print directory
	ix = open_dir(directory)
	print 1
	writer = ix.writer()
	query = QueryParser("Content",ix.schema,group=qparser.AndGroup).parse(input_query)
	ix.close()
	return query

'''
	function for query parsing of OR
'''
def query_OR(input_query,directory):
	ix = open_dir(directory)
	writer = ix.writer()
	query = QueryParser("Content",ix.schema,group=qparser.OrGroup).parse(input_query)
	ix.close()
	return query

'''
	function of query parsing NOT
'''

def query_NOT(input_query,directory):
	ix = open_dir(directory)
	writer = ix.writer()
	query = QueryParser("Content",ix.schema,group=qparser.NotGroup).parse(input_query)
	ix.close()
	return query

'''
	function for phrasal-query
'''
def query_phrasal(input_query,directory):
    ix = open_dir(directory)
    writer = ix.writer()
    query = QueryParser("Content",ix.schema,group=qparser.AndGroup).parse("\"" + input_query + "\"")
    ix.close()
    return query
