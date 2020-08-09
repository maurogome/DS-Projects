import tweepy
import csv
import re
import string
import pandas as pd
import nltk as nltk
import matplotlib.pyplot as plt
from datetime import datetime
from nltk.corpus import stopwords
from wordcloud import WordCloud

nltk.download('stopwords')

consumer_key = 'NHM7F8y0d4ERLsh1FdXKyez3f'
consumer_secret = 'vd2UsO4mJ7H7oMbufEKhVLQZdj9aB4eOkkwjVG3CoRkOhvxhRU'
access_token_key = '69721550-yNbG4UDRpt3H5XJJA4qKWtQxP6WQUwOdIDf2T4MMS'
access_token_secret = '5t2MdIkdz9OnZVDKX4rnL4i2eS9Uz1pZwV8vxRnMHxYL4'

def api_connection():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True)

    try:
        api.verify_credentials()
        print('Authentification succesful! \n\n')
    except:
        print('Error! \n\n')

    return api

def extract_tweets(keyword, count):
    api = api_connection()
    tweets = []
    for tweet in tweepy.Cursor(api.search, q = keyword, lang = 'es', include_rts = False).items(count):
        if (not tweet.retweeted and 'RT @' not in tweet.text):
            tweets.append(tweet.text)
    return tweets

def transform(text):
    stopWords = set(stopwords.words('spanish'))
    text = str(text)
    text = re.sub(r'@[A-Za-z0-9]+', ' ', text)
    text = re.sub(r'RT[\s]', ' ', text)
    text = re.sub(r'#', ' ', text)
    text = re.sub(r'https?:\/\/\S+', ' ', text)

    words = text.lower().split()

    re_punc = re.compile('[%s]' % re.escape(string.punctuation))
    stripped = [re_punc.sub('', w) for w in words]
    no_garbage = [w for w in stripped if not w in stopWords]

    return (" ".join(no_garbage))

if __name__ == '__main__':

    keyword = input('Enter the account or hashtag you want to analyse...\n\n')
    api = api_connection()
    tweets = extract_tweets(keyword, 1000)
    df = pd.DataFrame(data = tweets, columns = ['tweet_text'])
    now = datetime.now().strftime('%Y_%m_%d')
    path = 'tweet_ext/tweets_{}_{datetime}.csv'.format(keyword[1:], datetime = now)
    df.to_csv(path, sep = ',', index = False)

    df['tweets_transform'] = df['tweet_text'].apply(transform)
    #text = df.tweets_transform
    text = ' '.join(df.tweets_transform)
    wordcloud = WordCloud(width = 1024, height = 800, background_color = 'black', min_font_size = 14).generate(text)
    img_path = 'img/wordcloud_{}_{datetime}.png'.format(keyword[1:], datetime = now)

    plt.figure(figsize = (8, 8), facecolor = 'black')
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.tight_layout(pad = 0)
    plt.savefig(img_path)
    plt.show()
