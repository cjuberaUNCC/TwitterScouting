import pandas as pd

pd.set_option('mode.chained_assignment', None)
# to bring back SetWithCopyWarning
# pd.reset_option("mode.chained_assignment")

player_info_df = pd.read_csv("temp_ids.csv",index_col=0)
coaches_info_df = pd.read_csv("coaches.csv", index_col=0)



def get_followed_by(player_df:pd.DataFrame, coaches_df:pd.DataFrame):
    player_df['coaches_engaged'] = list

    for player_row in player_df.itertuples():
        coaches_engaged = []
        player_id = player_row[1]
        print(player_id)
        for coach_row in coaches_df.itertuples():
            coach_following_list = coach_row[1]
            if str(player_id) in coach_following_list:
                coaches_engaged.append(coach_row[2])

        player_df['coaches_engaged'][player_row[0]] = coaches_engaged
    return player_df

df = get_followed_by(player_info_df, coaches_info_df)
print(df["coaches_engaged"])

    




