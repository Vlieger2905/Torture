import pygame
from Game import settings
import sys
import time

# local Settings
local_scale = settings.sprite_size

left_limit = 0.06
right_limit = 0.02
top_limit = 0.11

def TextBox(screen, text):
    # Setting up the basics of the textbox
    image = pygame.image.load("Sprites\DEV resources\Text Box.png")
    screen_width, screen_height = pygame.display.get_surface().get_size()
    surface = pygame.Surface((screen_width, screen_height // 3))
    rect = surface.get_rect(bottom=screen_height)
    max_width, max_height = surface.get_size()
    # Transforming the image to the correct size
    image = pygame.transform.scale(image, (max_width, max_height))
    # Text settings
    total_text = text
    text_draw = ""
    text_color = (255, 255, 255)  # White color
    text_position = (screen_width*left_limit,max_height*top_limit)  # Adjust the position as needed
    font = pygame.font.Font(None, 36)  # You can adjust the font size and style here
    # Settings for the delay and timing of adding a character to drawing of the text
    old_time = time.time() 
    delay = 0.05
    full_text = False

    while True:    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if full_text:
                        return "hello"
                    else:
                        full_text = True

        surface.blit(image, (0, 0))
        
        # Call animate_text to check if it's time to print "now"
        text_draw, old_time, full_text = animate_text(old_time, total_text, text_draw, delay,full_text)

        draw_text(text_draw, font, text_color, text_position, surface)
        
        screen.blit(surface, rect.topleft)
        pygame.display.flip()

def animate_text(old_time, total_text, text_draw, delay, full_text):
    if full_text:
        text_draw = total_text
        return text_draw, old_time, full_text	
    else:
        current_time = time.time()
        if current_time - old_time >= delay:
            # Adding one character to the text.
            length = len(text_draw)
            text_draw = total_text[:length + 1]
            # Update old_time for the next animation cycle
            old_time = current_time  
            # Changing the state if the text is already fully on the screen
            if length == len(total_text):
                full_text = True
        return text_draw, old_time, full_text


def draw_text(text, font, color, position,surface):
    words = text.split(' ')
    max_width, _ = surface.get_size()
    max_width -= position[0] + max_width*right_limit  # Adjust max_width by the x position of the text

    lines = []
    line = ''
    for word in words:
        if font.size(line + ' ' + word)[0] < max_width:
            if line:
                line += ' '
            line += word
        else:
            lines.append(line)
            line = word
    lines.append(line)

    y = position[1]
    for line in lines:
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (position[0], y))
        y += font.get_height()  # Move to the next line

