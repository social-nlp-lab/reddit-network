# recovery-network
supporting code for works in understanding motivations behind recovery discussion on reddit


Main scripts:
1. `get_data.ipynb` : this notebook gets the active posters from each of the 12 subreddits chosen - dates : june 20218 - june 2022. from thse users, a random sample of 20k are selected for further analysis
1. `py/get_user_subreddits.py`: this script runs the PRAW api to get the list of subreddits each user has posted in with multi-threading.  
1. `py/create_edges`: each of the JSON files created in (2) are used to create the edge list for network analysis
1. `make-network.ipynb` : edge lilst from (3) used to calculate various measure of degree centrality and visualize the network
