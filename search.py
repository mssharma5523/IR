'''
This file contains the search functions namely the TF-IDF,BM25 and TF and the optimisations related to them, if any.

'''
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh import qparser
from util_functions import getRelevantText
from whoosh.scoring import WeightingModel
from query import query_AND

'''
	function for searching; takes the input parsed query, queryString and WeightingModel and outputs the objects
'''
def search(input_query,query,weighting):
	ix = open_dir('Indexes')
	writer = ix.writer()
	with ix.searcher(weighting=weighting) as searcher:
	    #query = QueryParser("Content", ix.schema,group=qparser.OrGroup).parse(input_query) ## here 'hsbc' is the search term
	    results = searcher.search(input_query)
	    response = []
	    for x in results:
	    	temp = {}
	        temp['FileName'] = x['FileName']
	        temp['Title'] = x['Title']
	        temp['Content'] = x['Content'][0:20]
	        temp['RelevantText'] = getRelevantText(x['Content'],query.lower())
	        response.append(temp)
	    ix.close()
	    return response
