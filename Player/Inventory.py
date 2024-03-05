import pygame , math, sys
from Game.settings import *
from Game.dt import calculate_dt
from Game.Classes import Inventory_button

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
        self.inventory_items = [None] * 45
        self.inventory_items_first_position = (556,296)
        self.inventory_items_distance = 64
        self.inventory_size = 45
        self.buttons = []

        # Defining the buttons of the inventory slot.
        i = 0
        j = 0
        for item in self.inventory_items:
            # Creating the positions of the buttons
            item_position_x = self.inventory_items_first_position[0] + i * self.inventory_items_distance
            item_position_y = self.inventory_items_first_position[1] + j * self.inventory_items_distance
            # Creating the Buttons and if there is already an item in the slot the buttons get the corresponding image.
            if item is not None:
                self.buttons.append(Inventory_button.Inventory_Button((item_position_x,item_position_y), item.image, (self.inventory_size, self.inventory_size)))
            else:
                self.buttons.append(Inventory_button.Inventory_Button((item_position_x,item_position_y), None, (self.inventory_size, self.inventory_size)))
            i += 1
            if i == 9:
                i = 0
                j += 1
        
    def update(self, clock):
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
            
            # Updating the buttons to display the correct image if a item is added/changed/removed
            for i in range(len(self.inventory_items)):
                if self.inventory_items[i] != None:
                    self.buttons[i].image = self.inventory_items[i].image
                else:
                    self.buttons[i].image = None
            # Drawing the buttons
            for button in self.buttons:
                button.draw(self.surface)
            
            # Blitting the surface on the screen
            self.screen.blit(self.surface, (0,0))
            clock.tick()
            pygame.display.update()

    # Function to add items to the inventory in the next available slot
    def add_item(self, item_name):
        for item in self.all_items:
            if item_name == item.name:
                item_to_add = item
                continue
        for i in range(len(self.inventory_items)):
            if self.inventory_items[i] is None:
                self.inventory_items[i] = item_to_add
                item_to_add = None




