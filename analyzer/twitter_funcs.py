import argparse
import mysql.connector

def get_tweets(is_technical=None):
	parser = argparse.ArgumentParser()
	parser.add_argument('sql_password', help='SQL database password')
	args = parser.parse_args()

	mydb = mysql.connector.connect(
	host = '15.222.147.65',
	user = 'root',
	passwd = args.sql_password,
	database = 'admin_prod'
	)

	if is_technical == None:
		sql_select_query = "SELECT * from tweets"
	elif is_technical:
		sql_select_query = "SELECT * from tweets WHERE is_technical = 1"
	else:
		sql_select_query = "SELECT * from tweets WHERE is_technical is NULL"

	mycursor = mydb.cursor()
	mycursor.execute(sql_select_query)
	tweets = mycursor.fetchall()

	return tweets


def get_recent_tweets_count(tweets):
	counter = 0
	current_month = tweets[0][4][4:8] # Ex. "Jan"
	current_day = int(tweets[0][4][8:10])
	for tweet in tweets:
		tweet_month = tweet[4][4:8]
		tweet_day = int(tweet[4][8:10])
		if (tweet_month == current_month) and (tweet_day >= current_day - 5 and tweet_day <= current_day):
			counter += 1

	return counter


def get_tweet_sentiment(tweets):
	good_count = 0
	bad_count = 0
	for tweet in tweets:
		if tweet[7] == "1":
			good_count += 1
		else:
			bad_count += 1

	return_list = []

	if good_count > bad_count:
		return_list.append(True)
	else:
		return_list.append(False)

	return_list.append(good_count)
	return_list.append(bad_count)

	return return_list


