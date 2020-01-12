# -*- coding: utf-8 -*-

import sys, argparse
import tweepy
import mysql.connector

import unicodedata
from unidecode import unidecode

def string_cleaner(input_string):
    return_string = ""

    for character in input_string:
        try:
            character.encode("ascii")
            return_string += character
        except UnicodeEncodeError:
            replaced = unidecode(str(character))
            if replaced != '':
                return_string += replaced
            else:
                try:
                     return_string += "[" + unicodedata.name(character) + "]"
                except ValueError:
                     return_string += "[x]"

    return return_string

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('c_api_key', help='Twitter consumer API keys')
    parser.add_argument('c_api_secret', help='Twitter consumer API secret key')

    parser.add_argument('sql_password', help='SQL database password')

    args = parser.parse_args()

    consumer_token = args.c_api_key
    consumer_secret = args.c_api_secret

    mydb = mysql.connector.connect(
    host = '15.222.147.65',
    user = 'root',
    passwd = args.sql_password,
    database = 'admin_prod'
    )

    mycursor = mydb.cursor()

    auth = tweepy.AppAuthHandler(consumer_token, consumer_secret)
    auth.secure = True
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    search_query = '@AskRBC'
    retweet_filter='-filter:retweets'
    q=search_query+retweet_filter
    tweets_per_query = 100
    since_id = None

    max_id = -1
    max_tweets = 10000000 

    tweet_count = 0
    print(f'Downloading max {max_tweets} tweets')
    while tweet_count < max_tweets:
        try:
            if (max_id <= 0):
                if (not since_id):
                    new_tweets = api.search(q=search_query, count=tweets_per_query)
                else:
                    new_tweets = api.search(q=search_query, count=tweets_per_query,
                                            since_id=since_id)
            else:
                if (not since_id):
                    new_tweets = api.search(q=search_query, count=tweets_per_query,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=search_query, count=tweets_per_query,
                                            max_id=str(max_id - 1),
                                            since_id=since_id)
            if not new_tweets:
                print('No more tweets found')
                break
            for tweet in new_tweets:
                tweet_count += 1
                tweet_text = tweet._json['text']
                tweet_user = tweet._json['user']['screen_name']
                tweet_pfp = tweet._json['user']['profile_image_url']
                tweet_date = tweet._json['created_at']
                try:
                    tweet_text.encode('latin1')
                    
                    sql = 'INSERT INTO tweets (username, user_avatar, tweet_content, date_posted) VALUES (%s, %s, %s, %s)'
                    val = (tweet_user, tweet_pfp, tweet_text, tweet_date)
                    mycursor.execute(sql, val)
                    mydb.commit()
                except UnicodeEncodeError:
                    print('stop using emotes :-)')

                    tweet_text = string_cleaner(tweet_text)
                    sql = 'INSERT INTO tweets (username, user_avatar, tweet_content, date_posted) VALUES (%s, %s, %s, %s)'
                    val = (tweet_user, tweet_pfp, tweet_text, tweet_date)
                    mycursor.execute(sql, val)
                    mydb.commit()
            
            print(f'Downloaded {tweet_count} tweets')
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print('some error : ' + str(e))
            break

    print (f'Downloaded {tweet_count} tweets')

if __name__ == '__main__':
    main()
    

