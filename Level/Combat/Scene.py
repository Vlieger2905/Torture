import pygame
import Game.dt as deltaTime
from debug import *


class Combat_scene():
    def __init__(self, enemy_party, player_party) -> None:
        # Getting the display surface
        self.display_surface = pygame.display.get_surface()


    def run(self, clock):
        last_time = pygame.time.get_ticks()
        while True:
            last_time,dt = deltaTime.calculate_dt(last_time)
            # Checking for key inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        return last_time
                
                
            self.display_surface.fill((0,0,123))
            

            # Ending of each frame and updating the screen 
            debug(clock.get_fps())
            clock.tick(60)
            pygame.display.update()