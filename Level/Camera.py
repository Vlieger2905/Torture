import pygame
from Game import settings

class CameraGroup(pygame.sprite.Group):
    def __init__(self, floor_image):
# general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.display_WIDTH = self.display_surface.get_size()[0] // 2
        self.display_HEIGTH = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

# Creating the floor
        floor_map = pygame.image.load(floor_image).convert()
        floor_map_size = floor_map.get_size()
        self.floor_surface = pygame.transform.scale(floor_map, (floor_map_size[0] / settings.sprite_size * settings.Tilesize,floor_map_size[1] / settings.sprite_size * settings.Tilesize ))
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))

# Drawing the sprites in the group
    def custom_draw(self,player):
        self.offset.x = player.rect.centerx - self.display_WIDTH
        self.offset.y = player.rect.centery - self.display_HEIGTH

# Drawing the floor
        floor_offset = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset)
# Drawing the sprites
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
#Testing function only
#See the sensory lines of the enemy type
            if hasattr(sprite, 'sensory_lines'):
                # Draw sensory lines
                for line in sprite.sensory_lines:
                    start_point = (line[0][0] - self.offset.x, line[0][1] - self.offset.y)
                    end_point = (line[1][0] - self.offset.x, line[1][1] - self.offset.y)
                    pygame.draw.line(self.display_surface, line[2], start_point, end_point, 2)