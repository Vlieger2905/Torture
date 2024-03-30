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
    
    