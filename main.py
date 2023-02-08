import tweepy
import configparser
import pandas as pd
from collections import Counter
import re

pd.set_option('mode.chained_assignment', None)
# to bring back SetWithCopyWarning
# pd.reset_option("mode.chained_assignment")

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

def get_followed_ids(usernames:list, num_followers:int):
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
    df = pd.DataFrame(Counter(all_follows).items(), columns=['id', 'followed_by_count'])
    df = df.sort_values('followed_by_count',ascending=False)
    return df[df.followed_by_count >= num_followers], coaches_df

def add_names_and_descriptions(player_id_df:pd.DataFrame):
    user_ids = player_id_df['id'].values.tolist()
    # create name and description columns with empty strings
    names = []
    descriptions = []
    # get all names and descriptions for users in id list
    list_sections = [user_ids[x:x+100] for x in range(0, len(user_ids), 100)]
    for list_section in list_sections:
        user_data = client.get_users(ids=list_section, user_fields=["description"]).data
        for user_index in range(len(user_data)):
            names.append(user_data[user_index].name)
            descriptions.append(user_data[user_index].description)
    # add information to dataframe
    player_id_df["name"] = names
    player_id_df["description"] = descriptions
    return player_id_df

def filter_users(df:pd.DataFrame, filter_words:list, and_or:bool):
    
    dropped_rows = df[df["description"].isnull()]
    df.dropna(inplace=True)
    if and_or == True:
        filter_string_and = ""
        for word_index in range(len(filter_words)):
            filter_string_and += f"(?=.*{filter_words[word_index]})"
        filtered_ids = df[df['description'].str.contains(filter_string_and, flags=re.IGNORECASE, regex=True)]
    elif and_or == False:
        filter_string_or = "|".join(filter_words)
        filtered_ids = df[df['description'].str.contains(filter_string_or, flags=re.IGNORECASE, regex=True)]

    return filtered_ids, dropped_rows

def get_followed_by(player_df:pd.DataFrame, coaches_df:pd.DataFrame):
    player_df['coaches_engaged'] = list

    for player_row in player_df.itertuples():
        coaches_engaged = []
        player_id = player_row[1]
        
        for coach_row in coaches_df.itertuples():
            coach_following_list = coach_row[1]
            if player_id in coach_following_list:
                coaches_engaged.append(coach_row[2])

        player_df['coaches_engaged'][player_row[0]] = coaches_engaged
    return player_df

# read usernames and get twitter ids
usernames = ["Taylor_Wike_", "jodydavidson", "ashleychastain", "cj_leighton"]
filter_words = ["High School"]
number_of_following_accounts = 3
# 
player_twitter_ids, coaches_df = get_followed_ids(usernames, number_of_following_accounts)
player_twitter_ids = add_names_and_descriptions(player_twitter_ids)
player_twitter_ids,dropped = filter_users(player_twitter_ids, filter_words, and_or=True)
player_twitter_ids = get_followed_by(player_twitter_ids, coaches_df)
print(player_twitter_ids.head())

# Saving to csv for manipulation 
player_twitter_ids.to_csv("temp_ids.csv")
coaches_df.to_csv("coaches.csv")