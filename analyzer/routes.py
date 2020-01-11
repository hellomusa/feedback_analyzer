from flask import render_template, url_for, redirect, request
from analyzer import app

@app.route("/")
def home():
	return render_template('home.html')

@app.route("/tweets")
def tweets():
	return render_template('tweets.html')

@app.route("/login")
def login():
	return render_template('login.html')
