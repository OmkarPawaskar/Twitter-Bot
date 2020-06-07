import tweepy
import time
from keys import *
import sys
#importing all my api keys from keys.py file

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)


FILE_NAME = "last_seen_id.txt"

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    try:
        print('retrieving and replying to tweets...', flush=True)
        # DEV NOTE: use 1060651988453654528 for testing
        last_seen_id = retrieve_last_seen_id(FILE_NAME)
        # NOTE: We need to use tweet_mode='extended' below to show
        # all full tweets (with full_text). Without it, long tweets
        # would be cut off.
        mentions = api.mentions_timeline(last_seen_id,tweet_mode = 'extended') # since_id = last_seen_id ie Returns only statuses with an ID greater than (that is, more recent than) the specified ID.

        for mention in  reversed(mentions): #reversed it to start from oldest tweets
            print(str(mention.id) + '-' + mention.full_text , flush = True)
            last_seen_id = mention.id
            store_last_seen_id(last_seen_id , FILE_NAME)

            if '#helloworld' in mention.full_text.lower():
                print('found #helloworld !', flush = True)
                print('responding back...', flush = True)
                api.update_status('@'+ mention.user.screen_name + ' Hello back to you !', mention.id)
            elif 'hibot' in mention.full_text.lower():
                print('found #hibot !', flush = True)
                print('responding back...', flush = True)
                api.update_status('@'+ mention.user.screen_name + ' Hey there! Bot here!', mention.id)

            
    except Exception as err:
        print("Unexpected error:", sys.exc_info()[0])
    

while True:
    reply_to_tweets()
    time.sleep(15)