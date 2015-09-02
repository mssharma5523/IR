'''
This is the main function that will sync with the indexing , query parsing , search and other parts...
Other files should contain functions only and the input to them should be passed from this
'''

import os
from search import search_BM25, searchPhrasal,search_TFIDF,search_TF
from query import query_OR,query_AND
from util_functions import getRelevantText

if __name__ == "__main__":
	#ix = open_dir('Indexes')
	query = raw_input("Please Enter the query to search for:")
	input_query = query_AND(query)
	print "BM25 Results"
	result = search_BM25(input_query,query)
	for x in result:
		print 'Title : ' + x['Title']
		print 'Filename : ' + x['FileName']
		print 'Short description : ' + x['Content'][0:20] + '...'
		#relevant_text = getRelevantText(x['Content'],query.lower())
		#x['RelevantText'] = relevant_text
		print 'Relevant text : ' + x['RelevantText']
	print "Phrasal Query Results"
	#for x in result:
	#	print x['RelevantText']
	result = searchPhrasal(query)
	print result[0]['RelevantText']