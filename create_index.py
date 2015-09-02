#file for creating the indexing structure of the file

from whoosh.index import create_in
from whoosh.fields import *
import os
import stat
import time
#import cleanHtml

#The schema can be improved by storing the keywords (Title) which can enhance the search
def create_schema():    
    schema = Schema(FileName=TEXT(stored=True), FilePath=TEXT(stored=True), Content=TEXT(stored=True), Size=TEXT(stored=True), LastModified=TEXT(stored=True),
                    LastAccessed=TEXT(stored=True), CreationTime=TEXT(stored=True), Mode=TEXT(stored=True))

    ix = create_in("./Indexes", schema)
    global writer
    writer = ix.writer()

def create_index():
    for top, dirs, files in os.walk('./Dataset'):
        for nm in files:
            try:
                fileStats = os.stat(os.path.join(top, nm))
                content = ""
                with open(os.path.join(top,nm), 'r') as content_file:
                    content = content_file.read()
                #content = dehtml(content)
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
            except:
                pass
    writer.commit()

if __name__ == "__main__":
    create_schema()
    create_index()