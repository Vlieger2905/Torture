import pygame, math
from Game.Classes import Button
import Game.settings

# Function to calculate the accuracy of a action the current character does
def calculate_accuracy(current_character, target, skill):
    # Getting the difference in agility
    agility_outcome = current_character.Agility - target.Agility
    # Getting the hit chance based on the skill used and the stats of the current_character and the enemy
    if agility_outcome >= 0:  
        Hit = skill.base_accuracy + math.sqrt(agility_outcome)
    if agility_outcome < 0:
        Hit = skill.base_accuracy - math.sqrt(abs(agility_outcome))
    
    current_character_status_effect = 0
    target_status_effect = 0
    # Calculating the modifiers and % effect of the status 
    for status in current_character.status:
        current_character_status_effect += status.accuracy_modifier
    for status in target.status:
        target_status_effect += status.accuracy_modifier

    # Calculating the total effect of the player equipement on the accuracy
    equipement_bonus = 0
    target_equipement = 0
    for equipement in current_character.equipement:
        if equipement != "":
            equipement_bonus += equipement.accuracy_modifier
    # Calculate the effect the target equipement has on the accuracy
    for equipement in target.equipement:
        if equipement != "":
            target_equipement += equipement.accuracy_modifier


    # Calculating the actual accuracy
    accuracy = Hit + current_character_status_effect + equipement_bonus - target_status_effect - target_equipement

    if accuracy < 0:
        accuracy = 0
    if accuracy > 100:
        accuracy = 100

    return accuracy

# Function to calculate the damage a attack of a skill would do
def damage_calculation(current_character, target, skill):
    if hasattr(current_character, "inventory"):
        # Getting base damage and modifiers
        weapon = current_character.inventory.right_hand
        weapon_damage = weapon.base_damage
    if hasattr(current_character, "right_hand"):
        weapon_damage = current_character.right_hand.base_damage
    
    # Getting the modifier of the skill
    skill_modifier = skill.damage_modifier

    # Getting the bonus amount based on the skill used and the stats of the player
    if skill.modifier_type == "Might":
        bonus_damage = current_character.Might * skill.modifier_amount
    if skill.modifier_type == "Agility":
        bonus_damage = current_character.Agility * skill.modifier_amount
    if skill.modifier_type == "Mind":
        bonus_damage = current_character.Mind * skill.modifier_amount
    if skill.modifier_type == "Vitality":
        bonus_damage = current_character.Vitality * skill.modifier_amount    
    if skill.modifier_type == "Fortitude":
        bonus_damage = current_character.Fortitude * skill.modifier_amount

    
    # Calculating the modifiers and % effect of the status 
    current_character_status_effect = 1
    target_status_effect = 1
    for status in current_character.status:
        current_character_status_effect += status.accuracy_modifier
    for status in target.status:
        target_status_effect += status.accuracy_modifier

    # Calculate the effect the target equipement has on the accuracy
    target_resistance = 0
    for equipement in target.equipement:
        if equipement != "":
            pass
            # target_resistance += equipement.resistance
    target_resistance += target.resistance
# Total damage that would be dealt after all effect
    total_damage= (((weapon_damage * skill_modifier) * current_character_status_effect) + bonus_damage) * target_resistance

    return total_damage

# Function to provide a list of all the skill names for saving purposes
def return_skills(character_skills):
    list = []
    for skill in character_skills:
        list.append(skill.name)

    return list

# Function to create skills based on the skill list provided by the save file
def get_skills(skill_list):
    initiated_skill_list = []
    for skill in skill_list:
        # initiate the skill class whenever the name skill is in the list of skills the player has
        if skill == "strike":
            initiated_skill_list.append(Strike())
    return initiated_skill_list
            
class Skill_button():
    def __init__(self, position, output):
        self.rect = pygame.Rect(position, (0, 0))
        self.pressed = False
        self.size = (64,64)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect.size = self.image.get_size()   
        self.rect.topleft = position

        # Saves the output of the button. This will be returned when the button is pressed
        self.output = output 

    # Drawing the button on the screen
    def draw(self, screen, position):
        self.rect.topleft = position
        screen.blit(self.image, self.rect)

    # Function to handle button presses
    def handle_event(self, event):
        # Left mouse button pressed
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
        # Left mouse button released
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed and self.rect.collidepoint(event.pos):
                # Perform button click action here
                self.pressed = False
                return self.output
                # You can replace the print statement with your desired action
            self.pressed = False
        return None

class Strike(Skill_button):
    def __init__(self):
        # Combat stats
        self.damage_modifier = 1
        self.base_accuracy = 100
        # Stat the skill gets more damage with
        self.modifier_type = "Might"
        # Percentage amount of increase based on the stat. So if might is 100 and modifier is 0.5 you get 50% extra damage
        self.modifier_amount = 0

        # Other variables
        self.name = "strike"
        # Variables for the skill button

        self.image = pygame.image.load("Sprites//Combat//Skills Icon//Strike.png")

        super().__init__((0,0), self)

