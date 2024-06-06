import pygame, json
import Game.dt as deltaTime
from debug import *
from Game import settings
from Game.Classes import Button


class Combat_scene():
    def __init__(self, enemy_party, player_party, location) -> None:
        # Getting the display surface
        self.display_surface = pygame.display.get_surface()
        # Location where the combat is taking place. This is depended on the level and there enviroment
        self.combat_location = location
        # Getting the information for the combat scene that corresponds to the scene the combat is taking place in
        with open("Level//Combat//Combat scenes.json", 'r') as file:
            self.general_json_data = json.load(file)
        
        self.json_data = self.general_json_data[location]

        # Loading the background image
        self.background = pygame.image.load(self.json_data["background"])
        self.scale = settings.WIDTH/self.background.get_width()
        # Scaling to full screen
        self.background = pygame.transform.scale(self.background, (settings.WIDTH, settings.HEIGTH))

        # List to store all the different buttons
        self.friendly_buttons = []
        friendly_button_location = (self.json_data["friendly location"])
        friendly_button_location = [tuple(map(int, coord.split(','))) for coord in friendly_button_location.values()]
        friendly_button_location = [(x*self.scale, y*self.scale) for x,y in friendly_button_location]
        
        # Enemy buttons storage
        self.enemy_buttons = []
        enemy_button_location = self.json_data["enemy location"]
        self.action_buttons = []

        # Loading the player party and corresponding images
        self.player_party = player_party
        self.party_members = player_party.party_members
        self.player_image = player_party.image
        self.player_image = pygame.transform.scale(self.player_image,(self.player_image.get_height() * 2,self.player_image.get_width() * 2))
        
        # Creating the buttons for the friendly side to select
        # Draw the main character in the first slot
        self.friendly_buttons.append(Button.Button(friendly_button_location[3],"party member 1",self.player_image, combat=True))
        if self.party_members != []:
            i = 2
            for member in self.party_members:
                self.friendly_buttons.append(Button.Button(friendly_button_location[i],f"party member {i}",pygame.transform.scale(member.image,(self.player_image.get_height(),self.player_image.get_width())), combat=True))
                # Drawing character from left to right
                i -= 1

        # Loading the enemy party and corresponding image
        self.enemy_party = enemy_party
        self.enemy_image = enemy_party.image



    def run(self, clock):
        last_time = pygame.time.get_ticks()
        while True:
            last_time,dt = deltaTime.calculate_dt(last_time)
            # Checking for key inputs
            pygame_events = pygame.event.get()
            for event in pygame_events:
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        return last_time
            # Drawing the background
            self.display_surface.blit(self.background, (0,0)) 
            #Drawing all the buttons of the friendly characters
            for button in self.friendly_buttons:
                button.draw(self.display_surface)

            # Drawing all the buttons for the enemies


            # Drawing all the buttons for the actions 

            # Ending of each frame and updating the screen 
            debug(clock.get_fps())
            clock.tick(60)
            pygame.display.update()