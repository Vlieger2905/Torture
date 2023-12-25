import pygame,sys,os
from pygame.sprite import Group
from Game import settings
from .tile import *
from Player import player
from debug import *
from .Camera import *
from .loading_tmx_file import *

class Level:
    def __init__(self, level_map, entry_point):
# Getting the display surface
        self.display_surface = pygame.display.get_surface()     
# Sprite group setup
        floor_image = self.get_files_by_extension(level_map, [".png"])
        
        # Sprites that can be drawn on the screen
        self.visible_sprites = CameraGroup(floor_image)
        # Sprites that interact with the player
        self.obstacle_sprites = pygame.sprite.Group()
        # Getting the sprite details out of the tmx file creating them
        tmx_file = self.get_files_by_extension(level_map, [".tmx"])
        tmx_data = load_tmx(tmx_file)
        # Creating all the tiles in the tmx file Except the background that is a image
        create_tiles(tmx_data, [self.visible_sprites, self.obstacle_sprites])
        # Looping through the objects in the tmx files to find the corresponding point and the coordinates thereof to spawn in the player in the correct position
        for obj in tmx_data.objects:
            if obj.name == entry_point:
                entry_point = (obj.x* settings.scale, obj.y* settings.scale)
                break 
        if entry_point is None or not isinstance(entry_point, tuple):
            raise ValueError(f"No entry point found for name '{entry_point}' in the '{level_map}' folder.")    
        # Creating player
        self.player = player.Player(entry_point, [self.visible_sprites], self.obstacle_sprites)

    def get_files_by_extension(self, folder_path, extensions):
        matching_files = []

        # Ensure folder path ends with a separator
        folder_path = os.path.join(folder_path, "")

        # Get a list of all items in the folder
        items = os.listdir(folder_path)

        for item in items:
            item_path = os.path.join(folder_path, item)

            # Check if the item is a file and has a matching extension
            if os.path.isfile(item_path):
                _, extension = os.path.splitext(item)
                if extension.lower() in extensions:
                    relative_path = os.path.relpath(item_path, folder_path)
                    combined_path = os.path.join(folder_path, relative_path)
                    matching_files.append(combined_path)

        return matching_files[0]

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
                    self.player = player.Player((x,y), [self.visible_sprites, self.obstacle_sprites])

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
            debug(self.player.rect.topleft)
            pygame.display.update()
            clock.tick(settings.targetFPS)
