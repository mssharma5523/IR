from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext, loader

from .forms import search_form

from whoosh import scoring
from .search import search
from .query import query_OR,query_AND,query_NOT
import time

import os
from django.conf import settings


# Create your views here.
def index(request):
	start_time = time.time()
	query = request.GET.get('query')
	qtype = request.GET.get('qtype')
	bm25 = request.GET.get('bm25')
	tf_idf = request.GET.get('tf_idf')
	tf = request.GET.get('tf')
	stemming = request.GET.get('stemming')
	stopWords = request.GET.get('stop_words')
	result_BM25 = []
	result_TFIDF = []
	result_TF = []
	# directory = get_directory(stemming, stopWords)
	if query:
		# result_BM25 = query_backend(query, qtype, 'BM25')
		for r in query_backend(query, qtype, 'BM25',get_directory(stemming,stopWords)):
			result_BM25.append({'title':r['Title'], 'fname':r['FileName'], 'content':r['Content'], 'rel_text':r['RelevantText']})
		for r in query_backend(query, qtype, 'TFIDF',get_directory(stemming,stopWords)):
			result_TFIDF.append({'title':r['Title'], 'fname':r['FileName'], 'content':r['Content'], 'rel_text':r['RelevantText']})
		for r in query_backend(query, qtype, 'TF',get_directory(stemming,stopWords)):
			result_TF.append({'title':r['Title'], 'fname':r['FileName'], 'content':r['Content'], 'rel_text':r['RelevantText']})
		# result_TFIDF = query_backend(query, qtype, 'TFIDF')
		# result_TF = query_backend(query, qtype, 'TF')
	# print len(query_backend(query, qtype, 'BM25'))
	paginatorBM25 = Paginator(result_BM25, 10)
	paginatorTF_IDF = Paginator(result_TFIDF, 10)
	paginatorTF = Paginator(result_TF, 10)
	
	try:
		TF_IDF = paginatorTF_IDF.page(tf_idf)
	except PageNotAnInteger:
		TF_IDF = paginatorTF_IDF.page(1)
	except EmptyPage:
		TF_IDF = paginatorTF_IDF.page(paginatorTF_IDF.num_pages)

	try:
		BM25 = paginatorBM25.page(bm25)
	except PageNotAnInteger:
		BM25 = paginatorBM25.page(1)
	except EmptyPage:
		BM25 = paginatorBM25.page(paginatorBM25.num_pages)
		
	# for b in BM25:
	# 	print b['title']
	try:
		TF = paginatorTF.page(tf)
	except PageNotAnInteger:
		TF = paginatorTF.page(1)
	except EmptyPage:
		TF = paginatorTF.page(paginatorTF.num_pages)
	
	end_time = time.time()
	context = 	{
					'BM25': BM25,
					'TF': TF,
					'TF_IDF': TF_IDF, 
					'query':query, 
					'tf': tf, 
					'bm25': bm25, 
					'tf_idf':tf_idf, 
					'time': round(end_time - start_time, 3), 
					'bm_pages': len(result_BM25),
					'tfidf_pages': len(result_TFIDF),
					'tf_pages': len(result_TF),
					'stemming': stemming,
					'stop_words': stopWords,
					'qtype': qtype
				}
	if query != None:
		fp = open(os.path.join(settings.MEDIA_ROOT,'search/log/logfile'), 'a')
		fp1 = open(os.path.join(settings.MEDIA_ROOT,'search/log/latencylog'), 'a')
		line = "for query:\"" + query + "\", connected with:'" + qtype + "', time taken: " + str(round(end_time - start_time, 3)) + 'seconds \n'
		fp.write(line)
		line = str(round(end_time - start_time, 3)) + ',' + str(len(query)) + '\n'
		fp1.write(line)
		fp1.close()
		fp.close()

	return render(request, 'search/index.html', context)


def staticpage(request, page):
	print page
	# return render(request, 'Test/'+page, {})
	template = loader.get_template('Test/'+page)
	return HttpResponse(template.render({}))


def get_directory(stemming, stopWords):
	if stemming == 'off' and stopWords == 'off':
		directory = 'search/Indexes/withoutStopWords'
	elif stemming == 'off' and stopWords == 'on':
		directory = 'search/Indexes/stopWordsWithoutStemming'
	elif stemming == 'on' and stopWords == 'on':
		directory = 'search/Indexes/stopWordsWithStemming'
	else:
		directory = 'search/Indexes/withStemming'
	return directory



'''
The input is the query from the front end along with the type of query that he wants
returns list of objects.. qtype can be 'and', 'or','not','phrase'
searchtype can be 'BM25','TF','TFIDF'
'''
def query_backend(query,qtype,searchtype,directory):
	print os.path.join(settings.MEDIA_ROOT,directory)
	if qtype == 'and':
		#this logic here
		input_query = query_AND(query,os.path.join(settings.MEDIA_ROOT,directory))
		return search_result(input_query,query,searchtype, directory)
	elif qtype == 'or':
		#this logic here
		input_query = query_OR(query,os.path.join(settings.MEDIA_ROOT,directory))
		return search_result(input_query,query,searchtype, directory)
	elif qtype == 'not':
		#logic
		input_query = query_NOT(query,os.path.join(settings.MEDIA_ROOT,directory))
		return search_result(input_query,query,searchtype, directory)
	elif qtype == 'phrase':
		return searchPhrasal(query,os.path.join(settings.MEDIA_ROOT,directory))
		#logic

def search_result(input_query,query,searchtype,directory):
	if searchtype == 'BM25':
		#logic
		return search(input_query,query,os.path.join(settings.MEDIA_ROOT,directory),scoring.BM25F())
	elif searchtype == 'TFIDF':
		#logic
		return search(input_query,query,os.path.join(settings.MEDIA_ROOT,directory),scoring.TF_IDF())
	elif searchtype == 'TF':
		#logic
		return search(input_query,query,os.path.join(settings.MEDIA_ROOT,directory),scoring.Frequency())