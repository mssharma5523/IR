'''
This file creates different types of indexing structures that are required... Please write code related to that only
'''

from whoosh.index import create_in
from whoosh.analysis import StandardAnalyzer,StopFilter,StemmingAnalyzer
from whoosh.fields import *
from whoosh.lang.porter import stem
import os
import stat
import time
import cleanHtml
from cleanHtml import *
import util_functions
from util_functions import *
import html2text



#The schema can be improved by storing the keywords (Title) which can enhance the search

def create_schema(directory):
    schema = Schema(FileName=TEXT(stored=True), FilePath=TEXT(stored=True), Title=TEXT(stored=True), Content=TEXT(stored=True), Size=TEXT(stored=True), LastModified=TEXT(stored=True), LastAccessed=TEXT(stored=True), CreationTime=TEXT(stored=True), Mode=TEXT(stored=True),text=TEXT(spelling=True))
    create_non_existent_directory(directory)
    ix = create_in(directory, schema)
    global writer
    writer = ix.writer()
    return

#creates the schema for indexing by stemming words
def create_schema_with_stemming(directory):
    analyzer = StemmingAnalyzer()
    schema = Schema(FileName=TEXT(stored=True), FilePath=TEXT(stored=True), Title=TEXT(stored=True), Content=TEXT(stored=True,analyzer=analyzer), Size=TEXT(stored=True), LastModified=TEXT(stored=True),
                    LastAccessed=TEXT(stored=True), CreationTime=TEXT(stored=True), Mode=TEXT(stored=True),  text=TEXT(spelling=True))
    create_non_existent_directory(directory)
    ix = create_in(directory, schema)
    global writer
    writer = ix.writer()
    return 
    
#includes stop words in the schema
def create_schema_with_stopwords(directory):
    schema = Schema(FileName=TEXT(stored=True), FilePath=TEXT(stored=True), Title=TEXT(stored=True), Content=TEXT(stored=True,analyzer=StandardAnalyzer(stoplist=None)), Size=TEXT(stored=True), LastModified=TEXT(stored=True),
                    LastAccessed=TEXT(stored=True), CreationTime=TEXT(stored=True), Mode=TEXT(stored=True), text=TEXT(spelling=True))
    create_non_existent_directory(directory)
    ix = create_in(directory, schema)
    global writer
    writer = ix.writer()
    return
    
#schema with stop words along with stemming
def create_schema_with_stemming_with_stopwords(directory):
    analyzer = StemmingAnalyzer(stoplist=None)
    schema = Schema(FileName=TEXT(stored=True), FilePath=TEXT(stored=True), Title=TEXT(stored=True), Content=TEXT(stored=True,analyzer=analyzer), Size=TEXT(stored=True), LastModified=TEXT(stored=True),
                    LastAccessed=TEXT(stored=True), CreationTime=TEXT(stored=True), Mode=TEXT(stored=True),  text=TEXT(spelling=True))
    create_non_existent_directory(directory)
    ix = create_in(directory, schema)
    global writer
    writer = ix.writer()
    return

def create_non_existent_directory(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
    return
    
def create_index():
    for top, dirs, files in os.walk('./templates/Test'):
        for nm in files:
            try:
                fileStats = os.stat(os.path.join(top, nm))
                content = ""
                with open(os.path.join(top,nm), 'r') as content_file:
                    content = content_file.read()
                title = getTitle(content)
                # content = dehtml(content)
                content = html2text.html2text(content)
                fileInfo = {
                    'FileName':nm,
                    'FilePath':os.path.join(top, nm),
                    'Title': title,
                    'Content' : content,
                    'Size' : fileStats [ stat.ST_SIZE ],
                    'LastModified' : time.ctime ( fileStats [ stat.ST_MTIME ] ),
                    'LastAccessed' : time.ctime ( fileStats [ stat.ST_ATIME ] ),
                    'CreationTime' : time.ctime ( fileStats [ stat.ST_CTIME ] ),
                    'Mode' : fileStats [ stat.ST_MODE ]
                }
                try:
                    writer.add_document(FileName=u'%s'%fileInfo['FileName'],FilePath=u'%s'%fileInfo['FilePath'],Title=u'%s'%fileInfo['Title'],Content=u'%s'%fileInfo['Content'],Size=u'%s'%fileInfo['Size'],LastModified=u'%s'%fileInfo['LastModified'],LastAccessed=u'%s'%fileInfo['LastAccessed'],CreationTime=u'%s'%fileInfo['CreationTime'],Mode=u'%s'%fileInfo['Mode'])
                except:
                    pass
            except:
                pass
    writer.commit()
    return

if __name__ == "__main__":
    create_non_existent_directory('./Indexes')
    #create_schema('./Indexes/withoutStopWords')
    #create_schema_with_stopwords('./Indexes/stopWordsWithoutStemming')
    create_schema_with_stemming('./Indexes/withStemming')
    # create_schema_with_stemming_with_stopwords('./Indexes/stopWordsWithStemming')
    create_index()
