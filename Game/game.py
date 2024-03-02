import pygame, sys
from . import settings
import debug
from Level import level
from Player import player
from .Menu.mainMenu import *
from .dt import *
from .SaveFiles import Functions
from .Classes.Item import creating_items

class Game:
    def __init__(self):
        #Setting up the game class 
        pygame.init()
        # self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGTH), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGTH))
        pygame.display.set_caption('Torture')
        # Setting up the fps control system of the game
        self.clock =  pygame.time.Clock()
        self.last_time = pygame.time.get_ticks()

        self.state = "menu"
        # Information of the map 
        self.level = None
        # In what map the player is
        self.load_map = "Map Data\\Test Center"
        # Where the player should spawn in
        self.entry_point = "North"
        # List of all the items possible in the game
        self.item_list = creating_items()

        # player information and creation
        stats = {}
        self.player = player.Player(stats,self.item_list )
        

    def Run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Drawing the screen and updating it
            self.screen.fill('white')

            # Calculating the deltatime
            self.last_time, dt = calculate_dt(self.last_time)

            # Runs the current level and returns the next level data
            if self.state == "playing":
                if self.level is None:
                    self.level = level.Level(self.load_map, self.entry_point, self.player)       
                next_level, self.player =self.level.run(self.clock)
                if next_level == "main menu":
                    self.state = "menu"
                elif next_level == "quit":
                    Functions.collecting_data(self.player)
                    pygame.quit()
                    sys.exit()
                else:
                    self.level = None
                    self.load_map = next_level[0]
                    self.entry_point = next_level[1]

            # Runs the main menu program on the screen.
            elif self.state == "menu":
                action = mainMenu(self.screen)
                # When the play button gets pressed 
                if action == "play":
                    self.state = "playing"
                    if isinstance(self.load_map, str) and not self.level:
                        # Code to execute if self.level is a string and it is empty                        
                        self.level = level.Level(self.load_map, self.entry_point, self.player)
                    elif self.level is None:
                        # Code to execute if self.level is None
                        raise ValueError("No level instatiated.")
                if action == "quit":
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
