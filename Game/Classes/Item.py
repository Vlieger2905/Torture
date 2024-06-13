import pygame
from ..settings import *
import json

# Reading the json file
with open("Items//items_list.json", 'r') as file:
   items = json.load(file)

def creating_items():
    item_list = []
    # Extracting the information for each item
    for item in items:
        name = item['name']
        description = item['description']
        image_location = item['image_location']
        item_class = item['item_class']
        base_damage = item['base damage']
        damage_modifier = item['damage modifier']
        accuracy_modifier = item['accuracy modifier']
        item_list.append(Item(name, description, image_location,item_class, base_damage, damage_modifier, accuracy_modifier))
    return item_list

def create_item(item_name):
    for item in items:
        if item_name == item['name']:
            # Extracting the information from the json file to create the item
            name = item['name']
            description = item['description']
            image_location = item['image_location']
            item_class = item['item_class']
            base_damage = item['base damage']
            damage_modifier = item['damage modifier']
            accuracy_modifier = item['accuracy modifier']
            # Creating the actual item
            created_item = Item(name, description, image_location,item_class, base_damage, damage_modifier, accuracy_modifier)
            return created_item
    
        

class Item:
    def __init__(self, name, description, image, item_class, base_damage, damage_modifier, accuracy_modifier):
        # Defining the attributes of the specific item
        self.name = name
        self.discription = description
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, item_scale)
        # Item class that determines in which slot the item can go.
        self.type = item_class

        # Stats of the item
        self.base_damage = base_damage
        self.damage_modifier = damage_modifier
        self.accuracy_modifier = accuracy_modifier

    # Function to draw the item
    def draw(self, screen, position):
        screen.blit(self.image, position)
