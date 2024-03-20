import pygame
from ..settings import *
import json

def creating_items():
    item_list = []
    # Reading the json file
    with open("D:\Atlas\Year 2023\Personal Pursuit 2\Torture\Items\items_list.json", 'r') as file:
        items = json.load(file)   
    # Extracting the information for each item
    for item in items:
        name = item['name']
        description = item['description']
        image_location = item['image_location']
        item_class = item['item_class']
        item_list.append(Item(name, description, image_location,item_class))
    return item_list
        

class Item:
    def __init__(self, name, description, image, item_class ) -> None:
        # Defining the attributes of the specific item
        self.name = name
        self.discription = description
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, item_scale)
        # Item class that determines in which slot the item can go.
        self.type = item_class

    # Function to draw the item
    def draw(self, screen, position):
        screen.blit(self.image, position)
