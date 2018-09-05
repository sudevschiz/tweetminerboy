import csv
import json
from datetime import date

import jsonpickle
import numpy as np
import pandas as pd
import tweepy


def specific_attr(tweet_data):
    # User related fields
    user_id = tweet_data["user"]["id_str"]
    user_name = tweet_data["user"]["screen_name"]
    user_followers_count = tweet_data["user"]["followers_count"]
    user_favourites_count = tweet_data["user"]["favourites_count"]
    user_listed_count = tweet_data["user"]["listed_count"]
    user_verified = tweet_data["user"]["verified"]

    text = tweet_data["full_text"]

    # Coordinates
    try:
        coordinates = tweet_data["coordinates"]["coordinates"]
    except TypeError:
        coordinates = ""

    # Encode names
    # user_name = user_name.encode('utf-8')
    # text = text.encode('utf-8')

    return user_id, user_name, user_followers_count, user_favourites_count, user_listed_count, user_verified, \
           coordinates, text


def fetch_tweets(searchquery):
    try:
        with open('key_file.json') as f:
            consumer = json.load(f)
    except FileNotFoundError:
        print("Authentication credentials not found. Fix the 'key_file.json' file")
        return

    auth = tweepy.AppAuthHandler(consumer['ckey'], consumer['csecret'])
    auth.secure = True
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    tweetsperqry = 100

    maxtweets = 2000000
    max_id = -1
    tweetcount = 0

    print("Downloading max {0} tweets".format(maxtweets))
    try:
        temp = pd.read_csv("./mined_tweets/" + searchquery + "_tweets.csv")
        id_col = pd.to_numeric(temp['id'], errors='coerce').fillna(0).astype(np.int64)
        sinceid = max(id_col)
        print(sinceid)
    except (IOError, ValueError):
        print("W : New keyword - New file created")
        sinceid = None

    with open("./mined_tweets/" + searchquery + '_tweets.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        print("Fetching tweets for the keyword : " + searchquery)
        if sinceid is None:
            writer.writerow(
                ["id", "fetch_date", "created_at", "rt_status", "user_id", "user_name", "user_followers_count",
                 "user_favourites_count", "user_listed_count", "user_verified", "coordinates", "text"])

        while tweetcount < maxtweets:
            try:
                if max_id <= 0:
                    if not sinceid:
                        new_tweets = api.search(q=searchquery, tweet_mode="extended", count=tweetsperqry)
                    else:
                        new_tweets = api.search(q=searchquery, tweet_mode="extended", count=tweetsperqry,
                                                since_id=sinceid)
                else:
                    if not sinceid:
                        new_tweets = api.search(q=searchquery, tweet_mode="extended", count=tweetsperqry,
                                                max_id=str(max_id - 1))
                    else:
                        new_tweets = api.search(q=searchquery, tweet_mode="extended", count=tweetsperqry,
                                                max_id=str(max_id - 1),
                                                since_id=sinceid)
                if not new_tweets:
                    print("No more tweets found")
                    break

                for tweet in new_tweets:
                    print(tweet)
                    # print(tweet.full_text)
                    all_data = json.loads(jsonpickle.encode(tweet._json, unpicklable=False))
                    # all_data = json.loads(tweet)
                    tweet_id = int(all_data["id_str"])
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
                    row_list.extend([tweet_id, fetch_date, created_at, rt_status])
                    row_list.extend(spec_attr)
                    # print(row_list)

                    writer.writerow(row_list)

                tweetcount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetcount))
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break

    print("Downloaded all tweets")


def fetch_scheduler(time_interval_sec, fetch_max_count=1000):
    fetch_counter = 0

    while fetch_counter < fetch_max_count:
        print("I am here")
