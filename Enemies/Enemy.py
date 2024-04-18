import numpy as np
import math, random, pygame
from pygame.sprite import Sprite
from Game.settings import *


# General class for information that every enemy will have
class Enemy(Sprite):
<<<<<<< HEAD
    def __init__(self,position, image, level, obstacle_sprites):
=======
    def __init__(self, position, image, level, obstacle_sprites):
>>>>>>> parent of 5eeaf4e (Revert "	modified:   Enemies/Enemy.py")
        super().__init__()
        self.position = position
        # Image and hitbox/rect specs
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Tilesize, Tilesize))
        self.direction = pygame.math.Vector2()
        self.redirection_vector = pygame.math.Vector2()
        self.rect  = self.image.get_rect()
        self.hitbox = self.rect.copy()
        self.rect.center = self.position
        self.hitbox.center = self.rect.center
<<<<<<< HEAD
        # Type and state
=======
        # Type 
>>>>>>> parent of 5eeaf4e (Revert "	modified:   Enemies/Enemy.py")
        self.type = "enemy"
        self.state = "idle"
        # Obstacles to collide with
        self.obstacle_sprites = obstacle_sprites
        # Stats
        self.level = level
<<<<<<< HEAD
=======
        
>>>>>>> parent of 5eeaf4e (Revert "	modified:   Enemies/Enemy.py")
        
    # Move the Entity
    def move(self, dt):
        # If the Entity is moving making sure that the velocity stays the same and that the Entity is not moving faster when moving diagonally
        if self.direction.magnitude() != 0:
            changed_x = False
            self.direction = self.direction.normalize()
<<<<<<< HEAD
        # Moving the Entity
        move_vector = self.direction * self.speed * dt
        self.hitbox.x +=move_vector.x
        self.collision_walls('horizontal')
        self.hitbox.y +=move_vector.y
        self.collision_walls('vertical')
        
        # Moving the Entity
        move_vector = self.direction * self.speed * dt
        self.hitbox.x +=move_vector.x
        self.collision_walls('horizontal')
        self.hitbox.y +=move_vector.y
        self.collision_walls('vertical')
        
        # Aligning the rect of the enemy to the hitbox of the enemy
        self.rect.center = self.hitbox.center
        # Updating the position of the sensory lines
        self.update_line_positions()
        # Updating the position of the sensory lines
        self.update_line_positions()
=======
            # Moving the Entity
            move_vector = self.direction * self.speed * dt
            self.hitbox.x +=move_vector.x
            # Checking if the enemy can move in the x- direction 
            if self.collision_walls('horizontal'):
                # Collision in x-direction nullifies that direction and increases the y direction to full
                self.direction.x = 0
                # If there is no vertical movement just return
                if self.direction.magnitude() == 0:
                    return
                
                self.direction = self.direction.normalize()
                print(self.direction)
                move_vector = self.direction * self.speed * dt
                changed_x = True
            
            # Moving the enemy in the y direction
            self.hitbox.y +=move_vector.y
            # Check for vertical colission
            if self.collision_walls('vertical'):
                self.hitbox.center = self.rect.center
                self.direction.y = 0
                # If there is no horizontal return
                if self.direction.magnitude() == 0:
                    return
                self.direction = self.direction.normalize()
                # If there is collision on the y and there was already collision on the x just return and change state.
                # The enemy is in a corner and should not be able to see the player
                if changed_x:
                    self.state = "searching"
                else:
                    print(self.direction)
                    move_vector = self.direction * self.speed * dt
                    self.hitbox.x = self.rect.x
                    self.hitbox.x += move_vector.x
                    # self.collision_walls('horizontal')
        # Aligning the rect of the enemy to the hitbox of the enemy
        self.rect.center = self.hitbox.center
        

    #TODO 
    # Function to change the direction of the enemy when it gets closer to a wall
    def redirect(self):
        x_sum= 0
        y_sum = 0
        for line in self.sensory_lines:
            x_sum += line[1][0]
            y_sum += line[1][1]
        # Getting the average endpoint of all the lines which is the coordinate of of the sum of all vectors
        end_point = x_sum / len(self.sensory_lines), y_sum / len(self.sensory_lines)
        # Putting the vector in the correct place
        end_point = end_point[0] - self.rect.center[0], end_point[1] - self.rect.center[1]
        self.redirection_vector = pygame.math.Vector2(end_point)
>>>>>>> parent of 5eeaf4e (Revert "	modified:   Enemies/Enemy.py")

    # Checks for the collision of the Entity hitbox with the obstacles
    def collision_walls(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #Moving to the rigth
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0: #Moving to the left
<<<<<<< HEAD
                        self.hitbox.left = sprite.hitbox.right           
                        self.hitbox.left = sprite.hitbox.right           
=======
                        self.hitbox.left = sprite.hitbox.right    

                    return sprite       
>>>>>>> parent of 5eeaf4e (Revert "	modified:   Enemies/Enemy.py")

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #Moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0: #Moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    
                    return sprite
    
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
                
    # Function to check whether the line overlaps with a rectangle and return the closest position
    def collide_detect(self, line, obstacle):
        # Use clipline to check for collision
        clipped_line = obstacle.rect.clipline(line[0], line[1])

        if clipped_line:
            # If clipped_line is not an empty tuple, then the line collides/overlaps with the rect
            start, end = clipped_line
            return start  # Return the first point where the line intersects with the rect
        else:
            return None  # Return None if no collision is detected

    # Function to detect the player
    def player_detection(self, player):
        for line in self.sensory_lines:
            # Check for each line if it intersects with the player
            player_found = self.collide_detect(line , player)
            # If it intersect return True
            if player_found != None:
                return True
        # if the player was not found return false
        return False

    # function to return the direction towards the player
    def player_direction (self, player):
        # Transforming the enemy and player position into a vector
        enemy_location = pygame.math.Vector2(self.rect.center)
<<<<<<< HEAD
        player_location = pygame.math.Vector2(player.rect.center)
        player_location = pygame.math.Vector2(player.rect.center)
=======
        player_location = pygame.math.Vector2(player.hitbox.center)
>>>>>>> parent of 5eeaf4e (Revert "	modified:   Enemies/Enemy.py")

        # Getting the vector from the enemy to the player
        direction = player_location-enemy_location

        return direction

    # A function that looks around the enemy and correctly reacts
    def looking_around(self,player):
        # Updating the position of the sensory lines
        self.update_line_positions()
        # Putting the limit of each sensory line to the start of a obstacle
        self.obstacle_detection()
        # Trying to detect the player
        player_detected = self.player_detection(player)
        # If the player has been found move to the player
        if player_detected:
            return "player found"

    # Function to calculate the distance between the enemy and a different point
    def distance(self, point2):
        x1, y1 = self.rect.center
        x2, y2 = point2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # Function to update the position of the lines
    def update_line_positions(self):
        starting_position = self.rect.center
        self.sensory_lines = []
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