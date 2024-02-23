from ..settings import *
import pygame
from Game import dt as detalTime
from ..Classes import Button
from debug import debug

pygame.init()
# Loading button images
play_image = pygame.image.load("Sprites/Buttons/Test/Play-test.png")
quit_image = pygame.image.load("Sprites/Buttons/Test/Quit-test.png")
menu_image = pygame.image.load("Sprites\DEV resources\SpriteTest.png")
# Creating the buttons
play_button = Button.Button((100, 100),"play", play_image, None, (200, 100))
quit_button = Button.Button((100, 200),"quit", quit_image, None, (200, 100))
main_menu = Button.Button((100,300),"return to main menu", menu_image, "Main Menu", (200,100))
# List that stores all the buttons
buttons = [play_button,quit_button,main_menu]
# Running the menu

def pause_menu(screen,clock, last_time):
    while True:

        last_time,dt = detalTime.calculate_dt(last_time)
        # Drawing the buttons
        for button in buttons:
            button.draw(screen)
        # Checking all buttons for events
        event = Button.check_events(buttons)
        # For each button check if the action happened and if so return the result
        for button in buttons:
            if event == button.output:
                return button.output, last_time
           
        clock.tick(FPS)
        pygame.display.flip()