import pygame
import sys

class Button():
    def __init__(self, position, output, image=None, text=None, size = None, font=None, colour=None, combat = None, enemy = False, information = None):
        self.rect = pygame.Rect(position, (0, 0))
        self.image = image
        self.text = text
        self.font = font
        self.colour = colour
        self.pressed = False
        # Saves the output of the button. This will be returned when the button is pressed
        self.output = output 
        # If there is further information that needs to be stored in the button this variable is it
        self.information = information
        if self.image is not None:
            if size is not None:
                self.image = pygame.transform.scale(self.image, size)
            self.rect.size = self.image.get_size()   
        # For the combat the location represents the bottom right of the sprite or bottom left if they are the enemy
        if combat:
            if enemy:    
                self.rect.bottomleft = position
            else:
                self.rect.bottomright = position
        else:
            self.rect.topleft = position

    def draw(self, screen):
        # Draw image if there is a image
        if self.image is not None:
            screen.blit(self.image, self.rect) 
        # Draw text is there is a provided text and font
        elif self.text is not None and self.font is not None:
            text_surface = self.font.render(self.text, True, self.colour or (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        # Left mouse button pressed
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
        # Left mouse button released
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed and self.rect.collidepoint(event.pos):
                # Perform button click action here
                self.pressed = False
                return self.output
                # You can replace the print statement with your desired action
            self.pressed = False
        return None
            
def check_events(buttons, pygame_events):
    # List with the event that needs to be checked for the buttons
    events_type_check = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]
    for event in pygame_events:
        for check in events_type_check:
            # If the event in pygame_events is the same a one from the list to check actually do something otherwise go to the next event.
            if event.type == check:
                for button in buttons:
                    case = button.handle_event(event)
                    if case is not None:
                        return button.output
                del events_type_check[events_type_check.index(check)]
            if events_type_check == []:
                return
            