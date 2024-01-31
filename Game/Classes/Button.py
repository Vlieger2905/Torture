import pygame
import sys

class Button():
    def __init__(self, position,output, image=None, text=None,size = None, font=None, colour=None):
        self.rect = pygame.Rect(position, (0, 0))
        self.image = image
        self.text = text
        self.font = font
        self.colour = colour
        self.pressed = False
        self.output = output 
        if self.image is not None:
            if size is not None:
                self.image = pygame.transform.scale(self.image, size)
            self.rect.size = self.image.get_size()   
        # else:
        #     self.rect.size = size
        self.rect.topleft = position

    def draw(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect) 
        elif self.text is not None and self.font is not None:
            text_surface = self.font.render(self.text, True, self.colour or (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

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
            
def check_events(buttons):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        for button in buttons:
            case = button.handle_event(event)
            if case is not None:
                return button.output
            