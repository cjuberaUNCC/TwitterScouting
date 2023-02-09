import pandas as pd
import functions as func
import streamlit as st

coach_usernames = st.text_input('Account Usernames without the @ (max 25)', "Taylor_Wike_, jodydavidson, ashleychastain, cj_leighton").replace(" ","")
coach_usernames_list = coach_usernames.split(",")

num_of_engagments = st.slider(
    'Number of engagements on account',
    1, 25, (1))

filter_words = st.text_input('Words to filter accounts by their descriptions. If left blank all results will be shown.', "High School, 2025")
filter_words_list = filter_words.split(",")

filter_function = st.radio(
    "Filter And/Or",
     ("Or","And"))
filter_bool = None
if filter_function == "Or":
    filter_bool = False
if filter_function == "And":
    filter_bool = True

twitter_activity = st.radio(
    "Following or Liked",
     ("Liked","Following"))

if st.button('Run'):
    coaches_df = func.create_coaches_df(coach_usernames_list)
    
    if twitter_activity == "Liked":
        account_twitter_ids, coaches_interacted_df = func.get_liked_account_info(coaches_df, num_of_engagments)
    if twitter_activity == "Following":
        account_twitter_ids, coaches_interacted_df = func.get_followed_ids(coaches_df, num_of_engagments)
    account_twitter_details = func.add_names_and_descriptions(account_twitter_ids)
    account_twitter_details_filtered, dropped_accounts = func.filter_users(account_twitter_details, filter_words_list, and_or=filter_bool)
    account_twitter_final = func.get_followed_by(account_twitter_details_filtered, coaches_interacted_df)

    st.markdown("### Accounts that have been interacted with ")
    st.write(account_twitter_final)
    st.markdown("### Accounts with no bios")
    st.write(dropped_accounts)
