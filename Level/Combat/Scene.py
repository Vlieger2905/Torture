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
        enemy_button_location = (self.json_data["enemy location"])
        enemy_button_location = [tuple(map(int, coord.split(','))) for coord in enemy_button_location.values()]
        enemy_button_location = [(x*self.scale, y*self.scale) for x,y in enemy_button_location]

        # Location of the action buttons
        self.action_buttons = []

        # Loading the player party and corresponding images
        self.player = player_party
        scale = 2
        self.party_members = player_party.party_members
        self.player_image = pygame.transform.scale(self.player.image,(self.player.image.get_height() * scale,self.player.image.get_width() * scale))
        
        # Creating the buttons for the friendly side to select
        # Draw the main character in the first slot
        self.friendly_buttons.append(Button.Button(friendly_button_location[3],self.player, self.player_image, combat=True))
        if self.party_members != []:
            i = 2
            for member in self.party_members:
                self.friendly_buttons.append(Button.Button(friendly_button_location[i], member ,pygame.transform.scale(member.image,(self.player_image.get_height(), self.player_image.get_width())), combat=True))
                # Drawing character from left to right
                i -= 1

        # Loading the enemy party and corresponding image
        self.enemy_party = enemy_party
        self.enemy_image = enemy_party.image

        # Creating the buttons for the enemy
        # Creating enemy party leader
        self.enemy_buttons.append(Button.Button(enemy_button_location[3],enemy_party.party_leader, image = self.enemy_party.image, combat=True, enemy = True))
        if self.enemy_party != []:
            i = 2
            for member in self.enemy_party.party_members:
                if hasattr(member, "combat_size"):
                    self.enemy_buttons.append(Button.Button(enemy_button_location[i],member,pygame.transform.scale(member.image_loaded, member.combat_size), combat=True, enemy = True))
                else:
                    self.enemy_buttons.append(Button.Button(enemy_button_location[i],member,pygame.transform.scale(member.image_loaded,(self.player_image.get_height(),self.player_image.get_width())), combat=True, enemy = True))
                # Drawing character from left to right
                i -= 1
        
        # Set-up for the turn tracker
        self.characters = []
        # Getting all the characters in the combat and saving that in a list
        for character in self.friendly_buttons:
            self.characters.append(character.output)
        for character in self.enemy_buttons:
            self.characters.append(character.output)
        self.characters.sort(key = lambda x: x.Agility, reverse=True)
        

        # General purpose variables
        self.selected_entity = None
        self.current_turn_character = self.characters[0]


    # function to draw the buttons of the actions of the current selected character in the party
    def draw_action_buttons(self, skills):
        button_background = pygame.image.load("Sprites//Combat//Interface//Combat interface action button.png")


    # Function to keep track of whose turn it is and loop through the characters in combat
    def turn_tracker(self):
        self.characters.append(self.characters[0])
        self.characters.pop(0)


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
            # Drawing all the buttons of the enemies
            for button in self.enemy_buttons:
                button.draw(self.display_surface)  

            # Checking whether enemies or allies have been selected to change the target of the action
            button_event = Button.check_events(self.friendly_buttons, pygame_events)
            if button_event == None:
                button_event = Button.check_events(self.enemy_buttons, pygame_events)

            if button_event != None:
                self.selected_entity = button_event
                print(self.selected_entity)


            # Drawing the turn tracker( whose turn it is and the order of who is going to be next on top of the screen)


            # Actual combat
                # Get current turn
            # self.current_turn_character = self.characters[0]
            #     # Drawing all the buttons for the actions 
            # for skill in self.current_turn_character.skills:
            #     print(skill)
                # if it is a player character display the possible skill to choose from
                # Get target
                # Calc accuracy between current character and target. Also calculate if it hits
                # If it hits calculate the damage done
                # Substract the damage from the enemy
                # Substract cost for the skill/action from the character
                # Continue to the next turn 



            # Ending of each frame and updating the screen 
            debug(clock.get_fps())
            clock.tick()
            pygame.display.update()