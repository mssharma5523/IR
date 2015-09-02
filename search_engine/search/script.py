##indexing part

from whoosh.index import create_in
from whoosh.fields import *
import os
import stat
import time

schema = Schema(FileName=TEXT(stored=True), FilePath=TEXT(stored=True), Content=TEXT(stored=True), Size=TEXT(stored=True), LastModified=TEXT(stored=True),
                LastAccessed=TEXT(stored=True), CreationTime=TEXT(stored=True), Mode=TEXT(stored=True))

ix = create_in("./index", schema)
writer = ix.writer()



for top, dirs, files in os.walk('./0'):
    for nm in files:
        fileStats = os.stat(os.path.join(top, nm))
        content = ""
        with open(os.path.join(top,nm), 'r') as content_file:
            content = content_file.read()
        fileInfo = {
            'FileName':nm,
            'FilePath':os.path.join(top, nm),
            'Content' : content,
            'Size' : fileStats [ stat.ST_SIZE ],
            'LastModified' : time.ctime ( fileStats [ stat.ST_MTIME ] ),
            'LastAccessed' : time.ctime ( fileStats [ stat.ST_ATIME ] ),
            'CreationTime' : time.ctime ( fileStats [ stat.ST_CTIME ] ),
            'Mode' : fileStats [ stat.ST_MODE ]
        }
        try:
            writer.add_document(FileName=u'%s'%fileInfo['FileName'],FilePath=u'%s'%fileInfo['FilePath'],Content=u'%s'%fileInfo['Content'],Size=u'%s'%fileInfo['Size'],LastModified=u'%s'%fileInfo['LastModified'],LastAccessed=u'%s'%fileInfo['LastAccessed'],CreationTime=u'%s'%fileInfo['CreationTime'],Mode=u'%s'%fileInfo['Mode'])
        except:
            pass
writer.commit()


## now the seaching part
from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
    query = QueryParser("Content", ix.schema).parse(u"Westchester") ## here 'hsbc' is the search term
    results = searcher.search(query)
    for x in results:
        print x['FileName']
