import tweepy
import configparser
import pandas as pd

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


# read usernames and get twitter ids
usernames = ["Taylor_Wike_", "jodydavidson", "ashleychastain", "cj_leighton"]
users = client.get_users(usernames=usernames, user_fields=["id"])


coaches_df = pd.DataFrame(columns=["following"])
coaches_df["username"] = usernames
coaches_df["twitter_id"] = [users.data[x].id for x in range(len(usernames))]
all
for row_index,row in coaches_df.iterrows():
    following_response = client.get_users_following(
        id=coaches_df['twitter_id'][row_index],
        user_fields=["id"],
        max_results=1000
        ).data
    coaches_df["following"][row_index] = [following_response[x].id for x in range(len(following_response))]
    # if len(following_response) == 1000:
    #     following_response_page_2 = client.get_users_following(
    #     id=coaches_df['twitter_id'][row_index],
    #     user_fields=["id"],
    #     max_results=1000,
    #     pagination_token="next_token"
    #     ).data
    #     coaches_df["following"][row_index] += [following_response_page_2[x].id for x in range(len(following_response_page_2))]

print(len(coaches_df["following"][0]))



# take list of twitter accounts


# return list of players they have followed in a certain time limit and number of accounts follows

# 