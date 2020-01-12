from flask import render_template, url_for, redirect, request
from analyzer import app
import argparse
import mysql.connector

@app.route("/")
def home():
	return render_template('home.html')

@app.route("/tweets")
def tweets():
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

	# tweets = Database.get.all ()
	# pass in tweets list to render_template
	return render_template('tweets.html')

@app.route("/login")
def login():
	return render_template('login.html')
