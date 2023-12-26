import pygame,sys,os
from Game import settings
from debug import *

def get_spawnpoint(tmx_data,entry_point, level_map):
    # Looping through the objects in the tmx files to find the corresponding point and the coordinates thereof to spawn in the player in the correct position
        for obj in tmx_data.objects:
            if obj.name == entry_point:
                entry_point = (obj.x* settings.scale, obj.y* settings.scale)
                return entry_point
                break 
        if entry_point is None or not isinstance(entry_point, tuple):
            raise ValueError(f"No entry point found for name '{entry_point}' in the '{level_map}' folder.")
        

def get_exit(tmx_data, exit_group):
    for obj in tmx_data.objects:
        if obj.type == "Exitpoint":
             Exit(exit_group, obj)

class Exit(pygame.sprite.Sprite):
    def __init__(self, groups, obj):
        super().__init__(groups)
        self.name = obj.name
        self.y = obj.y * settings.scale
        self.x = obj.x * settings.scale
        self.width = obj.width * settings.scale
        self.height = obj.height * settings.scale
        self.colour=(0,0,255)
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
