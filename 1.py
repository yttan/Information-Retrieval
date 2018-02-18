import re

filePath = "test1.txt"

def tokenize(filePath):
    myFile = open(filePath, "r")
    text = myFile.read()
    text = text.lower()
    text = re.sub(r'[-]', ' ', text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    words = text.split()
    myFile.close()
    return words

def computeWordFrequencies(tokenlist):
    freqMap = {}
    for token in tokenlist:
        if freqMap.has_key(token):
            freqMap[token] += 1
        else:
            freqMap[token] = 1
    return freqMap

def Print(Frequencies):
    for key, value in sorted (Frequencies.iteritems(), key = lambda (k,v):(v,k), reverse = True):
        print "%s, %s" % (key,value)


t_list = tokenize(filePath)
freq_map = computeWordFrequencies(t_list)
Print(freq_map)
