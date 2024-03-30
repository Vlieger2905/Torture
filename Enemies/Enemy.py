import numpy as np
import math, random, pygame
from pygame.sprite import Sprite
from Game.settings import *


# General class for information that every enemy will have
class Enemy(Sprite):
    def __init__(self):
        super().__init__()
        
        # Move the Entity
    def move(self, dt):
        # If the Entity is moving making sure that the velocity stays the same and that the Entity is not moving faster when moving diagonally
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        # Moving the Entity
        move_vector = self.direction * self.speed * dt
        self.hitbox.x +=move_vector.x
        self.collision_walls('horizontal')
        self.hitbox.y +=move_vector.y
        self.collision_walls('vertical')

    # Checks for the collision of the Entity hitbox with the obstacles
    def collision_walls(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #Moving to the rigth
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0: #Moving to the left
                        self.hitbox.left = sprite.hitbox.right           

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #Moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0: #Moving up
                        self.hitbox.top = sprite.hitbox.bottom
    
    # Function to change the length of the sensory lines to either the detection range if there is not an obstacle in the way. Or to the side of the closest obstacle.
    def obstacle_detection(self):
        index = 0
        # for each sensor line check whether they collide with any object
        for line in self.sensory_lines:
            updated = False
            for object in self.obstacle_sprites:
                # Save the result in endpoint
                end_point = self.collide_detect(line, object)
            
                # If there is a collision update the line to the new line
                if end_point != None:
                    line = (line[0], end_point, self.no_detection_colour)
                    updated = True
            if updated:
                self.sensory_lines[index] = line
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
    