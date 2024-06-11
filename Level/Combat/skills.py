import pygame, math
from Game.Classes import Button
import Game.settings

# TODO
def calculate_accuracy(self, player, target, skill):
    # Getting the difference in agility
    agility_outcome = player.Agility - target.Agility
    # Getting the hit chance based on the skill used and the stats of the player and the enemy
    if agility_outcome >= 0:  
        Hit = skill.accuracy + math.sqrt(agility_outcome)
    if agility_outcome < 0:
        Hit = skill.accuracy - math.sqrt(abs(agility_outcome))
    
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
        self.base_damage = 10
        self.base_accuracy = 70
        self.modifier = "Might"

        # Other variables
        self.name = "strike"
        # Variables for the skill button

        self.image = pygame.image.load("Sprites//Combat//Skills Icon//Strike.png")

        super().__init__((0,0), self)

