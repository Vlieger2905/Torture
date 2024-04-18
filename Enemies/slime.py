import numpy as np
import math, random, pygame
from Game.settings import *
from .Enemy import *


class Slime(Enemy):
    def __init__(self, position,image, level, obstacle_sprites):
        super().__init__(position, image, level, obstacle_sprites)
        # Attribute

        # Overworld stats
        self.speed = 300
        self.first_frame = True

        self.obstacle_sprites = obstacle_sprites
        self.hitbox = self.hitbox.inflate(-10,-10)
        self.hitbox.center = self.rect.center

        # Stats
        self.level = level
         # TODO Initiate the stats of the enemy

        # Detection lines slime specifc settings
        self.detection_range = 300
        self.amount_of_sensory_lines = 16
        self.amount_of_sensory_lines = 16
        
        self.sensory_lines = []
        starting_position = self.rect.center
        self.no_detection_colour = (0,0,255)
        self.detected_colour = (255,0,0)
        self.no_detection_colour = (0,0,255)
        self.detected_colour = (255,0,0)

        # Calculate coordinates for each endpoint
        for i in range(self.amount_of_sensory_lines):
            # Getting the point from the unit circle
            angle = i * math.pi / (self.amount_of_sensory_lines / 2)
            x = self.detection_range * math.cos(angle)
            y = self.detection_range * math.sin(angle)
            # Moving the point to the correct position compared to center of the enemy(starting point)
            endpoint_x = starting_position[0] + x
            endpoint_y = starting_position[1] + y
            # Adding the lines to the list.
            self.sensory_lines.append(((starting_position[0], starting_position[1]), (endpoint_x, endpoint_y), self.no_detection_colour))

    def update(self,dt, player):
        if self.first_frame is False:
            # Checking for the distance
            player_distance = self.distance(player.rect.center)
            # If the distance bewteen the player and the enemy is too big Make it that the enemy if not going to look for the player. 
            if player_distance >= enemy_update_radius:
                pass
                pass
            
            #if the distance is not too big, Try and find something
            else:    
                self.looking_around()
                player_found = self.player_detection(player)
                self.looking_around()
                player_found = self.player_detection(player)
                # If you found something go to the something
                if player_found == True:
                    self.direction = self.player_direction(player)
                    # Move the enemy
                    self.move(dt)

            # Other wise just keep waddling around
            # Other wise just keep waddling around

            
        else:
            self.first_frame = False

