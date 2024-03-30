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
        self.speed = 100
        self.first_frame = True

        self.obstacle_sprites = obstacle_sprites

        # Stats
        self.level = level

        # Detection lines
        self.sensory_lines = []
        amount_of_sensory_lines = 16
        self.detection_range = 1000
        starting_position = self.rect.center
        self.no_detection_colour = (0,0,255)
        self.detected_colour = (255,0,0)
        # Calculate coordinates for each endpoint
        for i in range(amount_of_sensory_lines):
            # Getting the point from the unit circle
            angle = i * math.pi / (amount_of_sensory_lines / 2)
            x = self.detection_range * math.cos(angle)
            y = self.detection_range * math.sin(angle)
            # Moving the point to the correct position compared to center of the enemy(starting point)
            endpoint_x = starting_position[0] + x
            endpoint_y = starting_position[1] + y
            # Adding the lines to the list.
            self.sensory_lines.append(((starting_position[0], starting_position[1]), (endpoint_x, endpoint_y), self.no_detection_colour))
        self.original_state_sensory = self.sensory_lines




    def update(self,dt):
        if self.first_frame is False:
            self.move(dt)
            self.looking_around()
        else:
            self.first_frame = False
# A function that looks around the enemy and correctly reacts
    def looking_around(self):
        # Resetting the all the sensory lines to their original state
        self.sensory_lines = self.original_state_sensory
        # Putting the limit of each obstacle sprite to the start of a obstacle
        self.obstacle_detection()

# TODO fix it that the endpoint will only get clipped to the smallest distance
    def obstacle_detection(self):
        index = 0
        # for each sensor line check whether they collide with any object
        for line in self.sensory_lines:
            for object in self.obstacle_sprites:
                # Save the result in endpoint
                end_point = self.collide_detect(line, object)
                
                # If there is a collision the endpoint should not be none.
                if end_point != None:
                    self.sensory_lines[index] = (line[0], end_point, self.no_detection_colour)
                    # break
            index += 1
                

    def collide_detect(self, line, obstacle):
        # Use clipline to check for collision
        clipped_line = obstacle.rect.clipline(line[0], line[1])

        if clipped_line:
            # If clipped_line is not an empty tuple, then the line collides/overlaps with the rect
            start, end = clipped_line
            return start  # Return the first point where the line intersects with the rect
        else:
            return None  # Return None if no collision is detected
    
    # Function to calculate the distance between two points
    def distance_between_points(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance