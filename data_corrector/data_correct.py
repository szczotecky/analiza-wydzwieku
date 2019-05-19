import json
import pandas as pd

print('\xdf')

files= ["20171017-195946", "20171017-200226", "20171017-224116","20171018-215755"]

tweetsDataPath = "./data/"

for f in files:
    tweetsData = []
    tweetsFile = open(tweetsDataPath+f+".txt", "r", encoding='utf-8')
    tweetsText = []

    errors = 0

    for line in tweetsFile:
        try:
            tweet = json.loads(line)
        
            tweetsData.append(tweet)
            tweetsText.append(tweet['text'])
        except:
            continue

    tweetsSaveFile = open(tweetsDataPath+f+"_result.txt", "a")
    tweetsSaveFileTO = open(tweetsDataPath+f+"_result_TO.txt", "a")
    tweetsSaveFileRT = open(tweetsDataPath+f+"_result_RT.txt", "a")


    for t in tweetsText:
    
        string = " ".join(t.splitlines())
        try:
            if (string.find("RT @", 0, 4)== -1):
                if (string.find("@", 0, 2)== -1):
                    tweetsSaveFile.write(string)
                    tweetsSaveFile.write("\n")
                else:
                    tweetsSaveFileTO.write(string)
                    tweetsSaveFileTO.write("\n")
            else:                
                tweetsSaveFileRT.write(string)
                tweetsSaveFileRT.write("\n")

        except ValueError:
            errors = errors + 1 
            print ('BLAD KODOWANIA: ' + str(errors))
        
    #tweetsSaveFile.write(tweetsText[0])

    tweetsSaveFile.close()
    tweetsSaveFileRT.close()
    tweetsSaveFileTO.close()
    tweetsFile.close()
    print("zakonczono plik: ", f)

print("Zakonczono")