import re

filePath1 = "test1.txt"
filePath2 = "test2.txt"

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
        print "%s : %s" % (key,value)



list1 = tokenize(filePath1)
list2 = tokenize(filePath2)

freq_map1 = computeWordFrequencies(list1)
freq_map2 = computeWordFrequencies(list2)

if len(freq_map1) >= len(freq_map2):
    smallmap = freq_map2
    resultmap = freq_map1
else:
    smallmap = freq_map1
    resultmap = freq_map2

for k,v in smallmap.items():
    if k in resultmap:
        resultmap[k] = resultmap[k] + smallmap [k]
    else:
        resultmap[k] = smallmap[k]

Print(resultmap)
