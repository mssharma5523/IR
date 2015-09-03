from util_functions import getRelevantText

def printResult(result,query):
    for x in result:
		print 'Title : ' + x['Title']
		print 'Filename : ' + x['FileName']
		print 'Short description : ' + x['Content'][0:20] + '...'
		relevant_text = getRelevantText(x['Content'],query.lower())
		print 'Relevant text : ' + relevant_text + '\n'
    return
