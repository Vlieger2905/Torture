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

        # Maximum value the player has at the moment for the combat
        self.max_health = self.Vitality * math.sqrt(self.Vitality) + 20
        self.max_stamina = math.sqrt(self.Vitality) + 5
        self.max_mana = math.sqrt(self.Mind) + 5
        self.max_sanity = math.sqrt(self.Fortitude)

        # Current value the player has
        self.health_points = self.max_health
        self.stamina_points = self.max_stamina
        self.mana_points = self.max_mana
        self.sanity = self.max_sanity

        # Skills the ally has
        self.skills = get_skills(self.data["skills"])

        