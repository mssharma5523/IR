from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh import qparser


def search_BM25(input_query):
	with ix.searcher() as searcher:
	    query = QueryParser("Content", ix.schema,group=qparser.OrGroup).parse(input_query) ## here 'hsbc' is the search term
	    results = searcher.search(query)
	    for x in results:
	        print x['FileName']

def search_TFIDF(input_query):
	with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
	    query = QueryParser("Content", ix.schema).parse(input_query) ## here 'hsbc' is the search term
	    results = searcher.search(query)
	    for x in results:
	        print x['FileName']

def search_TF(input_query):
	with ix.searcher(weighting=scoring.Frequency()) as searcher:
	    query = QueryParser("Content", ix.schema).parse(input_query) ## here 'hsbc' is the search term
	    results = searcher.search(query)
	    for x in results:
	        print x['FileName']

#def parse_by_OR():

#def parse_by_AND():

#def parse_by_NOT():

#def parse_by_PHRASE():

if __name__ == "__main__":
	ix = open_dir('Indexes')
	global writer
	writer = ix.writer()

	
	input_query = raw_input("Enter search query : ")
	#parser = qparser.QueryParser("Content", schema=ix.schema,group=qparser.OrGroup)

	print input_query
	#input_query = parser.parse(u'%s'%input_query)
	#input_query = parser.parse(u"Welcome ")
	print input_query
	print "Results of BM25 query"
	search_BM25(input_query)
	print "Result of TF-IDF query"
	search_TFIDF(input_query)
	print "Result of Frequency query"
	search_TF(input_query)