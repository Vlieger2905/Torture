import pygame

# Function to calculate the time between frames(dt)
def calculate_dt(last_time):
    current_time = pygame.time.get_ticks() / 1000.0
    dt = current_time - last_time
    last_time = current_time
    return last_time, dt