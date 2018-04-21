import tokenize
import json
import math
import sys

with open('InvertedIndex.json') as json_file:
    data = json.load(json_file)

dirname = "WEBPAGES_TEST/"
f = open(dirname + "bookkeeping.json")
fstr = f.read()
bookkeeping = json.loads(fstr)
f.close()
# read from inverted index and return scores of a query
def getScore(query):
    global data
    words = tokenize.tokenizequery(query)
    pages = {}
    for word in words:
        try:
            postings = data[word]
            for posting in postings:
                if pages.has_key(posting["doc"]):
                    pages[posting["doc"]] += posting["tf-idf"]
                else:
                    pages[posting["doc"]] = posting["tf-idf"]
        except:
            print "term "+ word + " is not in index"
    return pages

# get the URLs of the pages
def PageLink(key):
    global bookkeeping
    page = bookkeeping[key]
    return page

# return the top 5 pages
def search(query):
    results = getScore(query)
    i = 0
    limit = 5
    for key, value in sorted (results.iteritems(), key = lambda (k,v):(v,k), reverse = True):
        if i< limit:
            print PageLink(key)
            i+=1
        else:
            break

def main(argv):
    if len(argv) >= 1:
        query = " ".join(argv)
        search(query)
    else:
        print "no query"
if __name__ == '__main__':
    main(sys.argv[1:])
