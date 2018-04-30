#Developed by Yrneh for the WPPD Mutual Fund Securities Trading Bot
import json
import time
import twitter
from twitter import *

consumer_key = 'insert yours here'
consumer_secret = 'insert yours here'
access_token = 'insert yours here'
access_secret = 'insert yours here'
t = Twitter(auth=OAuth(access_token, access_secret, consumer_key, consumer_secret))
data = t.search.tweets(q='#awesome') #change awesome to whatever you want to query for

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
print("Success.")
