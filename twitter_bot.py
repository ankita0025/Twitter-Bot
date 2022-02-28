print("hello")
import tweepy as twitter
import secret
import datetime
import time

FILE_NAME = "last_seen_id.txt"

auth = twitter.OAuthHandler(secret.API_KEY, secret.API_SECRET_KEY)
auth.set_access_token(secret.ACCESS_TOKEN,secret.SECRET_ACCESS_TOKEN )
api = twitter.API(auth)

def bot1(hashtags):
    n =0
    while n<5:
        print(datetime.datetime.now())

        for hashtag in hashtags:
            for tweet in twitter.Cursor(api.search , q = hashtag, rpp =10).items(5):
                try:

                    id = dict(tweet._json)["id"]
                    text = dict(tweet._json)["text"]

                    api.retweet(id)
                    api.create_favorite(id)


                    print("tweet_id:",id)
                    print("tweet text :",text)
                except twitter.TweepError as e:
                    print(e.reason)
        n+=1
        time.sleep(10)



def retrive_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id =int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id , file_name):
    f_write = open(file_name , 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    last_seen_id = retrive_last_seen_id(FILE_NAME)


    mentions  = api.mentions_timeline(last_seen_id, tweet_mode = "extended")

    for mention in reversed(mentions):
        print(str(mention.id) +" - "+ mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id , FILE_NAME)
        if "#needofo2" in mention.full_text.lower():
            print("found #needofo2")
            print("responding back")
            api.update_status("@" + mention.user.screen_name + " getting back to you! STAY SAFE", mention.id)
while True:
    reply_to_tweets()
    time.sleep(10)


