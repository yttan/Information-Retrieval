
from googlesearch import search
import json
import math
import tokenize

dirname = "WEBPAGES_CLEAN/"
f = open(dirname + "bookkeeping.json")
fstr = f.read()
bookkeeping = json.loads(fstr)
f.close()

with open('InvertedIndex.json') as json_file:
    data = json.load(json_file)

def DocId(url):
    global bookkeeping
    res = dict((v,k) for k,v in bookkeeping.iteritems())
    if url in res:
        return res[url]
    else:
        return None

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

def getPageScore(url,query):
    docid = DocId(url)
    score = 0
    if docid is not None:
        pages = getScore(query)
        if docid in pages:
            score += pages[docid]
    return score


def calDCG(scores):
    size = len(scores)
    DCG = [scores[0]]
    for i in range(2,1+size):
        temp = scores[i-1]/math.log(i,2)
        temp += DCG[-1]
        DCG.append(temp)
    return DCG

def calNDCG(scores):
    size = len(scores)
    actual = calDCG(scores)
    ideal = calDCG(sorted(scores,reverse =True))
    NDCG = []
    try:
        for i in range(size):
            NDCG.append(actual[i]/ideal[i])
    except:
        print "error when calaulate NDCG"
        print "actual DCG  " + str(actual)
        print "ideal DCG " + str(ideal)
    return NDCG


def getNDCG(query):
    urls = []
    domain = "  site:ics.uci.edu"
    q = query + domain
    for j in search(q, lang='en',num=5,start = 0,stop = 1,pause=2.0):
        if j.endswith("/"):
            j = j[:-1]
        if ("http://" in j ):
            urls.append(j.split("http://")[1])
        elif("https://" in j):
            urls.append(j.split("https://")[1])
        else:
            urls.append(j)
    scores = []
    for i in range(5):
        scores.append(getPageScore(urls[i],query))
    return calNDCG(scores)

def main():
    queries = ["mondego","machine learning","software engineering","security","student affairs","graduate courses","Crista Lopes","REST","computer games","information retrieval"]
    for query in queries:
        print "NDCG@5 for "+query+" is: "
        print getNDCG(query)

if __name__ == '__main__':
    main()
