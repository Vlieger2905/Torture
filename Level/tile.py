import pygame
import pygame.sprite
from Game import settings

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, image, groups,layer_name) -> None:
        super().__init__(groups)
        self.layer_name = layer_name
        # Loading the image and making the rectangle
        self.image = image
        # Scale the image from 32x32 pixels to correct size
        self.image = pygame.transform.scale(self.image, (settings.Tilesize, settings.Tilesize))
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,0)

def create_tiles(tmx_data, sprite_group):
    # cycle through all layers
    for layer in tmx_data.layers:
        if layer.name == "Ground":
            pass
        elif layer.name == "Barrier":
            for x, y, image in layer.tiles():
                    position = ((x * settings.Tilesize), (y * settings.Tilesize))
                    Tile(position, image, sprite_group[1], layer.name)
        else:
            if hasattr(layer, 'data') and layer.visible:
                for x, y, image in layer.tiles():
                    position = ((x * settings.Tilesize), (y * settings.Tilesize))
                    Tile(position, image, sprite_group[0], layer.name)

    for obj in tmx_data.objects:
        pos = obj.x,obj.y
        if obj.type in ('Building', 'Vegetation'):
            Tile(pos = pos, surf = obj.image, groups = sprite_group)









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
