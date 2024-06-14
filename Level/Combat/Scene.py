import pygame, json, random

import pygame.draw_py
import Game.dt as deltaTime
from debug import *
from Game import settings
from Game.Classes import Button
from .skills import calculate_accuracy, damage_calculation
from Player.Ally import Ally
from Player.player import Player



class Combat_scene():
    def __init__(self, enemy_party, player_party, location) -> None:
        # Getting the display surface
        self.display_surface = pygame.display.get_surface()
        self.width = self.display_surface.get_width()
        self.height = self.display_surface.get_height()
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

        # information action buttons
        self.action_button_size = (64,64)
        
        # Loading the player party and corresponding images
        self.player = player_party
        self.scale = 2
        self.party_members = player_party.party_members
        self.player_image = pygame.transform.scale(self.player.image,(self.player.image.get_height() * self.scale,self.player.image.get_width() * self.scale))
        
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
        self.selected_skill = None
        self.current_turn_character = self.characters[0]

        # Small health information
        # Information to draw the small health bar for each character
        self.small_health_image = pygame.image.load("Sprites//Combat//Interface//small health bar.png")
        

        self.small_health_rect = self.small_health_image.get_rect()

    # Function to place the buttons in the correct space and be centered 
    def draw_action_buttons(self, skills):
        total_skills = len(skills)

        button_width = skills[0].rect.width
        button_height = skills[0].rect.height
        max_buttons_per_row = self.width / button_width        
        # List of x-coordinates
        coordinates = [0, 64, 128, 192, 256, 320, 384, 448, 512, 576, 640, 704, 768, 832, 896, 960, 1024, 1088, 1152, 1216]

        # Calculate the center index of the coordinates list
        center_index = len(coordinates) // 2

        # Iterate over the buttons and place them accordingly
        for index, button in enumerate(skills):
            row = index // max_buttons_per_row
            col = index % max_buttons_per_row
            
            # Calculate the start index for the current row
            current_row_button_count = min(max_buttons_per_row, total_skills - row * max_buttons_per_row)
            start_index = center_index - (current_row_button_count // 2)
            
            # Ensure we don't go out of bounds
            if start_index < 0:
                start_index = 0
            if start_index + current_row_button_count > len(coordinates):
                start_index = len(coordinates) - current_row_button_count
            
            # Calculate the x position based on the adjusted start index
            x_position = coordinates[int(start_index + col)]
            
            # Calculate the y position of the button
            y_position = self.height - (row + 1) * button_height
            
            # Draw the button on the display surface
            button.draw(self.display_surface, (x_position, y_position))

        # skills[0].draw(self.display_surface, (0,self.height - button_height))

    # Function to draw the health mana stamina interface and update the length of the bar to the length of the current character
    def draw_health_mana_stamina(self, character):
        max_length = 360
        
        # draw health bar 
        percentage_filled = character.health_points / character.max_health
        width = int(max_length * percentage_filled)
        health_rect = pygame.rect.Rect(12,8,width,24)
        health_colour = (217,87,99)
        pygame.draw.rect(self.display_surface, health_colour, health_rect)

        # draw stamina bar
        percentage_filled = character.stamina_points / character.max_stamina
        width = int(max_length * percentage_filled)
        stamina_rect = pygame.rect.Rect(12,52,width,24)
        stamina_colour = (126,226,57)
        pygame.draw.rect(self.display_surface, stamina_colour, stamina_rect)

        # draw mana bar
        percentage_filled = character.mana_points / character.max_mana
        width = int(max_length * percentage_filled)
        mana_rect = pygame.rect.Rect(12,96,width,24)
        mana_colour = (95,205,228)
        pygame.draw.rect(self.display_surface, mana_colour, mana_rect)

    # Function to draw a small health bar under every character
    def draw_small_health(self, button_character_list):
        for button in button_character_list:
            character = button.output
            health_colour = (217,87,99)
            #  Variable to scale how full the health bar should be
            percentill_health = character.health_points / character.max_health
            small_health_bar_rect = pygame.rect.Rect((button.rect.bottomleft), (self.small_health_image.get_width()*percentill_health, self.small_health_image.get_height()))
            
            pygame.draw.rect(self.display_surface, health_colour, small_health_bar_rect)
            
            # TODO scale the small health bar to the width of the character
            self.display_surface.blit(self.small_health_image, button.rect.bottomleft)
            


            



    # Function to keep track of whose turn it is and loop through the characters in combat
    def turn_tracker(self):
        # Cycle to the next character
        self.characters.append(self.characters[0])
        self.characters.pop(0)
        # Resetting the variables
        self.selected_entity = None
        self.selected_skill = None

    # Check whether the attack hits based on the Hitchance
    def hit_check(self,hit_chance):
        hit_roll = random.randint(0,100)
        return hit_roll < hit_chance

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

            # Get current turn
            self.current_turn_character = self.characters[0]
            # Draw if it is a player character. If it has type it is a enemy and it should not be drawn
            if not (hasattr(self.current_turn_character, "type")):
                # Drawing all the buttons for the actions of the current character
                self.draw_action_buttons(self.current_turn_character.skills)
                #  If you selected an enemy draw the status of the current turn character
                if hasattr(self.selected_entity, "type"):
                    # Drawing the stats of the current character, health mana stamina
                    self.draw_health_mana_stamina(self.current_turn_character)
                # If you selected a character different than the current character in your team. display their information
                elif not hasattr(self.selected_entity, "type") and self.selected_entity != None :
                    self.draw_health_mana_stamina(self.selected_entity)

                else:
                    # Drawing the stats of the current character, health mana stamina
                    self.draw_health_mana_stamina(self.current_turn_character)

                # Checking the action buttons to see if a skill is being selected. ONLY IF IT IS A PLAYER CONTROLLED CHARACTER
                skill_button_event =Button.check_events(self.current_turn_character.skills, pygame_events)
            # When it is the turn of the enemy there is no skill_button_event
            else:
                skill_button_event = None

            # Checking whether enemies or allies have been selected to change the target of the action
            character_select_event = Button.check_events(self.friendly_buttons, pygame_events)
            if character_select_event == None:
                character_select_event = Button.check_events(self.enemy_buttons, pygame_events)

            #Selecting the pressed character as the target 
            if character_select_event != None:
                self.selected_entity = character_select_event
                # print(self.selected_entity)
            # Selecting the pressed skill as the selected skill
            if skill_button_event != None:
                self.selected_skill = skill_button_event
                # print(self.selected_skill)


            # TODO Drawing the turn tracker( whose turn it is and the order of who is going to be next on top of the screen)

            # Drawing small health bars under each entity in the combat. 
            self.draw_small_health(self.friendly_buttons + self.enemy_buttons)

            # Drawing who the current character 
            for button in self.friendly_buttons + self.enemy_buttons:
                if button.output == self.current_turn_character:
                    pygame.draw.rect(self.display_surface, (255,255,255), button.rect, width= 5)
            
            # Draw a green rect around the selected skill
            if self.selected_skill:
                pygame.draw.rect(self.display_surface, (0,255,0), self.selected_skill, width= 5)
            
            # Draw a red rect around the target that has been selected
            if self.selected_entity:
                for button in self.enemy_buttons + self.friendly_buttons:
                    if button.output == self.selected_entity:
                        pygame.draw.rect(self.display_surface, (255,0,0), button.rect, width= 5)



            # Actual combat
            # If the current character is a player controlled character check if the player has selected anything
            if isinstance(self.current_turn_character, Ally.Ally) or isinstance(self.current_turn_character, Player):
                if self.selected_entity and self.selected_skill:
                    # Check if a friendly character is selected
                    if isinstance(self.selected_entity, Ally.Ally) or isinstance(self.selected_entity, Player):
                        # If a friendly character is selected deselect it
                        self.selected_entity = None
                    
                    # If an enemy is selected deal damage
                    else:
                        self.selected_entity.health_points
                        # Calc accuracy between current character and target. Also calculate if it hits
                        hit_chance = calculate_accuracy(self.current_turn_character, self.selected_entity, self.selected_skill)
                        # Bool outcome if the current character hit there target
                        outcome = self.hit_check(round(hit_chance))

                        # If outcome is true it calculates the damage
                        if outcome:
                            # If it hits calculate the damage done
                            true_damage = damage_calculation(self.current_turn_character, self.selected_entity, self.selected_skill)
                            # Substract the damage from the enemy
                            self.selected_entity.health_points -= true_damage

                        #TODO Substract cost for the skill/action from the character
                        #TODO Status effects
                        
                        # Continue to the next turn 
                        self.turn_tracker()




            # Ending of each frame and updating the screen 
            # debug(clock.get_fps())
            clock.tick()
            pygame.display.update()