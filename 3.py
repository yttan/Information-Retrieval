import re

filePath1 = "As we may think.txt"
filePath2 = "As we may ink.txt"

def tokenize(filePath):
    index = set()
    myFile = open(filePath, "r")
    for line in myFile:
        temp = re.split('\W',line)
        for word in temp:
            if word is '':
                continue
            if word.lower() in index:
                continue
            else:
                index.add(word.lower())
    myFile.close()
    return index

def computeWordFrequencies(tokenlist,filePath):
    freqMap = {}
    myFile = open(filePath,"r")
    text = myFile.read()
    for token in tokenlist:
        pattern = re.compile(token,re.I)
        temp = re.findall(pattern,text)
        freqMap[token] = len(temp)

    myFile.close()
    return freqMap

def printFreq(Frequencies):
    for key, value in sorted (Frequencies.iteritems(), key = lambda (k,v):(v,k), reverse = True):
        print "%s : %s" % (key,value)


list1 = tokenize(filePath1)
list2 = tokenize(filePath2)

freq_map1 = computeWordFrequencies(list1,filePath1)
freq_map2 = computeWordFrequencies(list2,filePath2)

merge_map = freq_map1.copy()
merge_map.update(freq_map2)
printFreq(merge_map)
