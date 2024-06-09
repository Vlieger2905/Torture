import pygame, math, json
from Game import settings
from Level.Combat.skills import get_skills

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
        # level and stats of the Ally
        self.level = self.data["level"]
        self.Might = self.data["Might"]
        self.Agility = self.data["Agility"]
        self.Mind = self.data["Mind"]
        self.Vitality = self.data["Vitality"]
        self.Fortitude = self.data["Fortitude"]

        # Skills the ally has
        self.skills = get_skills(self.data["skills"])

        