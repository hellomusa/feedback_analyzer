from flask import render_template, url_for, redirect, request
from analyzer import app

@app.route("/")
def home():
	return "<h1> hello world! </h1>"