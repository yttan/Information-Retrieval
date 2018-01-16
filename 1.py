import re

filePath = "As we may think.txt"

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

def computeWordFrequencies(tokenlist):
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


t_list = tokenize(filePath)
freq_map = computeWordFrequencies(t_list)
printFreq(freq_map)
