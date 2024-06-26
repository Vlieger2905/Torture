import pygame, math
from Game import settings
from .modifiers import *
from .Inventory import Inventory

class Player(pygame.sprite.Sprite):
# Initializing the player
    def __init__(self, stats, item_list, player_items):
        super().__init__()
        # super().__init__(groups)
        self.image = pygame.image.load('Sprites\\Player\\Village boy #1.png').convert_alpha()
        # Scale the image to 32x32 pixels
        self.image = pygame.transform.scale(self.image, (settings.Tilesize, settings.Tilesize))
        # Creating the rect of the player
        self.rect  = self.image.get_rect()
        # Setting the player hitbox
        self.hitbox = self.rect.copy()
        # Rescaling the hitbox of the player to fit the player character
        self.hitbox= self.hitbox.inflate(-(self.hitbox.width * 0.45),-(self.hitbox.height * 0.8))
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.centery = self.rect.bottom + (self.rect.height * 0.05)
        # Variables used within the player class
        self.direction = pygame.math.Vector2()
        self.base_speed = base_speed
        self.world_speed = self.base_speed
        self.first_frame = True
        # Defining the player inventory
        self.inventory = Inventory(item_list, player_items)
        
    # loading the stats of the charachter into the playerclass
        
        # Player stats
        self.level = stats.get("level", 1)

        # Player innate stats
        self.Might = stats.get("Might", 14)
        self.Agility = stats.get("Agility", 7)
        self.Mind = stats.get("Mind", 3)
        self.Vitality = stats.get("Vitality", 12)
        self.Fortitude = stats.get("Fortitude", 6)

        # Combat proficiency
            # Melee
        self.Sword_proficiency = stats.get("Sword_proficiency", 1)
        self.Lance_proficiency = stats.get("Lance_proficiency", 1)
        self.Axe_proficiency = stats.get("Axe_proficiency", 1)
        self.Maul_proficiency = stats.get("Maul_proficiency", 1)
        self.Dagger_proficiency = stats.get("Dagger_proficiency", 1)
        self.Unarmed_proficiency = stats.get("Unarmed_proficiency", 1)
            # Ranged
        self.Bow_proficiency = stats.get("Bow_proficiency", 1)
        self.Crossbow_proficiency = stats.get("Crossbow_proficiency", 1)
        self.Thrown_proficiency = stats.get("Thrown_proficiency", 1)
        self.Firearms_proficiency = stats.get("Firearms_proficiency", 1)

            # Mind Magic
        self.Light_proficiency = stats.get("Light_proficiency", 0)
        self.Dark_proficiency = stats.get("Dark_proficiency", 0)
        self.Soul_proficiency = stats.get("Soul_proficiency", 0)
        self.Spirit_proficiency = stats.get("Spirit_proficiency", 0)

            # Fortitude Magic
        self.Fire_proficiency = stats.get("Fire_proficiency", 0)
        self.Earth_proficiency = stats.get("Earth_proficiency", 0)
        self.Water_proficiency = stats.get("Water_proficiency", 0)
        self.Air_proficiency = stats.get("Air_proficiency", 0)
        self.Plants_proficiency = stats.get("Plants_proficiency", 0)
        self.Lightning_proficiency = stats.get("Lightning_proficiency", 0)

    # Spawning the player in a new level
    def spawn(self,spawn_position, obstacle_sprites, exits):
        self.hitbox.x, self.hitbox.y = spawn_position
        self.aligment() 
        self.obstacle_sprites = obstacle_sprites
        self.exit_rects = exits 
        self.first_frame = True    
    # Retrieving the player stats to save
    def get_stats(self):
        stats = {
            'level': self.level,

            # Player innate stats
            'Might': self.Might,
            'Agility': self.Agility,
            'Mind': self.Mind,
            'Vitality': self.Vitality,
            'Fortitude': self.Fortitude,

            # Combat proficiency
            # Melee
            'Sword_proficiency': self.Sword_proficiency,
            'Lance_proficiency': self.Lance_proficiency,
            'Axe_proficiency': self.Axe_proficiency,
            'Maul_proficiency': self.Maul_proficiency,
            'Dagger_proficiency': self.Dagger_proficiency,
            'Unarmed_proficiency': self.Unarmed_proficiency,
            # Ranged
            'Bow_proficiency': self.Bow_proficiency,
            'Crossbow_proficiency': self.Crossbow_proficiency,
            'Thrown_proficiency': self.Thrown_proficiency,
            'Firearms_proficiency': self.Firearms_proficiency,

            # Mind Magic
            'Light_proficiency': self.Light_proficiency,
            'Dark_proficiency': self.Dark_proficiency,
            'Soul_proficiency': self.Soul_proficiency,
            'Spirit_proficiency': self.Spirit_proficiency,

            # Fortitude Magic
            'Fire_proficiency': self.Fire_proficiency,
            'Earth_proficiency': self.Earth_proficiency,
            'Water_proficiency': self.Water_proficiency,
            'Air_proficiency': self.Air_proficiency,
            'Plants_proficiency': self.Plants_proficiency,
            'Lightning_proficiency': self.Lightning_proficiency
        }
        return stats
    # Retreiving the player item to save
    def get_items(self):
        items ={
        "headwear": self.inventory.headwear.name if self.inventory.headwear else "",
        "chestplate": self.inventory.chestplate.name if self.inventory.chestplate else "",
        "pants": self.inventory.pants.name if self.inventory.pants else "",
        "boots": self.inventory.boots.name if self.inventory.boots else "",
        "necklace": self.inventory.necklace.name if self.inventory.necklace else "",
        "ring": self.inventory.ring.name if self.inventory.ring else "",
        "left_hand": self.inventory.left_hand.name if self.inventory.left_hand else "",
        "right_hand": self.inventory.right_hand.name if self.inventory.right_hand else "",
        "inventory_items" : [item.name if item else "" for item in self.inventory.inventory_items]
    }

        return items
    # Getting the input for the player movement
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.y = 0
        self.direction.x = 0
        # Vertical movement of the player input
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        # Horizontal movement of the player input
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        
        if keys[pygame.K_b]:
            self.Agility +=20
    # Move the player
    def move(self, dt):
        # If the player is moving making sure that the velocity stays the same and that the player is not moving faster when moving diagonally
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        # Moving the player
        self.world_speed =  self.base_speed + self.Agility
        move_vector = self.direction * self.world_speed * dt
        self.hitbox.x +=move_vector.x
        self.collision_walls('horizontal')
        self.hitbox.y +=move_vector.y
        self.collision_walls('vertical')

    # Checks for the collision of the player hitbox with the obstacles
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

    # checks for the collision between the player hitbox and the exit hitboxes
    def collision_exit(self):
        for obj in self.exit_rects:
                if obj.hitbox.colliderect(self.hitbox):
                    return obj.name

    def aligment(self):
        self.rect.centerx = self.hitbox.centerx
        self.rect.centery = self.hitbox.centery - (self.rect.height * 0.3)

    def update(self,dt, just_ignore_this_variable):
        if self.first_frame is False:
            self.input()
            self.move(dt)
            self.aligment()
        else:
            self.first_frame = False
            