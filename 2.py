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

list1 = tokenize(filePath1)
list2 = tokenize(filePath2)
print len(list1.intersection(list2))
