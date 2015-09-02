from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext, loader

from .forms import search_form

from .search import search_BM25, search_TF, search_TFIDF,searchPhrasal
from .query import query_OR,query_AND,query_NOT
import time


# Create your views here.
def index(request):
	start_time = time.time()
	query = request.GET.get('query')
	qtype = request.GET.get('qtype')
	bm25 = request.GET.get('bm25')
	tf_idf = request.GET.get('tf_idf')
	tf = request.GET.get('tf')
	result_BM25 = []
	result_TFIDF = []
	result_TF = []
	if query:
		# result_BM25 = query_backend(query, qtype, 'BM25')
		for r in query_backend(query, qtype, 'BM25'):
			result_BM25.append({'title':r['Title'], 'fname':r['FileName'], 'content':r['Content'], 'rel_text':r['RelevantText']})
		for r in query_backend(query, qtype, 'TFIDF'):
			result_TFIDF.append({'title':r['Title'], 'fname':r['FileName'], 'content':r['Content'], 'rel_text':r['RelevantText']})
		for r in query_backend(query, qtype, 'TF'):
			result_TF.append({'title':r['Title'], 'fname':r['FileName'], 'content':r['Content'], 'rel_text':r['RelevantText']})
		# result_TFIDF = query_backend(query, qtype, 'TFIDF')
		# result_TF = query_backend(query, qtype, 'TF')

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
					'tf_pages': len(result_TF)
				}

	return render(request, 'search/index.html', context)


def staticpage(request, page):
	print page
	template = loader.get_template('Test/'+page)
	# return render(request, 'Test/'+page, {})
	return HttpResponse(template.render({}))






'''
The input is the query from the front end along with the type of query that he wants
returns list of objects.. qtype can be 'and', 'or','not','phrase'
searchtype can be 'BM25','TF','TFIDF'
'''
def query_backend(query,qtype,searchtype):
	if qtype == 'and':
		#this logic here
		input_query = query_AND(query)
		return search_result(input_query,query,searchtype)
	elif qtype == 'or':
		#this logic here
		input_query = query_OR(query)
		return search_result(input_query,query,searchtype)
	elif qtype == 'not':
		#logic
		input_query = query_NOT(query)
		return search_result(input_query,query,searchtype)
	elif qtype == 'phrase':
		return searchPhrasal(query)
		#logic

def search_result(input_query,query,searchtype):
	if searchtype == 'BM25':
		#logic
		return search_BM25(input_query,query)
	elif searchtype == 'TFIDF':
		#logic
		return search_TFIDF(input_query,query)
	elif searchtype == 'TF':
		#logic
		return search_TF(input_query,query)