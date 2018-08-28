import tweepy
import jsonpickle
import json
import unicodecsv as csv
import pandas as pd
import numpy as np
import os
from datetime import date


def specific_attr(tweet_data):
    # User related fields
    user_id = tweet_data["user"]["id_str"]
    user_name = tweet_data["user"]["screen_name"]
    user_followers_count = tweet_data["user"]["followers_count"]
    user_favourites_count = tweet_data["user"]["favourites_count"]
    user_listed_count = tweet_data["user"]["listed_count"]
    user_verified = tweet_data["user"]["verified"]

    text = tweet_data["full_text"]

    return user_id,user_name,user_followers_count,user_favourites_count,user_listed_count,user_verified,text


def fetch_tweets(searchQuery):
    # consumer key, consumer secret, access token, access secret.
    ckey = "LPU0P3rStPE4u32FUMjGa6cN1"
    csecret = "mv3clTKi1mJmnZhVQh3ZkXoMj7s6CaRRfI1dj2Cykspc33KnLu"
    # atoken="597081592-SIwP953Pt1JBJojNHGSlb5mIOO1OfsF3QPDtvsi5"
    # asecret="gnaiAas66LwrsSjHq1w5mEpMKTqcruu73GyZSzcSNKOU9"

    auth = tweepy.AppAuthHandler(ckey, csecret)
    auth.secure = True
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    q = searchQuery
    tweetsPerQry = 100

    maxTweets = 2000000
    max_id = -1
    tweetCount = 0

    print("Downloading max {0} tweets".format(maxTweets))
    try:
        temp = pd.read_csv(searchQuery + "_tweets.csv")
        ID_col = pd.to_numeric(temp['id'], errors='coerce').fillna(0).astype(np.int64)
        sinceId = max(ID_col)
        print(sinceId)
    except:
        print("pandas didn't work")
        sinceId = None

    with open(searchQuery + '_tweets.csv', 'ab') as f:
        writer = csv.writer(f)

        if (sinceId == None):
            writer.writerow(["id", "fetch_date", "created_at", "rt_status", "user_id","user_name","user_followers_count","user_favourites_count","user_listed_count","user_verified","text"])

        while tweetCount < maxTweets:
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = api.search(q=searchQuery, tweet_mode="extended", count=tweetsPerQry)
                    else:
                        new_tweets = api.search(q=searchQuery, tweet_mode="extended", count=tweetsPerQry,
                                                since_id=sinceId)
                else:
                    if (not sinceId):
                        new_tweets = api.search(q=searchQuery, tweet_mode="extended", count=tweetsPerQry,
                                                max_id=str(max_id - 1))
                    else:
                        new_tweets = api.search(q=searchQuery, tweet_mode="extended", count=tweetsPerQry,
                                                max_id=str(max_id - 1),
                                                since_id=sinceId)
                if not new_tweets:
                    print("No more tweets found")
                    break

                for tweet in new_tweets:
                    # print(tweet.full_text)
                    all_data = json.loads(jsonpickle.encode(tweet._json, unpicklable=False))
                    id = int(all_data["id_str"])
                    # print(id)
                    created_at = all_data["created_at"]
                    # Add the coordinates

                    if hasattr(tweet, 'retweeted_status'):
                        rt_status = 1
                        tweet_data = all_data["retweeted_status"]

                    else:
                        rt_status = 0
                        tweet_data = all_data

                    spec_attr = specific_attr(tweet_data)

                    fetch_date = str(date.today())
                    
                    row_list = list()
                    row_list.extend([id,fetch_date,created_at,rt_status])
                    row_list.extend(spec_attr)
                    
                    writer.writerow(row_list)

                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break

    print("Downloaded all tweets")

