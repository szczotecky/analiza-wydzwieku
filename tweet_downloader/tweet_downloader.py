#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas as pd
import time

#Variables that contains the user credentials to access Twitter API 
access_token = "828959798100111360-hKIgR9d4bpIu28hsPdZb8FPXXHoldQq"
access_token_secret = "ecehgjNDy3UiV0PRXJ36Q81GJr7TiKBWKoJNPrKbNNZ5p"
consumer_key = "6doKfDfPDG3LncrNEHvilpwqW"
consumer_secret = "jd1go9L55MXduxcdoGHt8F0mcbb6bFpVOXZrbGLkP6sLIIzRSK"

timestr = time.strftime("%Y%m%d-%H%M%S")


class StdOutListener(StreamListener):
    iter = 0
    def on_data(self, data):
        print('tweet')

        self.iter = self.iter + 1
        print(self.iter)
       

        file = open(timestr + ".txt", "a")
        
        file.write(data)
        
        file.close

        return True

    def on_error(self, status):
        print("error: " + status)

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    #12.10.2017 12:00 - 14:00
    #stream.filter(track=['NiechJadą', 'protestmedykow', 'rezydenci', 'patryk vega', 'Rada Europy'])
    #13.10.2017 10:00 - 14:00
    #stream.filter(track=['Kazań', 'Orkan Ofelia', 'Ofelia Huragan', 'Piątek 13', 'Hrynkiewicz'])

    #pl.wiktionary.org/wiki/Indeks:Polski_-_Najpopularniejsze_s%C5%82owa_1-1000_wersja_Jerzego_Kazojcia
    stream.filter(track=["sie","się","i","w","nie","na","z","do","to","że","a","o","jak","ale","po","co","tak","za","od","go",
                         "już","juz","jego","jej","czy","przez","tylko","tego","sobie","jeszcze","może","moze","ze","kiedy",
                         "pan","ich","dla","by","gdy","teraz","ja","ten","który"], languages=["pl"])

