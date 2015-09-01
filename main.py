'''
This is the main function that will sync with the indexing , query parsing , search and other parts...
Other files should contain functions only and the input to them should be passed from this
'''

import os
from search import search_BM25
from query import query_OR,query_AND

if __name__ == "__main__":
	#ix = open_dir('Indexes')
	query = raw_input("Please Enter the query to search for:")
	input_query = query_AND(query)
	print "BM25 results"
	result = search_BM25(input_query)