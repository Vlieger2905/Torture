import pygame
from Game import settings
from .modifiers import *

class Player(pygame.sprite.Sprite):
# Initializing the player
    def __init__(self,position, groups, obstacle_sprites, exits):
        super().__init__(groups)
        self.image = pygame.image.load('Sprites\\Player\\Village boy #1.png').convert_alpha()
        # Scale the image to 32x32 pixels
        self.image = pygame.transform.scale(self.image, (settings.Tilesize, settings.Tilesize))
        self.rect  = self.image.get_rect(topleft = position)
        # Setting the player hitbox
        self.hitbox = self.rect.inflate(-10*settings.scale,-10*settings.scale)
        # Variables used within the player class
        self.direction = pygame.math.Vector2()
        self.base_speed = base_speed
        self.obstacle_sprites = obstacle_sprites
        self.exit_rects = exits 
        self.first_frame = True

        # # Player stats
        # level = initial_stats.get("level", 1)

        # # Player innate stats
        # self.Might = initial_stats.get("Might", 14)
        # self.Agility = initial_stats.get("Agility", 7)
        # self.Mind = initial_stats.get("Mind", 3)
        # self.Vitality = initial_stats.get("Vitality", 12)
        # self.Fortitude = initial_stats.get("Fortitude", 6)

        # # Combat proficiency
        #     # Melee
        # self.Sword_proficiency = initial_stats.get("Sword_proficiency", 1)
        # self.Lance_proficiency = initial_stats.get("Lance_proficiency", 1)
        # self.Axe_proficiency = initial_stats.get("Axe_proficiency", 1)
        # self.Maul_proficiency = initial_stats.get("Maul_proficiency", 1)
        # self.Dagger_proficiency = initial_stats.get("Dagger_proficiency", 1)
        # self.Unarmed_proficiency = initial_stats.get("Unarmed_proficiency", 1)
        #     # Ranged
        # self.Bow_proficiency = initial_stats.get("Bow_proficiency", 1)
        # self.Crossbow_proficiency = initial_stats.get("Crossbow_proficiency", 1)
        # self.Thrown_proficiency = initial_stats.get("Thrown_proficiency", 1)
        # self.Firearms_proficiency = initial_stats.get("Firearms_proficiency", 1)

        #     # Mind Magic
        # self.Light_proficiency = initial_stats.get("Light_proficiency", 0)
        # self.Dark_proficiency = initial_stats.get("Dark_proficiency", 0)
        # self.Soul_proficiency = initial_stats.get("Soul_proficiency", 0)
        # self.Spirit_proficiency = initial_stats.get("Spirit_proficiency", 0)

        #     # Fortitude Magic
        # self.Fire_proficiency = initial_stats.get("Fire_proficiency", 0)
        # self.Earth_proficiency = initial_stats.get("Earth_proficiency", 0)
        # self.Water_proficiency = initial_stats.get("Water_proficiency", 0)
        # self.Air_proficiency = initial_stats.get("Air_proficiency", 0)
        # self.Plants_proficiency = initial_stats.get("Plants_proficiency", 0)
        # self.Lightning_proficiency = initial_stats.get("Lightning_proficiency", 0)


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
    
    def move(self, dt):
        # If the player is moving making sure that the velocity stays the same and that the player is not moving faster when moving diagonally
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        # Moving the player
        speed =  base_speed
        move_vector = self.direction * speed * dt
        self.hitbox.x +=move_vector.x
        self.collision('horizontal')
        self.hitbox.y +=move_vector.y
        self.collision('vertical')
        self.rect.center=self.hitbox.center

    # Checks for the collision of the player hitbox with the obstacles
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #Moving to the rigth
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #Moving to the left
                        self.hitbox.left = sprite.hitbox.right           

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #Moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #Moving up
                        self.hitbox.top = sprite.hitbox.bottom

    # checks for the collision between the player hitbox and the exit hitboxes
    def collision_exit(self):
        for obj in self.exit_rects:
                if obj.hitbox.colliderect(self.hitbox):
                    return obj.name

    def update(self,dt):
        if self.first_frame is False:
            self.input()
            self.move(dt)
        else:
            self.first_frame = False