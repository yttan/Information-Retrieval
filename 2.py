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

def cleanData(tokenlist):
    tokens = set()
    for token in tokenlist:
        if token in tokens:
            continue
        else:
            tokens.add(token)
    return tokens

list1 = tokenize(filePath1)
list2 = tokenize(filePath2)
set1 = cleanData(list1)
set2 = cleanData(list2)
print len(set1.intersection(set2))
