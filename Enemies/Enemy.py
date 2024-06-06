import numpy as np
import math, random, pygame
# Imports for the pathfinding
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.core.node import Node
from pathfinding.finder.a_star import AStarFinder
from Enemies.Making_Grid import *
# Self made files to import from
from pygame.sprite import Sprite
from Game.settings import *


# General class for information that every enemy will have
class Enemy(Sprite):
    def __init__(self, position, image, level, obstacle_sprites, tmx_file_path):
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
        self.time_passed_pathfinding = 0

        # Defining items for the pathfinding ability of all enemies
        self.grid = self.create_grid(tmx_file_path)
        # Pathfinder where diagonal movement is allowed when there is are nog obstacles next to the movement
        self.finder = AStarFinder(diagonal_movement = DiagonalMovement.only_when_no_obstacle)
        # Path to follow
        self.path = []

        # Type 
        self.type = "enemy"
        self.state = "idle"
        # Obstacles to collide with
        self.obstacle_sprites = obstacle_sprites
        # Stats
        self.level = level
          
    # Move the Entity
    def move(self, dt):
        # If the Entity is moving making sure that the velocity stays the same and that the Entity is not moving faster when moving diagonally
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            # Moving the Entity
            move_vector = self.direction * self.speed * dt
            # horizontal movement
            self.hitbox.x +=move_vector.x
            # Checking if the enemy can move in the x- direction 
            self.collision_walls('horizontal')
            
            # Moving the enemy in the y direction
            self.hitbox.y +=move_vector.y
            # Check for vertical colission
            self.collision_walls('vertical')
        # Aligning the rect of the enemy to the hitbox of the enemy
        self.rect.center = self.hitbox.center     

    # Pathfinding
    def pathfinding(self, player):
        # Starting point
        start_x = self.rect.centerx // Tilesize
        start_y = self.rect.centery // Tilesize
        start = self.grid.node(start_x,start_y)
        # End point
        end_x = player.hitbox.centerx // Tilesize
        end_y = player.hitbox.centery // Tilesize
        end = self.grid.node(end_x,end_y)

        # Pathfinding
        path, runs = self.finder.find_path(start, end, self.grid)
        self.grid.cleanup()

        return path

    # Getting the coordinates of each point in the path
    def create_collision_rects(self, path):
        if path: 
            temp = []
            del path[0]   

            for point in path:
                position = point.x, point.y
                position = (position[0]*Tilesize)+ (Tilesize/2), (position[1]*Tilesize)+ (Tilesize/2)
                temp.append(pygame.Rect(position[0]-2,position[1]-2, 4, 4))
            self.path = temp

    # Creating the grid for the pathfinder the grid is the entire level and only the barrier layer
    def create_grid(self, tmx_file_path):
        # Transforming tmx data to a 2d list
        matrix = tmx_to_grid(tmx_file_path)
        # Use the matrix to create a actual grid for the pathfinding algorithme
        grid = Grid(matrix=matrix)
        return grid

    # Checks for the collision of the Entity hitbox with the obstacles
    def collision_walls(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #Moving to the rigth
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0: #Moving to the left
                        self.hitbox.left = sprite.hitbox.right    

                    return sprite       

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
                if self.distance(object.rect.center)>= self.detection_range:
                    continue
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
    def get_direction (self, point):
        # Transforming the enemy and player position into a vector
        enemy_location = pygame.math.Vector2(self.rect.center)
        target_location = pygame.math.Vector2(point)

        # Getting the vector from the enemy to the player
        direction = target_location-enemy_location

        return direction

    # A function updates the vision of the enemy and returns if is sees anything special
    def looking_around(self,player):
        # Updating the position of the sensory lines
        self.update_line_positions(player)
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
    def update_line_positions(self, player):
        starting_position = self.rect.center
        self.sensory_lines = []
        player_angle = math.atan2(( player.rect.centery- starting_position[1]),(player.rect.centerx - starting_position[0]))
        # Calculate coordinates for each endpoint
        for i in range(int(self.amount_of_sensory_lines/2)):
            # For the positive angle for the direct line to the player
            # Getting the point from the unit circle
            angle = player_angle + (i * (math.pi/4)/ (self.amount_of_sensory_lines/2))
            x = self.detection_range * math.cos(angle)
            y = self.detection_range * math.sin(angle)
            # Moving the point to the correct position compared to center of the enemy(starting point)
            endpoint_x = starting_position[0] + x
            endpoint_y = starting_position[1] + y
            # Adding the lines to the list.
            self.sensory_lines.append(((starting_position[0], starting_position[1]), (endpoint_x, endpoint_y), self.no_detection_colour))

            # For the negative Angle for the direct line to the player
            angle =  player_angle - (i * (math.pi/4) / (self.amount_of_sensory_lines/2))
            # Getting the point from the unit circle
            x = self.detection_range * math.cos(angle)
            y = self.detection_range * math.sin(angle)
            # Moving the point to the correct position compared to center of the enemy(starting point)
            endpoint_x = starting_position[0] + x
            endpoint_y = starting_position[1] + y
            # Adding the lines to the list.
            self.sensory_lines.append(((starting_position[0], starting_position[1]), (endpoint_x, endpoint_y), self.no_detection_colour))

    def update(self,dt, player):
        pass