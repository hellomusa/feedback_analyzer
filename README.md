# Feedback Analyzer
Monitors, tracks, analyzes and categorizes social media feedback 

# How to build and use

First of install all the dependancies, pip install -r requirements.txt

Make a SQL database and update the host in fetcher.py, techincal.py, routes.py and nlp.py

Remember to pass the database password as a command line argument

Run fetcher.py to get your tweets and save them to the database

Run nlp.py to train the model and classify the tweets as "positive" or "negative"

Run technical.py to classify the tweets as technical or non technical

Run run.py to start the web app