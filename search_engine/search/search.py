'''
This file contains the search functions namely the TF-IDF,BM25 and TF and the optimisations related to them, if any.

'''
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh import qparser
from util_functions import getRelevantText
from whoosh.scoring import WeightingModel
from query import query_AND
import os
from django.conf import settings

'''
	function for searching on the basis of BM25..takes as the input parsed query and outputs the objects
'''
def search_BM25(input_query,query):
	ix = open_dir(os.path.join(settings.MEDIA_ROOT, 'search/Indexes'))
	writer = ix.writer()
	with ix.searcher() as searcher:
	    #query = QueryParser("Content", ix.schema,group=qparser.OrGroup).parse(input_query) ## here 'hsbc' is the search term
	    results = searcher.search(input_query)
	    response = []
	    for x in results:
	    	temp = {}
	        print x['FileName']
	        temp['FileName'] = x['FileName']
	        temp['Title'] = x['Title']
	        temp['Content'] = x['Content'][0:20]
	        temp['RelevantText'] = getRelevantText(x['Content'],query.lower())
	        response.append(temp)
	    ix.close()
	    return response

'''
	function for searching on the basis of TF-IDF..takes as the input parsed query and outputs the objects
'''
def search_TFIDF(input_query,query):
	ix = open_dir(os.path.join(settings.MEDIA_ROOT, 'search/Indexes'))
	writer = ix.writer()
	with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
	    #query = QueryParser("Content", ix.schema).parse(input_query) ## here 'hsbc' is the search term
	    results = searcher.search(input_query)
	    response = []
	    for x in results:
	    	temp = {}
	        print x['FileName']
	        temp['FileName'] = x['FileName']
	        temp['Title'] = x['Title']
	        temp['Content'] = x['Content'][0:20]
	        temp['RelevantText'] = getRelevantText(x['Content'],query.lower())
	        response.append(temp)
	    ix.close()
	    return response
'''
	function for searching on the basis of TF..takes as the input parsed query and outputs the objects
'''
def search_TF(input_query,query):
	ix = open_dir(os.path.join(settings.MEDIA_ROOT, 'search/Indexes'))
	writer = ix.writer()
	with ix.searcher(weighting=scoring.Frequency()) as searcher:
	    #query = QueryParser("Content", ix.schema).parse(input_query) ## here 'hsbc' is the search term
	    results = searcher.search(input_query)
	    response = []
	    for x in results:
	    	temp = {}
	        print x['FileName']
	        temp['FileName'] = x['FileName']
	        temp['Title'] = x['Title']
	        temp['Content'] = x['Content'][0:20]
	        temp['RelevantText'] = getRelevantText(x['Content'],query.lower())
	        response.append(temp)
	    ix.close()
	    return response
'''
	function for phrasal queries
'''
def searchPhrasal(query):
	ix = open_dir(os.path.join(settings.MEDIA_ROOT, 'search/Indexes'))
	input_query=query_AND("\"" + query + "\"")
	writer = ix.writer()
	with ix.searcher() as searcher:
	    #query = QueryParser("Content", ix.schema,group=qparser.OrGroup).parse(input_query) ## here 'hsbc' is the search term
	    results = searcher.search(input_query)
	    response = []
	    for x in results:
	    	temp = {}
	        print x['FileName']
	        temp['FileName'] = x['FileName']
	        temp['Title'] = x['Title']
	        temp['Content'] = x['Content'][0:20]
	        temp['RelevantText'] = getRelevantText(x['Content'],query.lower())
	        response.append(temp)
	    ix.close()
	    return response
