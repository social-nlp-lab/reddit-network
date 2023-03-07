import json
import praw
import concurrent.futures
import argparse
import aiohttp
import datetime
import os

file = 'py/api-creds.py'
exec(open(file).read())

# f = open('data/user_subreddits.json', 'w')

# create session with async function
async def create_session():
    async with aiohttp.ClientSession() as session:
        return session
    
# read list of users 
users = 'data/user_names.json'
with open(users) as f:
    user_names = json.load(f)

def get_subreddits(user_id):
    
    print(user_id)
    user_info = {}
    try:
        # Get the user's submission history
        submissions = reddit.redditor(user_id).submissions.new(limit=None)

        # Get the subreddit display_names for each submission
        subreddits = [
            submission.subreddit.display_name for submission in submissions]
        
        return subreddits
        # to dictionary
        user_info[user_id] = subreddits
    except:
        print('error')
        return []
    # write the dictionary to f 
    # print(user_info)
    # json.dump(user_info, f)

    

def parse_ids(user_ids, chunk_num):
    # Set up multi-threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map the user IDs to the get_subreddits() function
        futures = [executor.submit(get_subreddits, user_id)
                   for user_id in user_ids]

        # Wait for all tasks to complete and get the results
        results = [future.result()
                   for future in concurrent.futures.as_completed(futures)]

        # Create a dictionary to store the results
        user_subreddits = {}

        # Loop through the user IDs and results, and store in the dictionary
        for i, user_id in enumerate(user_ids):
            user_subreddits[user_id] = results[i]

        # Write the dictionary to a JSON file
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        # create directory if it doesn't exist
        if not os.path.exists(f'data/user_subs/{date}'):
            os.makedirs(f'data/user_subs/{date}')

        path = f'data/user_subs/{date}/user_subreddits_{chunk_num}.json'
        with open(path, 'w') as f:
            json.dump(user_subreddits, f)

# iterate over list of users in chunks of 1000
chunk_size = 1000
for i in range(0, len(user_names), chunk_size):
    # get 100 user names
    user_names_100 = user_names[i:i+chunk_size]
    # get subreddits for 100 users
    parse_ids(user_names_100, i)

# if __name__ == '__main__':
#     # Parse command-line arguments
#     # parser = argparse.ArgumentParser(
#     #     description='Get subreddits for a list of Reddit users')
#     # parser.add_argument('user_ids', metavar='USER_ID',
#     #                     nargs='+', help='a list of Reddit user IDs')
#     # args = parser.parse_args()

#     # Get the list of user IDs from the command-line arguments
#     # user_ids = args.user_ids
#     user_ids = user_names

#     # Set up multi-threading
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         # Map the user IDs to the get_subreddits() function
#         futures = [executor.submit(get_subreddits, user_id)
#                    for user_id in user_ids]

#         # Wait for all tasks to complete and get the results
#         results = [future.result()
#                    for future in concurrent.futures.as_completed(futures)]

#         # Create a dictionary to store the results
#         user_subreddits = {}

#         # Loop through the user IDs and results, and store in the dictionary
#         for i, user_id in enumerate(user_ids):
#             user_subreddits[user_id] = results[i]

#         # Write the dictionary to a JSON file
#         with open('data/user_subreddits.json', 'w') as f:
#             json.dump(user_subreddits, f)

# close session
async def close_session(session):
    await session.close()

