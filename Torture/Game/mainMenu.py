from .settings import *
import pygame
import sys
from .Button import *
from debug import debug

pygame.init()

play_image = pygame.image.load("Sprites/Buttons/Test/Play-test.png")
quit_image = pygame.image.load("Sprites/Buttons/Test/Quit-test.png")
play_button = Button((100, 100),"play", play_image, None, (200, 100) )
quit_button = Button((100, 200),"quit", quit_image, None, (200, 100) )
buttons = [play_button,quit_button]

def mainMenu(screen):
    while True:
        screen.fill((255,255,255))
        for button in buttons:
            button.draw(screen)
        event = check_events(buttons)

        if event == play_button.output:
            # print(play_button.output)
            return play_button.output
        if event == quit_button.output:
            # print(quit_button.output)
            return quit_button.output


        pygame.display.flip()