from nltk.corpus import movie_reviews
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy as nltk_accuracy
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
import aspell
import numpy as np
import time

fileVeryNegative    = open("vNegative.txt","r")
fileNegative        = open("negative.txt","r")
fileNeutral         = open("neutral.txt","r")
filePositive        = open("positive.txt","r")
fileVeryPositive    = open("vPositive.txt","r")

speller = aspell.Speller(('lang', 'pl'), ('master', '/usr/lib/aspell/pl.rws'))
morfSlownikFile = open("./sjp-odm-20180307/odm.txt","r")
#morfSlownik = set(line.strip() for line in morfSlownikFile)
morfSlownik = {}
with morfSlownikFile as inputfile:
    morfslowniktmp = []
    for line in inputfile:
        morfslowniktmp.append(line.strip().split(', '))
    for wordsTmp in morfslowniktmp:
        if (len(wordsTmp) > 1):
            for w in range(1,len(wordsTmp)):
                morfSlownik[wordsTmp[w]] = wordsTmp[0]
        else:
            morfSlownik[wordsTmp[0]] = wordsTmp[0]

counter = 0
all = 0

def extractFeatures(words):
    return dict([(word.lower(), True) for word in words])
    #return dict([(corrector(word).lower(), True) for word in words])

def extractFeatures2(words):
    #return dict([(word.lower(), True) for word in words.split()])
    #return dict([(corrector(word).lower(), True) for word in words.split()])
    global counter
    global all
    if (counter % 100 == 0):
        print(str(counter+1) + " / " + str(all))
    counter = counter + 1
    #return dict([(morfs2(corrector(word).lower()), True) for word in words.split()])
    return dict([(corrector(word).lower(), True) for word in words.split()])

def corrector(word):
    wynik = ""
    wynik = speller.suggest(word)

    if (len(wynik) > 0):
        return wynik[0]
    else:
        return word

def delWhiteSpaces(textTable):
    return [text.strip() for text in textTable]

def delSpecials(textTable):
    return [re.sub('[^A-Za-z0-9 żźćńąśłęóŻŹĆŃĄŚŁĘÓ]+','',text) for text in textTable]

def loadTweets(file):
    tmp = file.readlines()

    #return delSpecials(delWhiteSpaces(tmp))
    return delWhiteSpaces(tmp)

def morfs(word):
    if (any(word in x for x in morfSlownik)):
        index = findItem(morfSlownik, word)
        ind = (index[0][0])
        return morfSlownik[ind][0]
    else:
        return word

def morfs2(word):
    if word in morfSlownik:
        return morfSlownik[word]
    else:
        return word

def findItem(list, item):
    return[(ind, list[ind].index(item)) for ind in range(len(list)) if item in list[ind]]

if __name__=='__main__':
    t0 = time.time()

    negative = loadTweets(fileNegative)
    neutral = loadTweets(fileNeutral)
    positive = loadTweets(filePositive)

    all = len(negative) + len(neutral) + len(positive)

    featuresNegative = [(extractFeatures2(tweet), 'Negative') for tweet in negative]
    featuresNeutral = [(extractFeatures2(tweet), 'Neutral') for tweet in neutral]
    featuresPositive = [(extractFeatures2(tweet), 'Positive') for tweet in positive]

    #trainsplit 80/20
    threshold = 0.8

    numNegative = int(threshold * len(featuresNegative))
    numNeutral = int(threshold * len(featuresNeutral))
    numPositive = int(threshold * len(featuresPositive))

    dataTrain = featuresNegative[:numNegative] + featuresNeutral[:numNeutral] + featuresPositive[:numPositive]
    dataTest = featuresNegative[numNegative:] + featuresNeutral[numNeutral:] + featuresPositive[numPositive:]

    #liczba uzytych datapoints
    print('\nNumber of training datapoints: ', len(dataTrain))
    print('Number od test datapoints: ', len(dataTest))

    #odpalamy naiwnego bayesa
    #classifier = NaiveBayesClassifier.train(dataTrain)

    #sklearnowy

    pipeline = Pipeline([('tfidf', TfidfTransformer()),
                         ('chi2', SelectKBest(chi2, k = 1000)),
                         ('nb', MultinomialNB())])
    #classifier = SklearnClassifier(pipeline)

    classifier = SklearnClassifier(LogisticRegression(penalty='l1'))

    classifier.train(dataTrain)


    print('\nAccuracy of the classifier: ', nltk_accuracy(classifier, dataTest))


    #top15 most informative words
    #N = 15
    #print('\nTop ' + str(N) + ' most informative words:')
    #for i, item in enumerate(classifier.most_informative_features()):
    #    print(str(i+1)+'. ' + item[0])
    #    if i == N - 1: break

    #TESTUJEMY KLASYFIKATOR:
    inputReviews = [
        'ja pierdole',
        #'kocham oleńke',
        #'jak ja kocham oleńke',
        #'jak ja kocham moją oleńke ',
        #'kocham moją oleńke',
        #'najszczęśliwszy dzien w moim życiu',
        #'no i co pan panie ferdku na to powiesz',
        #'jaki ja jestem kurwa szczęśliwy',
        #'jaki ja jestem kurwa szczęśliwy xd',
        #'jaki ja jestem szczęśliwy',
        #'jaki ja jestem szczęśliwy xd',
        #'xd',
        #'xdd',
        #'xddd',
        #'bardzo szczęśliwy',
        #'niedziela wieczur i humor popsuty',
        'ludzie'
    ]

    print("\nPredictions:")
    for review in inputReviews:
        print("\nReview: ", review)

        #compute probabilities
        probabilities = classifier.prob_classify(extractFeatures(review.split()))
        #pick max prob
        predictedSentiment = probabilities.max()

        print("Predicterd sentiment: ", predictedSentiment)
        print("Probability: ", round(probabilities.prob(predictedSentiment),2))

    t1=time.time()
    print("Time: ", round(t1-t0, 4))
    #print(morfs('aborcjonistce'))

