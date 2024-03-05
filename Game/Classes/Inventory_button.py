import pygame
import sys

class Inventory_Button():
    def __init__(self, position, image=None, size = None, colour=None):
        self.rect = pygame.Rect(position, (0, 0))
        self.image = image
        self.colour = colour
        self.pressed = False
        if self.image is not None:
            if size is not None:
                self.image = pygame.transform.scale(self.image, size)
            self.rect.size = self.image.get_size()   
        self.rect.topleft = position

    def draw(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect) 

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Left mouse button pressed
            if self.rect.collidepoint(event.pos):
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Left mouse button released
            if self.pressed and self.rect.collidepoint(event.pos):
                # Perform button click action here
                self.pressed = False
                return self.output
                # You can replace the print statement with your desired action
            self.pressed = False
        return None
            
def check_events_inventory(buttons):
    for event in pygame.event.get():
        for button in buttons:
            case = button.handle_event(event)
            
            