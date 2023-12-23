import pygame,sys
from pygame.sprite import Group
from pytmx.util_pygame import load_pygame
from Game import settings
from .tile import *
from Player import player
from debug import *

class Level:
    def __init__(self):
# Getting the display surface
        self.display_surface = pygame.display.get_surface()     
# Sprite group setup
        # Sprites that can be drawn on the screen
        self.visible_sprites = CameraGroup()
        # Sprites that interact with the player
        self.obstacle_sprites = pygame.sprite.Group()
# Creating player
        self.player = player.Player((5240,3262), [self.visible_sprites], self.obstacle_sprites)
        # self.create_map()

    def create_map(self):
        for row_index, row in enumerate(settings.WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * settings.Tilesize
                y = row_index * settings.Tilesize
                if (col == 'x'):
                    Wall((x,y), [self.visible_sprites, self.obstacle_sprites]) 
                if (col == ' '):
                    Grass((x,y), [self.visible_sprites])
                if (col == 'p'):
                    self.player = player.Player((x,y), [self.visible_sprites], self.obstacle_sprites)


    def run(self, dt, clock):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    print("Escape")
                    break
            self.display_surface.fill('white')
            self.visible_sprites.custom_draw(self.player)
            self.visible_sprites.update(dt)
            debug(self.player.rect.center)
            pygame.display.update()
            clock.tick(settings.targetFPS)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
# general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.display_WIDTH = self.display_surface.get_size()[0] // 2
        self.display_HEIGTH = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

# Creating the floor
        floor_map = pygame.image.load('Map Data\\Test Map\\testMap.png').convert()
        floor_map_size = floor_map.get_size()
        self.floor_surface = pygame.transform.scale(floor_map, (floor_map_size[0] / settings.sprite_size * settings.Tilesize,floor_map_size[1] / settings.sprite_size * settings.Tilesize ))
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))
# Drawing the sprites in the group
    def custom_draw(self,player):
        self.offset.x = player.rect.centerx - self.display_WIDTH
        self.offset.y = player.rect.centery - self.display_HEIGTH

# Drawing the floor
        floor_offset = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
