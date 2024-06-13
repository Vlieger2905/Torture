import pygame, math, json
from Game import settings
from Level.Combat.skills import get_skills
import Game.Classes.Item as it

# Retreiving the Ally item to save
def get_items(equipement_data):
    items ={
    "headwear": equipement_data.inventory.headwear.name if equipement_data.inventory.headwear else "",
    "chestplate": equipement_data.inventory.chestplate.name if equipement_data.inventory.chestplate else "",
    "pants": equipement_data.inventory.pants.name if equipement_data.inventory.pants else "",
    "boots": equipement_data.inventory.boots.name if equipement_data.inventory.boots else "",
    "necklace": equipement_data.inventory.necklace.name if equipement_data.inventory.necklace else "",
    "ring": equipement_data.inventory.ring.name if equipement_data.inventory.ring else "",
    "left hand": equipement_data.inventory.left_hand.name if equipement_data.inventory.left_hand else "",
    "right hand": equipement_data.inventory.right_hand.name if equipement_data.inventory.right_hand else "",
    "inventory_items" : [item.name if item else "" for item in equipement_data.inventory.inventory_items]
}
    return items

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

        # Damage absorption 1 = no absorption. A lower numbers means less damage taken
        self.resistance = 1
        
        # List of status effects the character has
        self.status = []

        # Skills the ally has
        self.skills = self.data["skills"]
        self.skills = get_skills(self.skills)

        # Equipement the Ally has
        self.equipement = []
        loaded_items = self.data["equipement"]
        # Defining all the equiped items of the player
        # Headwear
        self.headwear = loaded_items.get("headwear", "")
        if self.headwear != "":
            self.headwear = it.create_item(self.headwear)
        self.headwear_position = (448,224)
        # Chestplate
        self.chestplate = loaded_items.get("chestplate", "")
        if self.chestplate != "":
            self.chestplate = it.create_item(self.chestplate)
        self.chestplate_position = (448,320)
        # Pants
        self.pants = loaded_items.get("pants", "")
        if self.pants != "":
            self.pants = it.create_item(self.pants)
        self.pants_position = (448,416)
        # Boots
        self.boots = loaded_items.get("boots", "")
        if self.boots != "":
            self.boots = it.create_item(self.boots)
        self.boots_position = (448,512)
        # Necklace
        self.necklace = loaded_items.get("necklace", "")
        if self.necklace != "":
            self.necklace = it.create_item(self.necklace)
        self.necklace_position = (180,224)
        # Ring
        self.ring = loaded_items.get("ring", "")
        if self.ring != "":
            self.ring = it.create_item(self.ring)
        self.ring_position = (180,320)
        # Left hand
        self.left_hand = loaded_items.get("left hand", "")
        if self.left_hand != "":
            self.left_hand = it.create_item(self.left_hand)
        self.left_hand_position = (180,416)
        # Right hand
        self.right_hand = loaded_items.get("right hand", "")
        if self.right_hand != "":
            self.right_hand = it.create_item(self.right_hand)
        self.right_hand_position = (180,512)

        