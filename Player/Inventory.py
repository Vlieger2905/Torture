import pygame , math, sys
from Game.settings import *
from Game.dt import calculate_dt
from Game.Classes import Inventory_button
from SaveFiles import Save_Functions

class Inventory:
    def __init__(self, item_list, loaded_items):
        # Loading the image of the inventory background
        self.image_background = pygame.image.load("Sprites\\Inventory\\Inventory1.0 scaled up.png").convert_alpha()
        # Loading the display
        self.screen = pygame.display.get_surface()
        # Creating a independend surface for the inventory to blit when all items are displayed with the background.
        self.surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        # A list of all the possible items in the game
        self.all_items = item_list
        # Defining all the equiped items of the player
        self.headwear = loaded_items.get("headwear", "")
        self.headwear_position = (448,224)
        self.chestplate = loaded_items.get("chestplate", "")
        self.chestplate_position = (448,320)
        self.pants = loaded_items.get("pants", "")
        self.pants_position = (448,416)
        self.boots = loaded_items.get("boots", "")
        self.boots_position = (448,512)
        self.necklace = loaded_items.get("necklace", "")
        self.necklace_position = (180,224)
        self.ring = loaded_items.get("ring", "")
        self.ring_position = (180,320)
        self.left_hand = loaded_items.get("left_hand", "")
        self.left_hand_position = (180,416)
        self.right_hand = loaded_items.get("right_hand", "")
        self.right_hand_position = (180,512)

        # Defining the list with the inventory items inside:
        self.inventory_items = self.load_inventory_items_boot(loaded_items.get( "inventory_items"))
        self.inventory_items_first_position = (556,296)
        self.inventory_items_distance = 64
        self.inventory_size = 45
        # Storing all the buttons of the inventory
        self.buttons = []
        self.equipment_buttons = []

        # Aditional functionality for the buttons
        self.selected_item = None
        self.previous_item_position = None
        self.clicked = False
        self.mouse_button = None
        self.selected_button_type = None
        self.previous_button_type = None

        # Defining the buttons of the inventory slot.
        i = 0
        j = 0
        for item in self.inventory_items:
            # Creating the positions of the buttons
            item_position_x = self.inventory_items_first_position[0] + i * self.inventory_items_distance
            item_position_y = self.inventory_items_first_position[1] + j * self.inventory_items_distance
            # Creating the Buttons and if there is already an item in the slot the buttons get the corresponding image.
            if item != "":
                self.buttons.append(Inventory_button.Inventory_Button((item_position_x,item_position_y), item.image, (48,48)))
            else:
                self.buttons.append(Inventory_button.Inventory_Button((item_position_x,item_position_y), None, (48,48)))
            i += 1
            if i == 9:
                i = 0
                j += 1
        
        # Defining the buttons of the equipment slots
        # If the item is has a image then the button gets that image if not the image is None
        headwear_image = self.headwear.image if hasattr(self.headwear, 'image') else None
        self.equipment_buttons.append(Inventory_button.Equipement_Button(self.headwear_position, "headwear", headwear_image))

        chestplate_image = self.chestplate.image if hasattr(self.chestplate, 'image') else None
        self.equipment_buttons.append(Inventory_button.Equipement_Button(self.chestplate_position, "chestplate", chestplate_image))

        pants_image = self.pants.image if hasattr(self.pants, 'image') else None
        self.equipment_buttons.append(Inventory_button.Equipement_Button(self.pants_position, "pants", pants_image))

        boots_image = self.boots.image if hasattr(self.boots, 'image') else None
        self.equipment_buttons.append(Inventory_button.Equipement_Button(self.boots_position, "boots", boots_image))

        necklace_image = self.necklace.image if hasattr(self.necklace, 'image') else None
        self.equipment_buttons.append(Inventory_button.Equipement_Button(self.necklace_position, "necklace", necklace_image))

        ring_image = self.ring.image if hasattr(self.ring, 'image') else None
        self.equipment_buttons.append(Inventory_button.Equipement_Button(self.ring_position, "ring", ring_image))

        left_hand_image = self.left_hand.image if hasattr(self.left_hand, 'image') else None
        self.equipment_buttons.append(Inventory_button.Equipement_Button(self.left_hand_position, "left_hand", left_hand_image))

        right_hand_image = self.right_hand.image if hasattr(self.right_hand, 'image') else None
        self.equipment_buttons.append(Inventory_button.Equipement_Button(self.right_hand_position, "right_hand", right_hand_image))

        

    def update(self, clock):
        last_time = pygame.time.get_ticks()
        # Resetting every inventory button/variable to be not pressed when booting the window again
        for button in self.buttons:
            button.pressed = False
        for button in self.equipment_buttons:
            button.pressed = False

        self.previous_item_position = None
        self.selected_item = None
        self.previous_button_type = None
        self.mouse_button = None

        # Starting the inventory loop
        while True:
            last_time,dt = calculate_dt(last_time)
            pygame_events = pygame.event.get()
            for event in pygame_events:
                # Quitting the game
                if event.type == pygame.QUIT:
                    return "quit"
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                    return last_time
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return last_time
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    # Adding a item to the inventory list
                    # Testing purposes only
                    self.add_item("Iron Sword")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                    # Adding a item to the inventory list
                    # Testing purposes only
                    self.add_item("Rusty Helmet")
                    
            
            # Blitting the background image on the surface
            self.surface.blit(self.image_background, (0,0))
            
            # Updating the buttons to display the correct image if a item is added/changed/removed
            for i in range(len(self.inventory_items)):
                if self.inventory_items[i] != "" and self.inventory_items[i] != None:
                    self.buttons[i].image = self.inventory_items[i].image
                else:
                    self.buttons[i].image = None
            
            # Updating the equipment slot button images
            for i in range(len(self.equipment_buttons)):
                if i == 0:
                    if self.headwear != "" and self.headwear != None:
                        self.equipment_buttons[i].image = self.headwear.image
                    else:
                        self.equipment_buttons[i].image = None

                if i == 1:    
                    if self.chestplate != "":
                        self.equipment_buttons[i].image = self.chestplate.image
                    else:
                        self.equipment_buttons[i].image = None
                if i == 2:    
                    if self.pants != "":
                        self.equipment_buttons[i].image = self.pants.image
                    else:
                        self.equipment_buttons[i].image = None
                if i == 3:    
                    if self.boots != "":
                        self.equipment_buttons[i].image = self.boots.image
                    else:
                        self.equipment_buttons[i].image = None
                if i == 4:    
                    if self.necklace != "":
                        self.equipment_buttons[i].image = self.necklace.image
                    else:
                        self.equipment_buttons[i].image = None
                if i == 5:    
                    if self.ring != "":
                        self.equipment_buttons[i].image = self.ring.image
                    else:
                        self.equipment_buttons[i].image = None
                if i == 6:    
                    if self.left_hand != "":
                        self.equipment_buttons[i].image = self.left_hand.image
                    else:
                        self.equipment_buttons[i].image = None
                if i == 7:    
                    if self.right_hand != "":
                        self.equipment_buttons[i].image = self.right_hand.image
                    else:
                        self.equipment_buttons[i].image = None




            # Blitting the surface on the screen
            self.screen.blit(self.surface, (0,0))

            # Drawing the buttons
            for button in self.buttons:
                button.draw(self.screen)
            # Drawing the equipement buttons
            for button in self.equipment_buttons:
                button.draw(self.screen)

            # Checking for button presses and makes the results of pressing buttons after eachother happen.
            self.handle_events(pygame_events)

            clock.tick(60)
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
            if self.inventory_items[i] == "":
                self.inventory_items[i] = item_to_add
                break

    # Function to handle the events and actions within the inventory
    def handle_inventory_clicks(self, selected_button):
        # Only do something when a button got pressed
        if selected_button is not None:
            # Do something when a inventory button has been pressed
            if self.selected_button_type == "inventory":
                if self.mouse_button == "Left click":
                    clicked_index = self.buttons.index(selected_button)

                    # No item is selected, so select the clicked item
                    if self.selected_item is None or self.selected_item == "":
                        # Select an item if none is selected
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
                        # Moving the item within the inventory
                        if self.previous_button_type == "inventory":
                            if clicked_index == self.previous_item_position:
                                # Clicked on the same slot again, deselect the item
                                self.selected_item = None
                                self.previous_item_position = None
                                self.buttons[clicked_index].pressed = False

                            elif self.buttons[clicked_index].image is not None:
                                temp_save_item = self.inventory_items[clicked_index]
                                self.inventory_items[clicked_index]  = self.selected_item
                                self.inventory_items[self.previous_item_position] = temp_save_item
                                self.previous_item_position = None
                                self.selected_item = None
                                self.buttons[clicked_index].pressed = False
                            
                            # Clicked on a different slot, move the item
                            else:
                                self.inventory_items[clicked_index] = self.selected_item
                                self.inventory_items[self.previous_item_position] = ""
                                self.previous_item_position = None
                                self.selected_item = None
                                self.buttons[clicked_index].pressed = False

                        # Moving the item for the equipement slot to the inventory
                        elif self.previous_button_type == "equipement":
                            # Check if the inventory slot that is now pressed is empty and if it is empty move it to there
                            if self.inventory_items[clicked_index] == "" or self.inventory_items[clicked_index] == None:
                                # Putting the selected item in a inventory slot as it is empty
                                self.inventory_items[clicked_index] = self.selected_item
                                self.buttons[clicked_index].pressed = False
                                self.selected_item = None
                                # Emtpying the item slot
                                if self.previous_item_position == 0:
                                    self.headwear = ""
                                elif self.previous_item_position == 1:
                                    self.chestplate = ""
                                elif self.previous_item_position == 2:
                                    self.pants = ""
                                elif self.previous_item_position == 3:
                                    self.boots = ""
                                elif self.previous_item_position == 4:
                                    self.necklace = ""
                                elif self.previous_item_position == 5:
                                    self.ring = ""
                                elif self.previous_item_position == 6:
                                    self.left_hand = ""
                                elif self.previous_item_position == 7:
                                    self.right_hand = ""
                                
                                self.buttons[clicked_index].pressed = False

                            # If the selected slot is not empty place the item in the next slot that is empty
                            
                            elif self.inventory_items[clicked_index] != "" or self.inventory_items[clicked_index] != None:
                                for i in range(len(self.inventory_items)):
                                    if self.inventory_items[i] == "":
                                        self.inventory_items[i] = self.selected_item
                                        self.selected_item = None
                                        self.previous_item_position = None
                                        self.buttons[clicked_index].pressed = False
                                        break


                    self.previous_button_type = "inventory"

            # Do something when a equipement button has been pressed
            elif self.selected_button_type == "equipement":
                if self.mouse_button == "Left click":
                    clicked_index = self.equipment_buttons.index(selected_button)

                    # No item is selected, so select the clicked item
                    if self.selected_item is None or self.selected_item == "":
                        # Select an item if none is selected
                        if clicked_index != self.previous_item_position:
                            self.previous_item_position = clicked_index
                            # Select the proper item to be selected from the equipement slots
                            if self.equipment_buttons[clicked_index].type == "headwear":
                                self.selected_item = self.headwear
                            if self.equipment_buttons[clicked_index].type == "chestplate":
                                self.selected_item = self.chestplate
                            if self.equipment_buttons[clicked_index].type == "pants":
                                self.selected_item = self.pants
                            if self.equipment_buttons[clicked_index].type == "boots":
                                self.selected_item = self.boots
                            if self.equipment_buttons[clicked_index].type == "necklace":
                                self.selected_item = self.necklace
                            if self.equipment_buttons[clicked_index].type == "ring":
                                self.selected_item = self.ring
                            if self.equipment_buttons[clicked_index].type == "left_hand":
                                self.selected_item = self.left_hand
                            if self.equipment_buttons[clicked_index].type == "right_hand":
                                self.selected_item = self.right_hand

                        else: 
                            # Clicked on the same slot again, deselect the item
                            self.selected_item = None
                            self.previous_item_position = None
                            self.equipment_buttons[clicked_index].pressed = False
                    
                    # When a item is selected do:
                    else:
                        # When you click the same button deselect the button
                        if clicked_index == self.previous_item_position:
                            # when the previous button was the same deselect the 
                            if self.previous_button_type == "equipement":
                                # Clicked on the same slot again, deselect the item
                                self.selected_item = None
                                self.previous_item_position = None
                                self.equipment_buttons[clicked_index].pressed = False
                            
                            # When de index is the same but the item is selected from the inventory. The item should be moved from the inventory to the equipement slot
                            elif self.previous_button_type == "inventory":
                                if self.equipment_buttons[clicked_index].type == self.selected_item.type:
                                    if clicked_index == 0:
                                        self.headwear, self.inventory_items[self.previous_item_position] = self.selected_item, self.headwear
                                    elif clicked_index == 1:
                                        self.chestplate, self.inventory_items[self.previous_item_position] = self.selected_item, self.headwear
                                    elif clicked_index == 2:
                                        self.pants, self.inventory_items[self.previous_item_position] = self.selected_item,self.pants
                                    elif clicked_index == 3:
                                        self.boots, self.inventory_items[self.previous_item_position] = self.selected_item,self.boots
                                    elif clicked_index == 4:
                                        self.necklace, self.inventory_items[self.previous_item_position] = self.selected_item, self.necklace
                                    elif clicked_index == 5:
                                        self.ring, self.inventory_items[self.previous_item_position] = self.selected_item, self.ring
                                    elif clicked_index == 6:
                                        self.left_hand, self.inventory_items[self.previous_item_position] = self.selected_item, self.left_hand
                                    elif clicked_index == 7:
                                        self.right_hand, self.inventory_items[self.previous_item_position] = self.selected_item, self.right_hand
                                    
                                    # Remove the item from its previous slot.
                                    self.selected_item = None
                                    self.previous_item_position = None
                                    # Unpressing the button
                                    self.equipment_buttons[clicked_index].pressed = False


                                elif self.equipment_buttons[clicked_index].type != self.selected_item.type:
                                    # Remove the item from its previous slot.
                                    self.selected_item = None
                                    self.previous_item_position = None
                                    # Unpressing the button
                                    self.equipment_buttons[clicked_index].pressed = False

                        # If a diferent index was selected last time change the equip the item if possible:
                        else:
                            # When the previous button was of the equipement then just select a the new pressed button as the selected item. Without changing the last one
                            if self.previous_button_type == "equipement":
                                # When the last button press was a different equipement type select new equipement as the selected item
                                if clicked_index == 0:
                                    self.selected_item = self.headwear 
                                elif clicked_index == 1:
                                    self.selected_item = self.chestplate 
                                elif clicked_index == 2:
                                    self.selected_item = self.pants
                                elif clicked_index == 3:
                                    self.selected_item = self.boots
                                elif clicked_index == 4:
                                    self.selected_item = self.necklace
                                elif clicked_index == 5:
                                    self.selected_item = self.ring
                                elif clicked_index == 6:
                                    self.selected_item = self.left_hand
                                elif clicked_index == 7:
                                    self.selected_item = self.right_hand

                                # change to new index and reset the previous button
                                self.equipment_buttons[clicked_index].pressed = False
                                self.previous_item_position = clicked_index

                            # When the previous button was of the inventory type, Equip the item if the item can be equiped in the new slot
                            if self.previous_button_type == "inventory":
                                if self.equipment_buttons[clicked_index].type == self.selected_item.type:
                                    # Assigning the item to the equipement
                                    if clicked_index == 0:
                                        self.headwear, self.inventory_items[self.previous_item_position] = self.selected_item, self.headwear
                                    elif clicked_index == 1:
                                        self.chestplate, self.inventory_items[self.previous_item_position] = self.selected_item, self.headwear
                                    elif clicked_index == 2:
                                        self.pants, self.inventory_items[self.previous_item_position] = self.selected_item,self.pants
                                    elif clicked_index == 3:
                                        self.boots, self.inventory_items[self.previous_item_position] = self.selected_item,self.boots
                                    elif clicked_index == 4:
                                        self.necklace, self.inventory_items[self.previous_item_position] = self.selected_item, self.necklace
                                    elif clicked_index == 5:
                                        self.ring, self.inventory_items[self.previous_item_position] = self.selected_item, self.ring
                                    elif clicked_index == 6:
                                        self.left_hand, self.inventory_items[self.previous_item_position] = self.selected_item, self.left_hand
                                    elif clicked_index == 7:
                                        self.right_hand, self.inventory_items[self.previous_item_position] = self.selected_item, self.right_hand

                                    # Resetting the selected item information
                                    self.selected_item = None
                                    self.previous_button_type = None
                                    self.previous_item_position = None
                                    self.equipment_buttons[clicked_index].pressed = False    
                                    
                                elif self.equipment_buttons[clicked_index].type != self.selected_item.type:
                                    # Remove the item from its previous slot.
                                    self.selected_item = None
                                    self.previous_item_position = None
                                    # Unpressing the button
                                    self.equipment_buttons[clicked_index].pressed = False


                    # Set the pressed button type to equipement
                    self.previous_button_type = "equipement"
                            
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
                # Checking inventory buttons
                for button in self.buttons:
                    button.handle_event(event)

                    if button.pressed:
                        self.selected_button_type = "inventory"
                        selected_button = button
                        for button1 in self.buttons:
                            button1.pressed = (button1 == button)
                # Checking equipement buttons
                for button in self.equipment_buttons:
                    button.handle_event(event)

                    if button.pressed:
                        self.selected_button_type = "equipement"
                        selected_button = button
                        for button1 in self.buttons:
                            button1.pressed = (button1 == button)

        return selected_button, mouse_button

    def load_inventory_items_boot(self, inventory_items_to_load):
        inventory_loaded = []
        for item in inventory_items_to_load:
            # If no item list is provided create a empty inventory
            if inventory_items_to_load == None:
                inventory_loaded = [""] * 45
            # If there is no item in the slot create a empty slot
            elif item == "":
                inventory_loaded.append("")
            # If there is a item in the slot add the item to the inventory
            else:
                for complete_item in self.all_items:
                    if item == complete_item.name:
                        inventory_loaded.append(complete_item)
        return inventory_loaded
    
