import pandas as pd
import tweepy
import configparser
import numpy as np


followed_user_ids = pd.read_csv("temp_ids.csv")

# read configs 
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

bearer_token = config['twitter']['bearer_token']


access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authentication 
client = tweepy.Client(
    bearer_token=bearer_token, 
    consumer_key=api_key, 
    consumer_secret=api_key_secret, 
    access_token=access_token, 
    access_token_secret=access_token_secret)

user_ids = followed_user_ids['id'].values.tolist()

# TODO fix on 2/8/2023
# for user_index, user in followed_user_ids.iterrows():
#     user_data = client.get_users(ids=user_ids, extentions=["id", "name", "description"]).data
#     followed_user_ids["name"][user_index] == user_data[user_index].name
#     followed_user_ids["description"][user_index] == user_data[user_index].description


