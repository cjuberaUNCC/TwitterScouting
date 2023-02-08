import tweepy
import configparser
import pandas as pd
from collections import Counter

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





def get_followed_ids(usernames, num_followers):
    users = client.get_users(usernames=usernames, user_fields=["id"])

    # create coaches dataframe that holds twitter ids, names, and following list
    coaches_df = pd.DataFrame(columns=["following"])
    coaches_df["username"] = usernames
    coaches_df["twitter_id"] = [users.data[x].id for x in range(len(usernames))]
    # create an all follows array that holds all twitter ids followed by users in list to count latter
    all_follows = []
    for row_index,row in coaches_df.iterrows():
        # create following list for current coach
        following = []
        # create list of following accounts if >1000 
        for response in tweepy.Paginator(client.get_users_following, id=coaches_df['twitter_id'][row_index],user_fields=["id"],max_results=1000,limit=2):
            # TODO: add counter for number of twitter requested used
            following += [(response.data[x].id) for x in range(len(response.data))]
        # add following list to coaches data frame
        coaches_df["following"][row_index] = following
        # add current coaches to all following
        all_follows += following


    df = pd.DataFrame(Counter(all_follows).items(), columns=['id', 'followed_by'])
    df = df.sort_values('followed_by',ascending=False)
    return df[df.followed_by >= num_followers]

# read usernames and get twitter ids
usernames = ["Taylor_Wike_", "jodydavidson", "ashleychastain"]
# "cj_leighton"
player_twitter_ids = get_followed_ids(usernames, 3)
player_twitter_ids.to_csv("temp_ids.csv")