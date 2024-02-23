import pygame , math, sys
from Game.settings import *
from Game.dt import calculate_dt


item = []

class Inventory:
    def __init__(self):
        # Loading the image of the inventory background
        self.image_background = pygame.image.load("Sprites\Inventory\Inventory1.0 scaled up.png").convert_alpha()
        # self.image_background = pygame.transform.smoothscale(self.image_background, (WIDTH, HEIGTH))
        # Loading teh display
        self.screen = pygame.display.get_surface()
        # Creating a independend surface for the inventory to blit when all items are displayed with the background.
        self.surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        # Defining all the equiped items of the player
        self.headwear = None
        self.headwear_position = None
        self.chestplate = None
        self.chestplate_position = None
        self.pants = None
        self.pants_position = None
        self.boots = None
        self.boots_position = None
        self.necklace = None
        self.necklace_position = None
        self.ring = None
        self.ring_position = None
        self.left_hand = None
        self.left_hand_position = None
        self.right_hand = None
        self.right_hand_position = None

        # Defining the list with the inventory items inside:
        self.inventory_items = []

    def draw(self, clock):
        last_time = pygame.time.get_ticks()
        while True:
            last_time,dt = calculate_dt(last_time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                    return last_time
            self.surface.blit(self.image_background, (0,0))
            self.screen.blit(self.surface, (0,0))
            clock.tick()
            pygame.display.update()

    

