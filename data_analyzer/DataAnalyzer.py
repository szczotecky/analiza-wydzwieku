import json
from pprint import pprint

data = json.load(open('2018_02_05_dumpdata.json'))

FvNeg = open('vNegative.txt','w') 
Fneg = open('negative.txt','w') 
Fneu = open('neutral.txt','w') 
Fpos = open('positive.txt','w') 
FvPos = open('vPositive.txt','w') 

print("FILE SUCCESFULLY LOADED")
#pprint(data[9855]['fields'])

questions = 0

bNegatywne = 0
negatywne = 0
neutralne = 0
pozytywne = 0
bPozytywne = 0

allVotes = 0

vNegPK = []
negPK = []
neuPK = []
posPK = []
vPosPK = []

Pk = 0
max = 0
# 1 - bardzo negatywne -> 5 - bardzo pozytywne
sentimentIndex = 0
questionIndex = 0
lastQuestionIndex = 0

#zliczanie głosów oraz wybór opcji z najwiekszą liczbą głosów.
for i, el in enumerate(data):
    if (el['model'] == 'polls.question'):
        questions += 1

    if (el['model'] == 'polls.choice'):
        allVotes += el['fields']['votes']

        if (questionIndex != el['fields']['question']):

            if (sentimentIndex == 1):
                bNegatywne += 1
                vNegPK.append(data[Pk]['fields']['question'])
            elif (sentimentIndex == 2):
                negatywne += 1
                negPK.append(data[Pk]['fields']['question'])
            elif (sentimentIndex == 3):
                neutralne += 1
                neuPK.append(data[Pk]['fields']['question'])
            elif (sentimentIndex == 4):
                pozytywne += 1
                posPK.append(data[Pk]['fields']['question'])
            elif (sentimentIndex == 5):
                bPozytywne += 1
                vPosPK.append(data[Pk]['fields']['question'])

            questionIndex = el['fields']['question']
            max = 0
            sentimentIndex = 0

        if (el['fields']['answer_text'] == 'bardzo negatywne' and el['fields']['votes'] != 0 ):
            if (el['fields']['votes'] > max):
                max = el['fields']['votes']
                Pk = i
                sentimentIndex = 1

        elif (el['fields']['answer_text'] == 'negatywne' and el['fields']['votes'] != 0 ):
            if (el['fields']['votes'] > max):
                max = el['fields']['votes']
                Pk = i
                sentimentIndex = 2

        elif (el['fields']['answer_text'] == 'neutralne' and el['fields']['votes'] != 0 ):
            if (el['fields']['votes'] > max):
                max = el['fields']['votes']
                Pk = i
                sentimentIndex = 3

        elif (el['fields']['answer_text'] == 'pozytywne' and el['fields']['votes'] != 0 ):
            if (el['fields']['votes'] > max):
                max = el['fields']['votes']
                Pk = i
                sentimentIndex = 4

        elif (el['fields']['answer_text'] == 'bardzo pozytywne' and el['fields']['votes'] != 0 ):
            if (el['fields']['votes'] > max):
                max = el['fields']['votes']
                Pk = i
                sentimentIndex = 5

#wpisywanie do odpowiednich plików wpisów wg ich kategorii
for el in data:
    if (el['model'] == 'polls.question'):
        if (el['pk'] in vNegPK):
            FvNeg.write(el['fields']['question_text'])
        elif (el['pk'] in negPK):
            Fneg.write(el['fields']['question_text'])
        elif (el['pk'] in neuPK):
            Fneu.write(el['fields']['question_text'])
        elif (el['pk'] in posPK):
            Fpos.write(el['fields']['question_text'])
        elif (el['pk'] in vPosPK):
            FvPos.write(el['fields']['question_text'])

print(allVotes)
print(questions)

F = open('results.txt','w') 

F.write('bardzo negatywne\twszystkich: ' + str(questions) + '\t0 głosów: ' + str(questions-bNegatywne) + '\toddanych głosów: ' + str(bNegatywne) + '\n')
F.write('negatywne\twszystkich: ' + str(questions) + '\t0 głosów: ' + str(questions-negatywne) + '\toddanych głosów: ' + str(negatywne) + '\n')
F.write('neutralne\twszystkich: ' + str(questions) + '\t0 głosów: ' + str(questions-neutralne) + '\toddanych głosów: ' + str(neutralne) + '\n')
F.write('pozytywne\twszystkich: ' + str(questions) + '\t0 głosów: ' + str(questions-pozytywne) + '\toddanych głosów: ' + str(pozytywne) + '\n')
F.write('bardzo pozytywne\twszystkich: ' + str(questions) + '\t0 głosów: ' + str(questions-bPozytywne) + '\toddanych głosów: ' + str(bPozytywne) + '\n')
F.write('Oddanych głosów: ' + str(allVotes) + '\n')
F.write('Obecnie oceniono ' + str(bNegatywne+bPozytywne+pozytywne+negatywne+neutralne) + ' z ' + str(questions) + ' wpisów')

F.close()

FvNeg.close()
Fneg.close()
Fneu.close()
Fpos.close()
FvPos.close()