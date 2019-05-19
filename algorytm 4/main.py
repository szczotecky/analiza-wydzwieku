from nltk.classify.util import accuracy as nltk_accuracy
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression
import re
import time

fileVeryNegative    = open("vNegative.txt","r")
fileNegative        = open("negative.txt","r")
fileNeutral         = open("neutral.txt","r")
filePositive        = open("positive.txt","r")
fileVeryPositive    = open("vPositive.txt","r")


def extractFeatures(words):
    return dict([(word.lower(), True) for word in words])

def extractFeatures2(words):
    return dict([(word.lower(), True) for word in words.split()])

def delWhiteSpaces(textTable):
    return [text.strip() for text in textTable]

def delSpecials(textTable):
    return [re.sub('[^A-Za-z0-9 żźćńąśłęóŻŹĆŃĄŚŁĘÓ]+','',text) for text in textTable]

def loadTweets(file):
    tmp = file.readlines()

    #return delSpecials(delWhiteSpaces(tmp))
    return delWhiteSpaces(tmp)

if __name__=='__main__':
    t0 = time.time()

    negative = loadTweets(fileNegative)
    neutral = loadTweets(fileNeutral)
    positive = loadTweets(filePositive)

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


    classifier = SklearnClassifier(LogisticRegression(penalty='l1'))

    classifier.train(dataTrain)


    print('\nAccuracy of the classifier: ', nltk_accuracy(classifier, dataTest))


    #TESTUJEMY KLASYFIKATOR:
    inputReviews = [
        'jak ja kocham oleńke',
        'najszczęśliwszy dzien w moim życiu',
        'no i co pan panie ferdku na to powiesz',
        'jaki ja jestem kurwa szczęśliwy',
        'jaki ja jestem kurwa szczęśliwy xd',
        'jaki ja jestem szczęśliwy',
        'xd',
        'xdd',
        'xddd',
        'bardzo szczęśliwy',
        'niedziela wieczur i humor popsuty',
        'ludzie'
    ]

    print("\nPREDYKCJE:")
    for review in inputReviews:
        print("\nTREŚĆ: ", review)

        #compute probabilities
        probabilities = classifier.prob_classify(extractFeatures(review.split()))
        #pick max prob
        predictedSentiment = probabilities.max()

        print("Predicterd sentiment: ", predictedSentiment)
        print("Probability: ", round(probabilities.prob(predictedSentiment),2))

    t1=time.time()
    print("Time: ", round(t1-t0,4))

