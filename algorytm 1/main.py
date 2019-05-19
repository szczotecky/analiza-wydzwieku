from nltk.corpus import movie_reviews
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy as nltk_accuracy
import re
import time

fileVeryNegative    = open("vNegative.txt","r")
fileNegative        = open("negative.txt","r")
fileNeutral         = open("neutral.txt","r")
filePositive        = open("positive.txt","r")
fileVeryPositive    = open("vPositive.txt","r")


def extractFeatures(words):
    return dict([(word, True) for word in words])

def extractFeatures2(words):
    return dict([(word, True) for word in words.split()])

def delWhiteSpaces(textTable):
    return [text.strip() for text in textTable]

def delSpecials(textTable):
    return [re.sub('[^A-Za-z0-9 żźćńąśłęóŻŹĆŃĄŚŁĘÓ]+','',text) for text in textTable]

def loadTweets(file):
    tmp = file.readlines()
    return delSpecials(delWhiteSpaces(tmp))

if __name__=='__main__':

    t0 = time.time()

    veryNegative = loadTweets(fileVeryNegative)
    negative = loadTweets(fileNegative)
    neutral = loadTweets(fileNeutral)
    positive = loadTweets(filePositive)
    veryPositive = loadTweets(fileVeryPositive)

    featuresVeryNegative = [(extractFeatures2(tweet), 'VeryNegative') for tweet in veryNegative]
    featuresNegative = [(extractFeatures2(tweet), 'Negative') for tweet in negative]
    featuresNeutral = [(extractFeatures2(tweet), 'Neutral') for tweet in neutral]
    featuresPositive = [(extractFeatures2(tweet), 'Positive') for tweet in positive]
    featuresVeryPositive = [(extractFeatures2(tweet), 'VeryPositive') for tweet in veryPositive]

    #trainsplit 80/20
    threshold = 0.8

    numVeryNegative = int(threshold * len(featuresVeryNegative))
    numNegative = int(threshold * len(featuresNegative))
    numNeutral = int(threshold * len(featuresNeutral))
    numPositive = int(threshold * len(featuresPositive))
    numVeryPositive = int(threshold * len(featuresVeryPositive))


    dataTrain = featuresVeryNegative[:numVeryNegative] + featuresNegative[:numNegative] \
                + featuresNeutral[:numNeutral] + featuresPositive[:numPositive] + featuresVeryPositive[:numVeryPositive]
    dataTest = featuresVeryNegative[numVeryNegative:] + featuresNegative[numNegative:] \
                + featuresNeutral[numNeutral:] + featuresPositive[numPositive:] + featuresVeryPositive[numVeryPositive:]

    #liczba uzytych datapoints
    print('\nNumber of training datapoints: ', len(dataTrain))
    print('Number od test datapoints: ', len(dataTest))

    #odpalamy naiwnego bayesa
    classifier = NaiveBayesClassifier.train(dataTrain)

    print('\nAccuracy of the classifier: ', nltk_accuracy(classifier, dataTest))


    #top15 most informative words
    N = 15
    print('\nTop ' + str(N) + ' most informative words:')
    for i, item in enumerate(classifier.most_informative_features()):
        print(str(i+1)+'. ' + item[0])
        if i == N - 1: break

    #TESTUJEMY KLASYFIKATOR:
    inputReviews = [
        'ja pierdole',
        'kocham Oleńke',
        'jak ja kocham Oleńke',
        'kocham moją Oleńke',
        'najszczęśliwszy dzien w moim życiu',
        'no i co pan panie ferdku na to powiesz',
        'jaki ja jestem kurwa szczęśliwy',
        'XDD',
        'XDDD',
        'bardzo szczęśliwy',
        'niedziela wieczur i humor popsuty'
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


    t1 = time.time()
    print("Time: ", round(t1-t0, 4))