import json

def load_exit(json_file, exit_point):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    exits = data.get('exits', [])

    for exit_data in exits:
        name = exit_data.get('name', '')
        if name == exit_point:
            next_level = exit_data.get('next_level', '')
            spawn_point = exit_data.get('spawn_point', '')
            return (next_level, spawn_point)

    # If exit_point is not found, return a default value (e.g., None or an empty dictionary)
    return {}

