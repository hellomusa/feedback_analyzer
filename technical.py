import argparse, time
import mysql.connector

keywords = [
    "slow",
    "down",
    "load",
    "loading",
    "blank",
    "screen",
    "problem",
    "website",
    "closed",
    "error",
    "errors",
    "outage",
    "outages",
    "login",
    "register",
    "404",
    "broken",
    "technical",
    "question",
    "password",
    "user",
    "sign in",
    "sign up",
    "app",
    "bug",
    "report",
    "difficulty",
    "not",
    "working",
    "fixed",
    "error",
    "forever",
    "issues",
    "glitch",
    "glitching",
    "glitches" ]

parser = argparse.ArgumentParser()
parser.add_argument('sql_password', help='SQL database password')
args = parser.parse_args()

mydb = mysql.connector.connect(
host = '15.222.147.65',
user = 'root',
passwd = args.sql_password,
database = 'admin_prod'
)
mycursor = mydb.cursor()

sql_select_query = "select * from tweets"
mycursor = mydb.cursor()
mycursor.execute(sql_select_query)
tweets = mycursor.fetchall()

while(True):
    scores = {}
    for tweet in tweets:
        counter = 0
        for word in tweet[3].split(' '):
            if word in keywords:
                counter += 1

        if counter >= 2:
            tweet_id = tweet[6]
            sql_update_query = "UPDATE tweets SET is_technical = %s WHERE tweet_id = %s"
            input_data = (True, tweet_id)
            mycursor.execute(sql_update_query, input_data)
            mydb.commit()
        scores[tweet[6]] = counter

    time.sleep(300)