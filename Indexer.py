
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
    for filename in rawIndex:
        for term, tfposlist in rawIndex[filename].iteritems():
            if InvertedIndex.has_key(term):
                itf = math.log10(tfposlist[0] + 1)
                InvertedIndex[term].append({"document": filename, "tf": tfposlist[0], "tf-idf": itf * idfMap[term], "position":tfposlist[1]})
            else:
                itf = math.log10(tfposlist[0] + 1)
                InvertedIndex[term] = [{"document": filename, "tf": tfposlist[0], "tf-idf": itf * idfMap[term], "position":tfposlist[1]}]
    return InvertedIndex



def Indexer():
    dirname = "WEBPAGES_TEST/"
    f = open(dirname + "bookkeeping.json").read()
    bookkeeping = json.loads(f)
    rawIndex = {}
    for filename in bookkeeping:
        tokens = tokenize.tokenize(dirname + filename)
        rawIndex[filename] = tokenize.tfposMap(tokens)
    return invertedIndex(rawIndex)


print Indexer()
# rawIndex = {}
# tokens = tokenize.tokenize("test1.txt")
# rawIndex["test1.txt"] = tokenize.tfposMap(tokens)
# tokens = tokenize.tokenize("test2.txt")
# rawIndex["test2.txt"] = tokenize.tfposMap(tokens)
# tokens = tokenize.tokenize("test3.txt")
# rawIndex["test3.txt"] = tokenize.tfposMap(tokens)
# myindex = invertedIndex(rawIndex)
# for k in myindex:
#     print k
#     print myindex[k]
#
