import pygame
import pygame.sprite
from pygame.sprite import Group
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
