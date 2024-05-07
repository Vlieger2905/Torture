import xml.etree.ElementTree as ET
import csv
from io import StringIO

def tmx_to_grid(file_path):
    # Parse TMX file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Find the layer element with the desired name
    layer_name = "Barrier"  # For the barrier layer
    layer = None
    for child in root.findall('.//layer'):
        if child.attrib['name'] == layer_name:
            layer = child
            break
    # If the layer is found
    if layer is not None:
        # Extract CSV data from layer
        csv_data = layer.find('data').text.strip()

        # Parse CSV data
        parsed_data = []
        reader = csv.reader(StringIO(csv_data))
        for row in reader:
            parsed_row = []
            for cell in row:
                if cell:  # Check if the cell is not empty
                    parsed_row.append(int(cell))
            parsed_data.append(parsed_row)

        for row_idx, row in enumerate(parsed_data):
            for col_idx, value in enumerate(row):
                # If the value is 0, change it to 1 for the pathfinder
                if value == 0:
                    parsed_data[row_idx][col_idx] = 1
                # If the value is 1, change it to 0 to make sure it's seen as an obstacle
                elif value != 1:
                    parsed_data[row_idx][col_idx] = 0
                # If it's neither 0 nor 1, leave it unchanged
                else:
                    pass



        return parsed_data
            
    else:
        print("Layer with Name {} not found.".format(layer_name))
