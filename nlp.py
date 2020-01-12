import re, string, random, argparse, time
import mysql.connector
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier


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

stop_words = stopwords.words('english')
positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')
tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]


def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    
    return cleaned_tokens


positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

positive_cleaned_tokens_list = []
negative_cleaned_tokens_list = []

for tokens in positive_tweet_tokens:
    positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words)) # cleans the positive tweets

for tokens in negative_tweet_tokens:
    negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words)) # cleans the negative tweets


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


all_pos_words = get_all_words(positive_cleaned_tokens_list)
all_neg_words = get_all_words(negative_cleaned_tokens_list)
freq_dist_pos = FreqDist(all_pos_words)
freq_dist_neg = FreqDist(all_neg_words)


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

positive_dataset = [(tweet_dict, '1')
                     for tweet_dict in positive_tokens_for_model]

negative_dataset = [(tweet_dict, '0')
                     for tweet_dict in negative_tokens_for_model]


dataset = positive_dataset + negative_dataset

random.shuffle(dataset)
train_data = dataset[:7000]
test_data = dataset[7000:]
classifier = NaiveBayesClassifier.train(train_data)

while(True):
    sql_select_query = "select * from tweets"
    mycursor = mydb.cursor()
    mycursor.execute(sql_select_query)
    tweets = mycursor.fetchall()

    for tweet in tweets:
        tweet_class = classifier.classify(dict([token, True] for token in (remove_noise(word_tokenize(tweet[3])))))    

        if tweet_class == '1':
            print('test')
            tweet_id = tweet[6]
            sql_update_query = "UPDATE tweets SET tweet_class = %s WHERE tweet_id = %s"
            print(tweet_class, tweet_id)
            inputData = (tweet_class, tweet_id)
            mycursor.execute(sql_update_query, inputData)
            mydb.commit()
            
        else:
            print('test2')
            tweet_id = tweet[6]
            sql_update_query = "UPDATE tweets SET tweet_class = %s WHERE tweet_id = %s"
            inputData = (tweet_class, tweet_id)
            mycursor.execute(sql_update_query, inputData)
            mydb.commit()
        
    time.sleep(300)
            
