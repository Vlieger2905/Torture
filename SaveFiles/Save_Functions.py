import json


# Collecting all the data and formatting that for use.
def collecting_data(player, game):
    # Creating the the entire dataset that needs to be saved:
    save_data = {
        # Getting the player stats
        "player_stats" : player.get_stats(),
        "player_items" : player.get_items(),
        "current level": game.load_map,
        "spawnpoint" : game.entry_point
    }
    return save_data

# Function to write the save data to a json file
def writing_save_data(data):
    file_name = "SaveFiles/Save File.json"
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Function to read the save data from a json file
def reading_save_data():
    file_name = "SaveFiles/Save File.json"
    with open(file_name, 'r') as json_file:
            data = json.load(json_file)
    return data
