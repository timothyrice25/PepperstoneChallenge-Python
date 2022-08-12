from operator import truediv
from os.path import exists

class classChallengeProcessor:
    def __init__(self, dictionary, search):
        self.DictionaryFile = dictionary
        self.SearchFile = search
        self.DictionaryList = []
        self.SearchList = []
        self.CaseCount = []
        self.parseDictionaryFile()
        self.parseSearchFile()

    def process(self):
        self.parseDictionaryFile()
        self.parseSearchFile()
        self.processData()

    def parseDictionaryFile(self):
        self.DictionaryList = []
        f = open(self.DictionaryFile, "r")
        content = f.read()
        self.DictionaryList = content.split("\n")
        
    def parseSearchFile(self):
        self.SearchList = []
        f = open(self.SearchFile, "r")
        content = f.read()
        self.SearchList = content.split("\n")

        self.CaseCount.clear()
        for prob in self.SearchList:
            self.CaseCount.append(0)


    def processData(self):
        for k in range(0, len(self.SearchList)):
            for dictionary in self.DictionaryList:
                probabilityList = self.generateProbabilityList(dictionary)
                for prob in probabilityList:
                    found = False
                    if self.SearchList[k].count(prob) > 0:
                        self.CaseCount[k]+=1
                        found = True

                    if found:
                        break

    def generateProbabilityList(self, input):
        ret = []
        start = str(input[0])
        end = str(input[len(input) - 1])
        for i in range(1, len(input)-1):
            token = str(input[i])
            popindex = len(input) - 1
            others = input[:popindex] + input[popindex+1:]
            popindex = i
            others = others[:popindex] + others[popindex+1:]
            popindex = 0
            others = others[:popindex] + others[popindex+1:]

            word = start + token + others + end

            if ret.count(word) == 0:
                ret.append(word)

            for j in range(0, len(others)):
                popindex = len(others) - 1
                substr = others[:popindex] + others[popindex+1:]
                substr = others[len(others) - 1] + substr

                word = start + token + substr + end

                if ret.count(word) == 0:
                    ret.append(word)

        return ret

    def generateResults(self):
        ret = ""
        for i in range(0, len(self.CaseCount)):
            ret += "Case #" + str(i + 1) + ": " + str(self.CaseCount[i]) + "\r\n"

        return ret

    def checkDuplicateWordInDictionaryFile(self):
        lst = []
        for item in self.DictionaryList:
            if lst.count(item) == 0:
                lst.append(item)
            else:
                return item
        return ""

    def checkWordLengthInDictionaryFile(self):
        lst = []
        for item in self.DictionaryList:
            if (len(item) >= 105 or len(item) <= 2) and item != "":
                return item
                
        return ""

    def checkDictionaryFileLength(self):
        f = open(self.DictionaryFile, "r")
        content = f.read()
        content = content.replace("\r","")
        content = content.replace(" ","")
        if len(content) > 105:
            return False
        return True
        
dictionary = "Dictionary.txt"
search = "Input.txt"
processor = classChallengeProcessor(dictionary, search)

def analyze():
    if(isValidInputs()):
        processor.process()
        print(processor.generateResults())

def isValidInputs():
    if dictionary == "":
        print("Please browse for the directory file.")
        return False
    
    if search == "":
        print("Please browse for the search file.")
        return False

    if not exists(dictionary):
        print("Invalid Directory File")
        return False

    if not exists(search):
        print("Invalid Search File")
        return False

    msg = processor.checkDuplicateWordInDictionaryFile()
    if msg != "":
        print("Duplicate word found: " + msg)
        print("No two words in the dictionary should be the same.")
        return False

    msg = processor.checkWordLengthInDictionaryFile()
    if msg != "":
        if(len(msg)<=2):
            print("This word is too short: " + msg)
        elif (len(msg) >= 105):
            print("This word is too long: " + msg)
        print("Each word in the dictionary must be between 2 and 105 letters long.")
        return False

    if (not processor.checkDictionaryFileLength()):
        print("The sum of lengths of all words in the dictionary must not exceed 105.")
        return False

    return True

analyze()
