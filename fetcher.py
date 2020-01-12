# get tweets

# tweet will have username [string]
# tweet will have profile picture [url]
# tweet will have text  [text]
# tweet will have date  [datetime]
# is_technical [bool]

import sys, argparse
import jsonpickle
import requests
import tweepy
from analyzer import db
from analyzer.models import Tweet

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('c_api_key', help='Twitter consumer API keys')
    parser.add_argument('c_api_secret', help='Twitter consumer API secret key')

    args = parser.parse_args()

    consumer_token= args.c_api_key
    consumer_secret= args.c_api_secret

    auth = tweepy.AppAuthHandler(consumer_token, consumer_secret)
    auth.secure = True
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    search_query = '@AskRBC'
    retweet_filter='-filter:retweets'
    q=search_query+retweet_filter
    tweets_per_query = 100
    filename = 'tweets.txt'
    since_id = None

    max_id = -1
    max_tweets = 10000000 

    tweet_count = 0
    print("Downloading max {0} tweets".format(max_tweets))
    with open(filename, 'w') as f:
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
                    print("No more tweets found")
                    break
                for tweet in new_tweets:
                    tweet_text = tweet._json['text']
                    tweet_user = tweet._json['user']['screen_name']
                    tweet_replies = tweet._json['reply_count']
                    tweet_pfp = tweet._json['user']['profile_image_url']
                    tweet_date = tweet._json['created_at']

                    tw = Tweet(username=tweet_user, user_avatar=tweet_pfp, tweet_content=tweet_text, date_posted=tweet_date, is_technical=None)
                    db.Tweet.add(tw)
                    db.Tweet.commit()
                    
                print("Downloaded {0} tweets".format(tweet_count))
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break

    print ("Downloaded {0} tweets, Saved to {1}".format(tweet_count, filename))

if __name__ == '__main__':
    main()
    

