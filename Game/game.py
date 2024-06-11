import pygame, sys
from . import settings
import debug
from Level import level
from Player import player
from .Menu.mainMenu import *
from .dt import *
from SaveFiles import Save_Functions
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

        # Reading from the save file
        save_data = Save_Functions.reading_save_data()
        # Unpacking the information in the save data to use it
        player_stats = save_data["player_stats"]
        player_skills = save_data["player skills"]
        player_items = save_data["player_items"]
        party_members = save_data["party members"]


        # Starting state of the game should be menu to boot up in the main menu.
        self.state = "menu"
        # Information of the map 
        self.level = None
        # In what map the player is
        self.load_map = save_data["current level"]
        # Where the player should spawn in
        self.entry_point = save_data["spawnpoint"]
        # List of all the items possible in the game
        self.item_list = creating_items()

        # player information and creation
        self.player = player.Player(player_stats,self.item_list, player_items, party_members, player_skills)

    def Run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    next_level = "quit"
            # Drawing the screen and updating it
            self.screen.fill('white')

            # Calculating the deltatime
            self.last_time, dt = calculate_dt(self.last_time)

            # Runs the current level and returns the next level data
            if self.state == "playing":
                # Create a new level and run it
                if self.level is None:
                    self.level = level.Level(self.load_map, self.entry_point, self.player)       
                # Run the level
                next_level, self.player =self.level.run(self.clock)
                
                # Return to the main level 
                if next_level == "main menu":
                    self.state = "menu"

                # Quit the game
                elif next_level == "quit":
                    # Saving the game
                    save_data =Save_Functions.collecting_data(self.player, self)
                    # Writing the save data to a savefile
                    Save_Functions.writing_save_data(save_data)
                    # Quitting the game
                    pygame.quit()
                    sys.exit()

                # If the previous level exited then load the item for the next level
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
                
                # Quitting the game in the main menu when the quit button has been pressed
                if action == "quit":
                    # Save the game data
                    save_data =Save_Functions.collecting_data(self.player, self)
                    # Writing save information to save file
                    Save_Functions.writing_save_data(save_data)
                    # Quitting the game
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
