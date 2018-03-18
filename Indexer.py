
import tokenize as tokenize
import json
import math



def calculateDF(Index):
    dfMap = {}
    for filename in Index:
        for term in Index[filename]:
            if dfMap.has_key(term):
                dfMap[term] += 1
            else:
                dfMap[term] = 1
    return dfMap


def invertedIndex(rawIndex):
    dfMap = calculateDF(rawIndex)
    N = len(rawIndex)
    idfMap = {}
    for term in dfMap:
        idfMap[term] = math.log10( float(N) / dfMap[term])
    InvertedIndex = {}
    with open('idfMap.json', 'w') as outfile:
        json.dump(idfMap, outfile)
    for filename in rawIndex:
        for term, tfposlist in rawIndex[filename].iteritems():
            if InvertedIndex.has_key(term):
                itf = math.log10(tfposlist[0] + 1)
                InvertedIndex[term].append({"doc": filename, "tf-idf": itf * idfMap[term], "pos":tfposlist[1]})
            else:
                itf = math.log10(tfposlist[0] + 1)
                InvertedIndex[term] = [{"doc": filename, "tf-idf": itf * idfMap[term], "pos":tfposlist[1]}]
    return InvertedIndex

def unique(inverted):
    unique = 0
    for term in inverted:
        if len(inverted[term]) == 1 :
            unique += 1
    print unique

def Index():
    dirname = "WEBPAGES_CLEAN/"
    f = open(dirname + "bookkeeping.json")
    fstr = f.read()
    bookkeeping = json.loads(fstr)
    rawIndex = {}
    for filename in bookkeeping:
        tokens = tokenize.tokenize(dirname + filename)
        rawIndex[filename] = tokenize.tfposMap(tokens)
    f.close()
    inverted =  invertedIndex(rawIndex)
    unique(inverted)
    with open('InvertedIndex.json', 'w') as outfile:
        json.dump(inverted, outfile)
    return inverted


if __name__ == '__main__':
    Index()
