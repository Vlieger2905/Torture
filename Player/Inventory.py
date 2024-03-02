import pygame , math, sys
from Game.settings import *
from Game.dt import calculate_dt

class Inventory:
    def __init__(self, item_list):
        # Loading the image of the inventory background
        self.image_background = pygame.image.load("Sprites\\Inventory\\Inventory1.0 scaled up.png").convert_alpha()
        # Loading the display
        self.screen = pygame.display.get_surface()
        # Creating a independend surface for the inventory to blit when all items are displayed with the background.
        self.surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        # A list of all the possible items in the game
        self.all_items = item_list
        # Defining all the equiped items of the player
        self.headwear = None
        self.headwear_position = (448,224)
        self.chestplate = None
        self.chestplate_position = (448,320)
        self.pants = None
        self.pants_position = (448,416)
        self.boots = None
        self.boots_position = (448,512)
        self.necklace = None
        self.necklace_position = (180,224)
        self.ring = None
        self.ring_position = (180,320)
        self.left_hand = None
        self.left_hand_position = (180,416)
        self.right_hand = None
        self.right_hand_position = (180,512)

        # Defining the list with the inventory items inside:
        self.inventory_items = []
        self.inventory_items_first_position = (556,296)
        self.inventory_items_distance = 64
        self.inventory_size = 45
        
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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return last_time
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    # Adding a item to the inventory list
                    # Testing purposes only
                    self.add_item("Iron Sword")
                    # Deleting items that have been added above the inv size
                    while len(self.inventory_items) > self.inventory_size:
                        del self.inventory_items[-1]

            # Blitting the background image on the surface
            self.surface.blit(self.image_background, (0,0))
            # Blitting the items in the inventory slots on the surface
            i = 0
            j = 0
            for item in self.inventory_items:
                item_position_x = self.inventory_items_first_position[0] + i * self.inventory_items_distance
                item_position_y = self.inventory_items_first_position[1] + j * self.inventory_items_distance
                item.draw(self.surface, (item_position_x, item_position_y))
                i += 1
                if i == 9:
                    i = 0
                    j += 1
            # Blitting the surface on the screen
            self.screen.blit(self.surface, (0,0))
            clock.tick()
            pygame.display.update()

    def add_item(self, item_name):
        for item in self.all_items:
            if item_name == item.name:
                self.inventory_items.append(item)


