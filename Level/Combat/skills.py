import pygame, math
from Game.Classes import Button

# TODO
def calculate_accuracy(self, player, target, skill):
    # Getting the difference in agility
    agility_outcome = player.Agility - target.Agility
    # Getting the hit chance based on the skill used and the stats of the player and the enemy
    if agility_outcome >= 0:  
        Hit = skill.accuracy + math.sqrt(agility_outcome)
    if agility_outcome < 0:
        Hit = skill.accuracy + math.sqrt(abs(agility_outcome))
    
    # Calculating the actual accuracy
    accuracy = Hit + player.status + player.equipement - target.status - target.equipement

    return accuracy

def return_skills(character_skills):
    list = []
    for skill in character_skills:
        list.append(skill.name)

    return list


def get_skills(skill_list):
    initiated_skill_list = []
    for skill in skill_list:
        # initiate the skill class whenever the name skill is in the list of skills the player has
        if skill == "strike":
            initiated_skill_list.append(Strike())

    return initiated_skill_list
            

class Strike():
    def __init__(self):
        # Other variables
        self.name = "strike"
        self.image = pygame.image.load("Sprites//DEV resources//Player Spawn.png")
        # Combat stats
        self.base_damage = 10
        self.base_accuracy = 70
        self.modifier = "Might"


