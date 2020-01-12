from flask import render_template, url_for, redirect, request
from analyzer import app
import argparse
import mysql.connector


def get_tweets():
	parser = argparse.ArgumentParser()
	parser.add_argument('sql_password', help='SQL database password')
	args = parser.parse_args()

	mydb = mysql.connector.connect(
	host = '15.222.147.65',
	user = 'root',
	passwd = args.sql_password,
	database = 'admin_prod'
	)

	sql_select_query = "select * from tweets"
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


@app.route("/")
def home():
	tweets = get_tweets()
	tweets_count = get_recent_tweets_count(tweets)
	return render_template('home.html', tweets_count=tweets_count)

@app.route("/tweets")
def tweets():
	tweets = get_tweets()
	return render_template('tweets.html', tweets=tweets)

@app.route("/login")
def login():
	return render_template('login.html')
