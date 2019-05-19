from xml.etree import ElementTree as ET
from pyaspell import pyaspell
import time
import bisect

def sentyment(element):
    predict = 'Nieznany'
    if (' 0' in element):
        predict =  'neutralny'
    elif (' - s ' in element):
        predict = 'negatywny'
    elif (' - m ' in element):
        predict = 'bardzo negatywny'
    elif (' + s ' in element):
        predict = 'pozytywny'
    elif (' + m ' in element):
        predict = 'bardzo pozytywny'

    return predict

def makeWordSentimentSet():
    veryNegativeFile = open('veryNegative.txt','w', encoding='utf-8') 
    NegativeFile = open('Negative.txt','w', encoding='utf-8') 
    NeutralFile = open('Neutral.txt','w', encoding='utf-8') 
    PositiveFile = open('Positive.txt','w', encoding='utf-8') 
    veryPositiveFile = open('veryPositive.txt','w', encoding='utf-8') 
    
    vNCounter = 0
    NCounter = 0
    NeutralCounter = 0
    PCounter = 0
    vPCounter = 0
   
    parser = ET.iterparse(filename)
    elementy = []
    
    for event, element in parser:
    
        if 'desc' in element.attrib:
            if ('##A' in element.attrib['desc']):
                a1 = ''
                a2 = ''
                p1 = []
                p2 = []
                p2Flag = False
    
           
                tmp =  element.attrib['desc'].split('##A1:')
                if (len(tmp) > 1):
                    a1 = tmp[1]
            
                    if ('##A2' in tmp[1]):
                        tmp = tmp[1].split('##A2:')
                        a1 = tmp[0]
                        if(len(tmp)>1): 
                            a2 = tmp[1]
                            p2Flag = True
    
                        #wycinamy przypadki uzycia:
                        p1 = a1.split('[')
                        if(p2Flag == True): 
                            p2 = a2.split('[')
    
                    print("SŁOWO: " + element.attrib['name'])
                    print('\tA1: ' + sentyment(a1))
            
                    if(sentyment(a1) == 'bardzo negatywny'):
                        if(element.attrib['name'] not in veryNegativeSet):
                            
                            veryNegativeFile.write(element.attrib['name'] + '\n')
                            vNCounter += 1
    
                    elif(sentyment(a1) == 'negatywny'):
                        if(element.attrib['name'] not in negativeSet):
                            negativeSet.add(element.attrib['name'])
                            NegativeFile.write(element.attrib['name'] + '\n')
                            NCounter += 1
    
                    elif(sentyment(a1) == 'neutralny'):
                        if(element.attrib['name'] not in neutralSet):
                            neutralSet.add(element.attrib['name'])
                            NeutralFile.write(element.attrib['name'] + '\n')
                            NeutralCounter += 1
    
                    elif(sentyment(a1) == 'pozytywny'):
                        if(element.attrib['name'] not in positiveSet):
                            positiveSet.add(element.attrib['name'])
                            PositiveFile.write(element.attrib['name'] + '\n')
                            PCounter += 1
    
                    elif(sentyment(a1) == 'bardzo pozytywny'):
                        if(element.attrib['name'] not in veryPositiveSet):
                            veryPositiveSet.add(element.attrib['name'])
                            veryPositiveFile.write(element.attrib['name'] + '\n')
                            vPCounter += 1
    
    
                    if (a2 != ''):
                        print('\tA2: ' + sentyment(a2))
                        if (len(p1) > 1):
                            print('\tPrzypadki użycia:')
                            for i in range(1,len(p1)):
                                print ('\t\t' + p1[i])
                            if(p2Flag == True): 
                                for i in range(1,len(p2)):
                                    print ('\t\t' + p2[i])
            
                print('b.neg \t\tneg \t\tneu \t\tpos \t\tb.pos')
                print(str(vNCounter) + "\t\t" + str(NCounter) + "\t\t" + str(NeutralCounter) + "\t\t" + str(PCounter) + "\t\t" + str(vPCounter))
            #print(element.attrib)
                elementy.append(element)
    
        element.clear()
    return element, elementy, event, NCounter, NegativeFile, NeutralCounter, NeutralFile, parser, PCounter, PositiveFile, veryNegativeFile, veryPositiveFile, vNCounter, vPCounter

def loadWordSet():
    VNSet = set(line.strip() for line in open('veryNegative.txt', encoding='utf-8'))
    NSet = set(line.strip() for line in open('Negative.txt', encoding='utf-8'))
    NeSet = set(line.strip() for line in open('Neutral.txt', encoding='utf-8'))
    PSet = set(line.strip() for line in open('Positive.txt', encoding='utf-8'))
    VPSet = set(line.strip() for line in open('veryPositive.txt', encoding='utf-8'))
    return VNSet, NSet, NeSet, PSet, VPSet

def loadTweets(file):
    with file as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content] 
    return content

def morf(word):

    if(any(word in x for x in morfSlownik)):
        index = findItem(morfSlownik, word)
        ind = (index[0][0])
        return morfSlownik[ind][0]
    else:
        return word

def morf2(word):

    if word in morfSlownik:
        return morfSlownik[word]
    else:
        return word
    
def findItem(list, item):
    return[(ind, list[ind].index(item)) for ind in range(len(list)) if item in list[ind]]

def checkSentiments(sentence):
    value = 0
    wordCounter = 0
    for word in sentence.split():
        wordCounter += 1
        morfword = morf2(word.lower())

        if (morfword in veryNegativeSet):
            value -= 2
        elif (morfword in negativeSet):
            value -= 1
        elif (morfword in positiveSet):
            value += 1
        elif (morfword in veryPositiveSet):
            value += 2
        else: 
            value += 0
    return (value)

t0 = time.time()

filename = 'plwordnet-3.0.xml'

veryNegativeSet = set()
negativeSet = set()
neutralSet = set()
positiveSet = set()
veryPositiveSet = set()

#element, elementy, event, NCounter, NegativeFile, NeutralCounter, NeutralFile, parser, PCounter, PositiveFile, veryNegativeFile, veryPositiveFile, vNCounter, vPCounter = makeWordSentimentSet()

veryNegativeSet, negativeSet, neutralSet, positiveSet, veryPositiveSet = loadWordSet()
print("[] ZAŁADOWANO ZBIORY SŁóW")

negativeTweetsFile = open('tweets2/negative.txt','r') 
neutralTweetsFile = open('tweets2/neutral.txt','r') 
positiveTweetsFile = open('tweets2/positive.txt','r') 

negativeTweets = loadTweets(negativeTweetsFile)
neutralTweets = loadTweets(neutralTweetsFile)
positiveTweets = loadTweets(positiveTweetsFile)


print("[] ZAŁADOWANO TWEETY")

morfSlownikFile = open('odm.txt', 'r', encoding='utf-8')
morfSlownik = {}
with morfSlownikFile as inputfile:
    morfSlownikTmp = []
    for line in inputfile:
        morfSlownikTmp.append(line.strip().split(', '))
    for wordsTmp  in morfSlownikTmp:
        if (len(wordsTmp) > 1):
            morfSlownik[wordsTmp[0]] = wordsTmp[0]
            for w in range(1,len(wordsTmp)):
                morfSlownik[wordsTmp[w]] = wordsTmp[0]
        else:
            morfSlownik[wordsTmp[0]] = wordsTmp[0]



print("[] ZAŁADOWANO SŁOWNIK ODMIAN")

print(morf2('zrobiłem'))

all = 0
goodCount = 0
badCount = 0


for x in negativeTweets:
    all += 1
    sen = checkSentiments(x)
    if (sen < -1):
        goodCount += 1
    else:
        badCount += 1

    print('WSZYSTKICH ZBADANYCH: ' + str(all) + '\tPOPRAWNYCH: ' + str(goodCount) + '\tNIEPOPRAWNYCH:' + str(badCount))

for x in neutralTweets:
    all += 1
    sen = checkSentiments(x)
    if (sen < 1 and sen > -1):
        goodCount += 1
    else:
        badCount += 1

    print('WSZYSTKICH ZBADANYCH: ' + str(all) + '\tPOPRAWNYCH: ' + str(goodCount) + '\tNIEPOPRAWNYCH:' + str(badCount))

for x in positiveTweets:
    all += 1
    sen = checkSentiments(x)
    if (sen > 1):
        goodCount += 1
    else:
        badCount += 1

    print('WSZYSTKICH ZBADANYCH: ' + str(all) + '\tPOPRAWNYCH: ' + str(goodCount) + '\tNIEPOPRAWNYCH:' + str(badCount))


t1 = time.time()

print('Time: ' + str(t1 -t0))

#5 słowników ze słowami z etykietami
#TODO:
#2. zamiana na bezokoliczniki
#3. próba sprawdzenia wydzwięku ze słownikami
