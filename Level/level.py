import pygame,sys,os
from pygame.sprite import Group
from Game import settings
from .tile import *
from Player import player
from debug import *
from .Camera import *
from .loading_tmx_file import *
from .load_obj import *

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
        self.exit = pygame.sprite.Group()
        self.exit_points = pygame.sprite.Group()
        # Getting the sprite details out of the tmx file creating them
        self.tmx_file = self.get_files_by_extension(level_map, [".tmx"])
        self.tmx_data = load_tmx(self.tmx_file)
        # Creating the exit points and hitboxes on the map
        get_exit(self.tmx_data, self.exit_points)
        # Creating all the tiles in the tmx file Except the background that is a image
        create_tiles(self.tmx_data, [self.visible_sprites, self.obstacle_sprites])

        # Creating player
        entry_point = get_spawnpoint(self.tmx_data, entry_point, level_map)
        self.player = player.Player(entry_point, [self.visible_sprites], self.obstacle_sprites, self.exit_points)

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

    def run(self, dt, clock):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            self.display_surface.fill('white')
            self.visible_sprites.custom_draw(self.player)
            self.visible_sprites.update(dt)
            debug(self.player.rect.topleft)
            pygame.display.update()
            clock.tick(settings.targetFPS)
