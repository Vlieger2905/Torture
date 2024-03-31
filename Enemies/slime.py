import numpy as np
import math, random, pygame
from Game.settings import *
from .Enemy import *


class Slime(Enemy):
    def __init__(self, position, level, obstacle_sprites):
        super().__init__()
        # Attribute
        self.position = position
        self.image = pygame.image.load("Sprites\Enemies\Slime2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (Tilesize, Tilesize))
        self.direction = pygame.math.Vector2()
        self.rect  = self.image.get_rect()
        self.hitbox = self.rect.copy()
        self.rect.center = self.position
        self.hitbox.center = self.rect.center
        self.type = "enemy"
        # Overworld stats
        self.speed = 300
        self.first_frame = True

        self.obstacle_sprites = obstacle_sprites

        # Stats
        self.level = level

        # Detection lines slime specifc settings
        
        self.detection_range = 300
        self.amount_of_sensory_lines = 16
        
        self.sensory_lines = []
        starting_position = self.rect.center
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
            
            #if the distance is not too big, Try and find something
            else:    
                self.looking_around()
                player_found = self.player_detection(player)
                # If you found something go to the something
                if player_found == True:
                    self.direction = self.player_direction(player)
                    # Move the enemy
                    self.move(dt)

            # Other wise just keep waddling around

            
        else:
            self.first_frame = False

