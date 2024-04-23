import numpy as np
import math, random, pygame
from Game.settings import *
from .Enemy import *


class Enemy_Party(Enemy):
    def __init__(self, position, image, level, obstacle_sprites,tmx_file):
        super().__init__(position, image, level, obstacle_sprites,tmx_file)
        # Attribute
        
        # Overworld stats
        self.speed = 600
        self.first_frame = True
        self.hitbox = self.hitbox.inflate(-(self.hitbox.width * 0.45),-(self.hitbox.height * 0.45))
        self.hitbox.center = self.rect.center

        # Stats
        # TODO Initiate the stats of the enemy

        # Detection lines slime specifc settings        
        self.detection_range = 300
        self.amount_of_sensory_lines = 32
        
        self.sensory_lines = []
        starting_position = self.rect.center
        self.no_detection_colour = (0,255,255)

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
    # If it is not the first frame after the level loaded update the state of the slime
        if self.first_frame is False:
            # Checking for the distance
            player_distance = self.distance(player.rect.center)
# Changing the state
            # If the distance bewteen the player and the enemy is too big Make it that the enemy if not going to look for the player. 
            if player_distance >= enemy_update_radius:
                self.state = "idle"
            
            #if the distance is not too big, Try and find something
            else:    
                results = self.looking_around(player)
                
                # If the player is seen
                if results == "player found":
# TODO Make some sort of decision making to see if the enemy wants to run away, ignore or attack the player
                    self.state = "attacking"
                # Other wise just keep waddling around
                else: 
                    if self.state == "hunting":
                        pass
                    else:
                        self.state = "idle"
        
# Act according to the  state it is in
            # Check for the different states enemy and act accordingly
            if self.state == "idle":
                #  If there is still a path to the player location keep following that path
                if self.path:
                    self.state = "hunting"
                else:
                    pass

            #Hunt the player down when the enemy does not have vision of the player anymore 
            elif self.state == "hunting":
                if self.path:
                    # Walk to the first point 
                    self.direction = self.get_direction(self.path[0].center)
                    # Move the slime
                    self.move(dt)
                    # Check if the that point has been reached 
                    for rect in self.path:
                        if self.hitbox.colliderect(rect):
                            # If the point has been reached delete the point and walk to the next point
                            del self.path[0]
                            break
                else:
                    self.state = "idle"
            
            elif self.state == "attacking":
                # Check how much time passed in sec
                if self.time_passed_pathfinding >= enemy_pathfinding_time or self.path == []:
                    # Do pathfinding
                    path = self.pathfinding(player)
                    # Update the path
                    self.create_collision_rects(path)
                    # Reset the pathfinding time
                    self.time_passed_pathfinding = 0

                
                if self.path:
                    # Walk to the first point 
                    self.direction = self.get_direction(self.path[0].center)
                    # Move the slime
                    self.move(dt)
                    # Check if the that point has been reached 
                    for rect in self.path:
                        if self.hitbox.colliderect(rect):
                            # If the point has been reached delete the point and walk to the next point
                            del self.path[0]
                            break        
            # add dt to the pathfinding time 
            self.time_passed_pathfinding += dt

        # if it is the first frame after loading the level do nothing and set first frame false
        else:
            self.first_frame = False