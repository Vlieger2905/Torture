import json


# Collecting all the data and formatting that for use.
def collecting_data(player):
    # Creating the the entire dataset that needs to be saved:
    save_data = {}
    # Getting the player stats
    player_stats =player.get_stats()
    # print(player_stats)



















# Saving the items and writing them to a file

# Writing data to a JSON file
# with open("data.json", "w") as json_file:
#     json.dump(data, json_file, indent=4)

# print("Data has been written to data.json")

# # Reading data from a JSON file
# with open("data.json", "r") as json_file:
#     loaded_data = json.load(json_file)