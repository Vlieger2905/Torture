import pygame
import sys

class Inventory_Button():
    def __init__(self, position, image=None, size = None, colour=None):
        self.rect = pygame.Rect(position, (48, 48))
        self.image = image
        self.colour = colour
        self.pressed = False
        if self.image is not None:
            if size is not None:
                self.image = pygame.transform.scale(self.image, size)
            self.rect.size = self.image.get_size()   
        self.rect.topleft = position

    def draw(self, screen):
        if self.pressed:
            # Create a transparent white surface with the same size as self.rect
            transparent_white_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            transparent_white_surface.fill((255, 255, 255, 128))  # 128 is the alpha value for transparency

            # Blit the transparent white surface onto the screen
            screen.blit(transparent_white_surface, self.rect)
        
        # Blit the image onto the screen
        if self.image is not None:
            screen.blit(self.image, self.rect)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Left mouse button pressed
            if self.rect.collidepoint(event.pos):
                self.pressed = True
            # If you press the same space twice you unselect it.
            elif self.rect.collidepoint(event.pos) and self.pressed:
                self.pressed = False
        return self.pressed

# def check_events_inventory(buttons, events):
#     for event in events:
#         for button in buttons:
#             button.handle_event(event)
#             if button.pressed == True:
#                 return button
            
def check_events_inventory(buttons, events):
    selected_button = None
    
    for event in events:
        for button in buttons:
            button.handle_event(event)

            if button.pressed:
                selected_button = button
                for item in buttons:
                    item.pressed = (item == button)
    
    return selected_button


            