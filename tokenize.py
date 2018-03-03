import re
def tokenize(filePath):
    myFile = open(filePath, "r")
    text = myFile.read()
    text = text.lower()
    text = re.sub(r'[-]', ' ', text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    words = text.split()
    myFile.close()
    return words

def tokenizequery(query):
    text = query.lower()
    text = re.sub(r'[-]', ' ', text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    words = text.split()
    return words

def computeWordFrequencies(tokenlist):
    freqMap = {}
    for token in tokenlist:
        if freqMap.has_key(token):
            freqMap[token] += 1
        else:
            freqMap[token] = 1
    return freqMap

def wordPositions(tokenlist):
    positionMap = {}
    N = len(tokenlist)
    for i in range(N):
        token = tokenlist[i]
        if positionMap.has_key(token):
            positionMap[token].append(i)
        else:
            positionMap[token] = [i]
    return positionMap

def tfposMap(tokenlist):
    tfposMap = {}
    N = len(tokenlist)
    for i in range(N):
        token = tokenlist[i]
        if tfposMap.has_key(token):
            tfposMap[token][0] += 1
            tfposMap[token][1].append(i)
        else:
            tfposMap[token] = []
            tfposMap[token].append(1)
            tfposMap[token].append([i])
    return tfposMap
