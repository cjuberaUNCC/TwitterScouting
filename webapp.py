import pandas as pd
import functions as func
import streamlit as st

usernames = ["Taylor_Wike_", "jodydavidson", "ashleychastain", "cj_leighton"]
filter_words = ["High School"]
number_of_following_accounts = 3

coaches_df = func.create_coaches_df(usernames)
# player_twitter_ids, coaches_df = get_liked_account_info(coaches_df, 4)
player_twitter_ids, coaches_df = func.get_followed_ids(coaches_df, number_of_following_accounts)
player_twitter_ids = func.add_names_and_descriptions(player_twitter_ids)
player_twitter_ids,dropped = func.filter_users(player_twitter_ids, filter_words, and_or=True)
player_twitter_ids = func.get_followed_by(player_twitter_ids, coaches_df)

st.write("Hi")