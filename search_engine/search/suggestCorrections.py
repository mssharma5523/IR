from whoosh.index import open_dir

def suggestCorrections(input_query,query,directory):
    ix = open_dir(directory)
    writer = ix.writer()
    with ix.searcher() as searcher:
        corrected = searcher.correct_query(input_query, query)
        if corrected.query != input_query:
            print "Did you mean: " + corrected.string + '?'
        return
