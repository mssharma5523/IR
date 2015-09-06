'''
This is the main function that will sync with the indexing , query parsing , search and other parts...
Other files should contain functions only and the input to them should be passed from this
'''

import os
from whoosh import scoring
from search import search
from query import query_OR,query_AND, query_phrasal
from suggestCorrections import suggestCorrections
from printResult import printResult

if __name__ == "__main__":
	#ix = open_dir('Indexes')
	query = raw_input("Please Enter the query to search for:")
	input_query = query_AND(query,'./Indexes/stopWordsWithoutStemming')
	suggestCorrections(input_query,query,'./Indexes/stopWordsWithoutStemming')

	print "BM25 Results"
	result = search(input_query,query,'./Indexes/stopWordsWithoutStemming',scoring.BM25F())
	printResult(result,query)

	print "Phrasal Query Results"
	result = search(query_phrasal(query,'./Indexes/stopWordsWithoutStemming'),query,'./Indexes/stopWordsWithoutStemming',scoring.BM25F())
	printResult(result,query)

	print "TF_IDF Results"
	result = search(input_query,query,'./Indexes/stopWordsWithoutStemming',scoring.TF_IDF())
	printResult(result,query)

	print "TF Results"
	result = search(input_query,query,'./Indexes/stopWordsWithoutStemming',scoring.Frequency())
	printResult(result,query)
