# create edge list from the users and subreddits they post to
import json
import pandas as pd
import os
# users df
users = pd.read_pickle('../data/users.pkl')
users = users[['name', 'subreddit', 'type']]

# user subreddits json
path = '../data/user_subs/'
dates = ['2023-03-06', '2023-03-07']

# read each file in dir and append to list
user_subs = pd.DataFrame()
# create new columns
user_subs['name'] = ''
user_subs['subreddit'] = ''
for date in dates:
    files = os.listdir(path + date)
    for file in files:
        with open(path + date + '/' + file) as f:
            user_dict = json.load(f)
            names = user_dict.keys()
            subs = user_dict.values()
            user_subs = pd.concat([user_subs,pd.DataFrame({'name': names, 'subreddit': subs})])
# reset index
user_subs = user_subs.reset_index(drop=True)
# add 'from' column
drug_subs = ['LSD', 'stims', 'opiates', 'cocaine', 'benzodiazepines', 'shrooms', 'ambien', 'Autoflowers', 'cannabis', 'Drugs', 'MDMA', 'Psychedelics']
# subreddit type is list, iterate through list to find if any are in drug_subs
def find_druggsub(row):
    matches = []
    for sub in row:
        if sub in drug_subs:
            matches.append(sub)
    if len(matches) > 0:
        return matches
    else:
        return None

user_subs['from'] = user_subs['subreddit'].apply(find_druggsub)

# nan values are users who only commented but did not post
# drop rows where from in nan
user_subs = user_subs.dropna(subset=['from'])
# 8321 users and their subs

# expand subreddit column and from column
user_subs2 = user_subs.explode('subreddit')
user_subs2 = user_subs2.explode('from')

# drop rows where from == subreddit
user_subs2 = user_subs2[user_subs2['from'] != user_subs2['subreddit']]
# remove duplicates
user_subs2 = user_subs2.drop_duplicates()

# get freq
user_subs2['from'].value_counts(dropna=False)
# 186,833 pairs
# save to pickle
user_subs2.to_pickle('../data/subreddit_edges.pkl')
