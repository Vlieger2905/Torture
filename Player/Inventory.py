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

        # Aditional functionality for the buttons
        self.selected_item = None
        self.previous_item_position = None
        self.clicked = False
        self.mouse_button = None

        # Defining the buttons of the inventory slot.
        i = 0
        j = 0
        for item in self.inventory_items:
            # Creating the positions of the buttons
            item_position_x = self.inventory_items_first_position[0] + i * self.inventory_items_distance
            item_position_y = self.inventory_items_first_position[1] + j * self.inventory_items_distance
            # Creating the Buttons and if there is already an item in the slot the buttons get the corresponding image.
            if item is not None:
                self.buttons.append(Inventory_button.Inventory_Button((item_position_x,item_position_y), item.image, (48,48)))
            else:
                self.buttons.append(Inventory_button.Inventory_Button((item_position_x,item_position_y), None, (48,48)))
            i += 1
            if i == 9:
                i = 0
                j += 1
        
    def update(self, clock):
        last_time = pygame.time.get_ticks()
        # Resetting every inventory button to be not pressed
        for button in self.buttons:
            button.pressed = False
        while True:
            last_time,dt = calculate_dt(last_time)
            pygame_events = pygame.event.get()
            for event in pygame_events:
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

            # Blitting the surface on the screen
            self.screen.blit(self.surface, (0,0))

            # Drawing the buttons
            for button in self.buttons:
                button.draw(self.screen)

            # Checking for button presses and makes the results of pressing buttons after eachother happen.
            self.handle_events(pygame_events)

            clock.tick(30)
            pygame.display.update()

    # Function to add items to the inventory in the next available slot
    def add_item(self, item_name):
        # Creating a instance of the correct item
        for item in self.all_items:
            if item_name == item.name:
                item_to_add = item
                continue
        # Putting the item in the next empty slot in the inventory
        for i in range(len(self.inventory_items)):
            if self.inventory_items[i] is None:
                self.inventory_items[i] = item_to_add
                item_to_add = None

    # Function to handle the events and actions within the inventory
    def handle_inventory_clicks(self, selected_button):
        if selected_button is not None:
            if self.mouse_button == "Left click":
                clicked_index = self.buttons.index(selected_button)

                # No item is selected, so select the clicked item
                if self.selected_item is None:
                    if clicked_index != self.previous_item_position:
                        self.previous_item_position = clicked_index
                        self.selected_item = self.inventory_items[clicked_index]
                    
                    else:
                        # Clicked on the same slot again, deselect the item
                        self.selected_item = None
                        self.previous_item_position = None
                        self.buttons[clicked_index].pressed = False
                    
                
                # An item is already selected
                else:
                    if clicked_index == self.previous_item_position:
                        # Clicked on the same slot again, deselect the item
                        self.selected_item = None
                        self.previous_item_position = None
                        self.buttons[clicked_index].pressed = False
                    else:
                        # Clicked on a different slot, move the item
                        self.inventory_items[clicked_index] = self.selected_item
                        self.inventory_items[self.previous_item_position] = None
                        self.previous_item_position = None
                        self.selected_item = None
                        self.buttons[clicked_index].pressed = False


    def handle_events(self, pygame_events):
        # Checking if a button gets pressed
        selected_button, self.mouse_button = self.check_events_inventory(pygame_events)
        self.handle_inventory_clicks(selected_button)  

    def check_events_inventory(self, events):
        selected_button = None
        mouse_button = None

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_button = "Left click"
                for button in self.buttons:
                    button.handle_event(event)

                    if button.pressed:
                        selected_button = button
                        for item in self.buttons:
                            item.pressed = (item == button)

        return selected_button, mouse_button
    