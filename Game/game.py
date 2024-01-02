import pygame, sys
from .settings import *
from Player.player import *
import debug
from Level.level import *
from .mainMenu import *


class Game:
    def __init__(self):
        #Setting up the game class 
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Torture')
        self.clock =  pygame.time.Clock()
        self.state = "menu"
        self.last_time = pygame.time.get_ticks()
        self.level = None
        self.load_map = "Map Data\Test Center"
        self.entry_point = "West"

    # Function to calculate the time between frames(dt)
    def calculate_dt(self):
        current_time = pygame.time.get_ticks() / 1000.0
        dt = current_time - self.last_time
        self.last_time = current_time
        return dt

    def Run(self):
        while True:
            self.screen.fill('white')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Drawing the screen and updating it
            self.screen.fill('white')
            dt = self.calculate_dt()
            # Runs the current level and returns the next level data
            if self.state == "playing":
                if self.level is None:
                    self.level = self.level = Level(self.load_map, self.entry_point)
                next_level =self.level.run(dt,self.clock)
                # print(next_level)
                self.level = None
                self.load_map = next_level[0]
                self.entry_point = next_level[1]

            # Runs the main menu program on the screen.
            elif self.state == "menu":
                action = mainMenu(self.screen)
                if action == "play":
                    self.state = "playing"
                    if isinstance(self.load_map, str) and not self.level:
                        # Code to execute if self.level is a string and it is empty                        
                        self.level = Level(self.load_map, self.entry_point)
                    elif self.level is None:
                        # Code to execute if self.level is None
                        raise ValueError("No level instatiated.")
                    else:
                        self.level = Level(self.load_map, self.entry_point)
                if action == "quit":
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick()
            debug(self.clock.get_fps())
            self.clock.tick(settings.targetFPS)
