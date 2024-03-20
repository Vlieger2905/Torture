from ..settings import *
import pygame
from ..Classes import Button
from debug import debug

pygame.init()
# Loading button images
play_image = pygame.image.load("Sprites/Buttons/Test/Play-test.png")
quit_image = pygame.image.load("Sprites/Buttons/Test/Quit-test.png")
# Creating the buttons
play_button = Button.Button((100, 100),"play", play_image, None, (200, 100))
quit_button = Button.Button((100, 200),"quit", quit_image, None, (200, 100))
# List that stores all the buttons
buttons = [play_button,quit_button]
# Running the menu
def mainMenu(screen):
    while True:
        pygame_events = pygame.event.get()
        screen.fill((255,255,255))
        for button in buttons:
            button.draw(screen)
        event = Button.check_events(buttons, pygame_events)

        for button in buttons:
            if event == button.output:
                return button.output

        pygame.display.flip()