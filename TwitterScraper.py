import json
import csv
import tweepy
import re
import Twitter_Credentials


def search_for_hashtags (api_key, api_secret_key, access_token, access_token_secret, hashtag_phrase):


    #create authentication for accessing Twitter
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    #initialize Tweepy API
    api = tweepy.API(auth)

    #get the name of the spreadsheet we will write to
    fname = '_'.join(re.findall(r"#(\w+)", hashtag_phrase))


    #open the spreadsheet we will write to
    with open('%s.csv' % (hashtag_phrase), 'w') as file:
        w = csv.writer(file)

        #write header row to spreadsheet
        w.writerow(['timestamp', 'tweet_text', 'username', 'all_hashtags', 'followers_count'])

    # for each tweet matching our hastag, write relavant info to the spreadsheet
        for tweet in tweepy.Cursor(api.search, q=hashtag_phrase+' -filter:retweets', lang="en", tweet_mode='extended').items(100):

            w.writerow([tweet.created_at, tweet.full_text.replace('\n',' '),
                      tweet.user.screen_name.encode('utf-8'), [e['text'] for e in tweet._json['entities']['hashtags']],
                      tweet.user.followers_count])



api_key = Twitter_Credentials.api_key
api_secret_key = Twitter_Credentials.api_secret_key
access_token = Twitter_Credentials.access_token
access_token_secret = Twitter_Credentials.access_token_secret

hashtag_phrase = input('Hashtag Phrase: ')


if __name__ == '__main__':
    search_for_hashtags(api_key, api_secret_key, access_token, access_token_secret, hashtag_phrase)