#Developed by Yrneh for the WPPD Mutual Fund Securities Trading Bot
import json
import time
import twitter
from twitter import *

consumer_key = 'bmU116990LaXs1axkdBpFG45Y'
consumer_secret = 'rkTK9Gr6XGruDLyCyHL8Tr7y2KVMzDLRNlkngqdaw9d9nqPXhG'
access_token = '983503114769653760-7NA0pPi3tc5b12eZKGEzTHHRdmMf48g'
access_secret = '9OiLPusP4qOZf4MkWo41L3eKB8kPQba1RnnTn99Dni4iU'
t = Twitter(auth=OAuth(access_token, access_secret, consumer_key, consumer_secret))
data = t.search.tweets(q='#awesome') #change awesome to whatever you want to query for

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
print("Success.")
