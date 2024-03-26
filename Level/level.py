import pygame,sys,os
from pygame.sprite import Group
from Game import settings
from Game import dt as detalTime
from Game.Menu.pauseMenu import *
from .tile import *
from Player import player
from debug import *
from .Camera import *
from .loading_tmx_file import *
from . import load_obj 
from .load_exit import load_exit

class Level:
    def __init__(self, level_map, entry_point, player):
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
        self.json_file = self.get_files_by_extension(level_map , [".json"])
        # Creating the exit points and hitboxes on the map
        load_obj.get_exit(self.tmx_data, self.exit_points)
        # Creating all the tiles in the tmx file Except the background that is a image
        create_tiles(self.tmx_data, [self.visible_sprites, self.obstacle_sprites])

        # Creating player
        entry_point = load_obj.get_spawnpoint(self.tmx_data, entry_point, level_map)
        self.player = player
        self.player.spawn(entry_point,self.obstacle_sprites, self.exit_points)
        # Add player to visible_sprites group
        self.visible_sprites.add(self.player)

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

    def run(self, clock):
        last_time = pygame.time.get_ticks()
        while True:
            last_time,dt = detalTime.calculate_dt(last_time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit", self.player
                
                # What to do when a key gets pressed
                if event.type == pygame.KEYDOWN:
                    # Running the pause menu
                    if event.key == pygame.K_ESCAPE:
                        pauseMenu, last_time = pause_menu(self.display_surface, clock, last_time)
                        # Continue playing
                        if pauseMenu == "play":
                            continue
                        # Exit the game
                        elif pauseMenu == "quit":
                            return "quit", self.player
                        # Returning to the main menu
                        elif pauseMenu == "return to main menu":
                            return "main menu", self.player

                        else:
                            pass
                    # Open the inventory
                    if event.key == pygame.K_i:
                        last_time = self.player.inventory.update(clock)
                        # If, when in the inventory the player pressed the X button quit the game
                        if last_time == "quit":
                            return "quit", self.player
                        

            self.display_surface.fill('white')
            self.visible_sprites.custom_draw(self.player)
            self.visible_sprites.update(dt)

            # Checking if the player collides with a exit point on the map and the returns the next level and the point the player should spawn
            exit = self.player.collision_exit()
            if exit is not None:
                next_level = load_exit(self.json_file, exit)
                return next_level, self.player

            # debug(self.player.world_speed)
            clock.tick(settings.FPS)
            pygame.display.update()
