#!/usr/bin/env python
# -*- coding: utf-8 -*-
import twitter
import datetime
import urllib.request, json

api = twitter.Api(consumer_key='puOCS7Qy8rvSvHluJDhJZcqcR',
                  consumer_secret='cIQIzXkRxv2yJlR2GnGZPO2GGiIov7auSZrzlevGsMSVyM701p',
                  access_token_key='625100109-E6Rc57gTnIzlpN86GnEXgFCsBN51KNuJIBEhh8oU',
                  access_token_secret='TVHD8RkO4qIwjE5AplPhXOwgN1WTvNSVglEd6sbzBNiE0')


def get_filtered_words():
    url = "https://raw.githubusercontent.com/zacanger/profane-words/master/words.json"
    response = urllib.request.urlopen(url)
    filter = json.loads(response.read())
    return filter

def clean_tweet(status):
    s = status['created_at'].split(' ')
    return s[0] + ' ' + s[1] + ' ' + s[2] + ' ' + s[-1]

def weird_division(n, d):
    return n / d if d else 0

def convert_date(date):
    month = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    } [date[0]]
    day = int(date[1])
    year = int(date[2])
    return [month, day, year]

def convert_epoch(year,month,day):
    return datetime.datetime(year,month,day,0,0).timestamp()

def get_tweets_in_range(statuses, start=0, stop=0):
    if start == 0 and stop == 0:
        return statuses
    statuses_in_range = []
    for status in statuses:
        full_date = status['created_at'].split()
        date = [full_date[1], full_date[2], full_date[5]]
        date = convert_date(date)
        date_epoch = convert_epoch(date[2],date[0],date[1])
        if start <= date_epoch <= stop:
            statuses_in_range.append(status)
    return statuses_in_range


def flag_tweets(handle, start=0, stop=0):
    """Takes in start and stop dates in the format: '11 13 2018' for Nov. 13 2018"""
    timeline = api.GetUserTimeline(screen_name=handle, count=200, include_rts=False)
    earliest_tweet = min(timeline, key=lambda x: x.id).id

    while True:
        tweets = api.GetUserTimeline(
            screen_name=handle, max_id=earliest_tweet, count=200, include_rts=False
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            print("getting tweet id before: ",earliest_tweet)
            earliest_tweet = new_earliest
            timeline += tweets

    statuses = [i.AsDict() for i in timeline]

    start = start.split('-')
    start = convert_epoch(int(start[2]), int(start[0]), int(start[1]))

    stop = stop.split('-')
    stop = convert_epoch(int(stop[2]), int(stop[0]), int(stop[1]))

    statuses = get_tweets_in_range(statuses, start, stop)
    filtered_statuses = []
    filtered_words = get_filtered_words()
    for status in statuses:
        for word in status['text'].split():
            if word.lower() in filtered_words:
                filtered_statuses.append(status)
    with open('bad tweet/tweetid.json', 'a+') as f:
        for tweet in filtered_statuses:
            f.write(json.dumps(tweet['id']))
            f.write('\n')
    return filtered_statuses, round(100*weird_division(len(filtered_statuses), len(statuses)), 2), len(filtered_statuses), len(statuses)

def cleanedTweets(tweets):
    dateDict = dict()
    for status in tweets[0]:
        dateDict[clean_tweet(status)] = status['text']
    return dateDict, tweets[1], tweets[2], tweets[3]
