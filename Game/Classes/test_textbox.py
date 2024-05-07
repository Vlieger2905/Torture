import pygame
from Game.Classes import TextBox as tb
from Game import settings

# Example usage
pygame.init()
screen = pygame.display.set_mode((800, 600))
text = "Hello how you doing Hello how you doing Hello how you doing Hello how you doing Hello how you doing Hello how you doing Hello how you doing"
# Fix the position of the text to be in line with the first pixel of the text box
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Fill the screen with black color
    returned = tb.TextBox(screen, text)
    pygame.display.flip()

pygame.quit()
