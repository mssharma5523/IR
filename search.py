'''
This file contains the search functions namely the TF-IDF,BM25 and TF and the optimisations related to them, if any.

'''
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh import qparser


'''
	function for searching on the basis of BM25..takes as the input parsed query and outputs the objects
'''
def search_BM25(input_query):
	ix = open_dir('Indexes')
	writer = ix.writer()
	with ix.searcher() as searcher:
	    #query = QueryParser("Content", ix.schema,group=qparser.OrGroup).parse(input_query) ## here 'hsbc' is the search term
	    results = searcher.search(input_query)
	    for x in results:
	        print x['FileName']
	    ix.close()
	    return results

'''
	function for searching on the basis of TF-IDF..takes as the input parsed query and outputs the objects
'''
def search_TFIDF(input_query):
	ix = open_dir('Indexes')
	writer = ix.writer()
	with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
	    #query = QueryParser("Content", ix.schema).parse(input_query) ## here 'hsbc' is the search term
	    results = searcher.search(input_query)
	    for x in results:
	        print x['FileName']
	    ix.close()
	    return results

'''
	function for searching on the basis of TF..takes as the input parsed query and outputs the objects
'''
def search_TF(input_query):
	ix = open_dir('Indexes')
	writer = ix.writer()
	with ix.searcher(weighting=scoring.Frequency()) as searcher:
	    #query = QueryParser("Content", ix.schema).parse(input_query) ## here 'hsbc' is the search term
	    results = searcher.search(query)
	    for x in results:
	        print x['FileName']
	    ix.close()
	    return results

'''
	function for phrasal queries
'''
def searchPhrasal(input_query):
	ix = open_dir('Indexes')
	writer = ix.writer()
	with ix.searcher() as searcher:
	    #query = QueryParser("Content", ix.schema,group=qparser.OrGroup).parse(input_query) ## here 'hsbc' is the search term
	    results = searcher.search(input_query)
	    for x in results:
	        print x['FileName']
	    ix.close()
	    return results
