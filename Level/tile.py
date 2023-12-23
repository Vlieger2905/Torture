import pygame
import pygame.sprite
from Game import settings

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups) -> None:
        super().__init__(groups)
# Loading the image and making the rectangle
        self.image = pygame.image.load('Sprites\Wall Grass.png').convert_alpha()
        # Scale the image to 32x32 pixels
        self.image = pygame.transform.scale(self.image, (settings.Tilesize, settings.Tilesize))
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,0)

class Wall(pygame.sprite.Sprite):
    def __init__(self, position, groups) -> None:
        super().__init__(groups)
# Loading the image and making the rectangle
        self.image = pygame.image.load('Sprites\Ground Tiles\Cobble road lighter2.png').convert_alpha()
        # Scale the image to 32x32 pixels
        self.image = pygame.transform.scale(self.image, (settings.Tilesize, settings.Tilesize))
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,0)

class Grass(pygame.sprite.Sprite):
    def __init__(self, position, groups) -> None:
        super().__init__(groups)
# Loading the image and making the rectangle
        self.image = pygame.image.load('Sprites\Ground Tiles\Grass tile 32.png').convert_alpha()
        # Scale the image to 32x32 pixels
        self.image = pygame.transform.scale(self.image, (settings.Tilesize, settings.Tilesize))
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,0)
