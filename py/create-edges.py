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

# expand subreddit column
user_subs = user_subs.explode('subreddit')
# take unique values
user_subs = user_subs.drop_duplicates()
#236,962 

# save to pickle
user_subs.to_pickle('../data/subreddit_edges.pkl')
