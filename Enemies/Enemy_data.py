import pygame, math, random

class Slime():
    def __init__(self, level) -> None:
        # Information for display
        self.image_path = "Sprites//Enemies//Slime.png"
        self.image_loaded = pygame.image.load("Sprites//Enemies//Slime.png")
        self.combat_size = (100,100)
        self.type = "enemy"
        # Stats of the Enemy
        self.level = level

        self.Might = 8 + 3 * self.level
        self.Agility = 3 + 2 * self.level
        self.Mind = 1 + 1 * self.level
        self.Vitality = 9 + 4 * self.level
        self.Fortitude = 4 + 2 * self.level

        # Skills of the Enemy
        self.skills = []

class Skeleton():
    def __init__(self, level) -> None:
        self.image_path = "Sprites//DEV resources//SpriteTest.png"
        self.image_loaded = pygame.image.load("Sprites//DEV resources//SpriteTest.png")
        self.combat_size = (100,100)
        self.type = "enemy"
        # Stats of the enemy
        self.level = level
        self.Might = 8 + 3 * self.level
        self.Agility = 3 + 2 * self.level
        self.Mind = 1 + 1 * self.level
        self.Vitality = 9 + 4 * self.level
        self.Fortitude = 4 + 2 * self.level
        
        # Skills of the enemy
        self.skills = []

        
