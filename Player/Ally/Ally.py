import pygame, math, json
from Game import settings

class Ally():
    def __init__(self,name):
        # Opening the file with all allied information. 
        with open("Player//Ally//Ally_data.json", 'r') as file:
            entity_data = json.load(file)
        # All data for this specific character
        self.data = entity_data[name]

        # Information of this specific Ally
        self.name = name
        self.image = pygame.image.load(self.data["image"]).convert_alpha()
        self.level = self.data["level"]
        self.skills = self.data["skills"] 
        # self.stats

        