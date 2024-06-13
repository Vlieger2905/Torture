import pygame, math, random

class Example():
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

            # Maximum value the player has at the moment for the combat
            self.max_health = self.Vitality * math.sqrt(self.Vitality) + 20
            self.max_stamina = math.sqrt(self.Vitality) + 5
            self.max_mana = math.sqrt(self.Mind) + 5
            self.max_sanity = math.sqrt(self.Fortitude)

            # Current value the player has
            self.health_points = self.max_health
            self.stamina_points = self.max_stamina
            self.mana_points = self.max_mana
            self.sanity = self.max_sanity
            # damage resistance. 1 = no absorption. A lower numbers means less damage taken
            self.resistance = 1
            self.status = []

            # Skills of the Enemy
            self.skills = []

            #  Equipement of the enemy
            self.equipement = [""]
            
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

        # Maximum value the player has at the moment for the combat
        self.max_health = self.Vitality * math.sqrt(self.Vitality) + 20
        self.max_stamina = math.sqrt(self.Vitality) + 5
        self.max_mana = math.sqrt(self.Mind) + 5
        self.max_sanity = math.sqrt(self.Fortitude)

        # Current value the player has
        self.health_points = self.max_health
        self.stamina_points = self.max_stamina
        self.mana_points = self.max_mana
        self.sanity = self.max_sanity
        # Damage absorption 1 = no absorption. A lower numbers means less damage taken
        self.resistance = 0.6


        self.status = []

        # Skills of the Enemy
        self.skills = []

        #  Equipement of the enemy
        self.equipement = [""]

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

        # Maximum value the player has at the moment for the combat
        self.max_health = self.Vitality * math.sqrt(self.Vitality) + 20
        self.max_stamina = math.sqrt(self.Vitality) + 5
        self.max_mana = math.sqrt(self.Mind) + 5
        self.max_sanity = math.sqrt(self.Fortitude)

        # Current value the player has
        self.health_points = self.max_health
        self.stamina_points = self.max_stamina
        self.mana_points = self.max_mana
        self.sanity = self.max_sanity
        # Damage absorption 1 = no absorption. A lower numbers means less damage taken
        self.resistance = 1


        self.status = []
        
        # Skills of the enemy
        self.skills = []

        #  Equipement of the enemy
        self.equipement = [""]

        

        
