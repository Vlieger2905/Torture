import pygame
import sys
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

pygame.init()
screen = pygame.display.set_mode((1280, 720))

try:
    tmx_data = load_pygame('Map Data\\Test Map\\testMap.tmx')
except Exception as e:
    print("Error loading TMX file:", e)
    sys.exit()

for obj in tmx_data.objects:
    print(obj.type, obj.name)
    
# for item in tmx_data.visible_layers:
#     if item.name == "Collision Barriers":
#         print(item)
    
sprite_group = pygame.sprite.Group()
size = 16
# cycle through all layers
# for layer in tmx_data.layers:
#     # if layer.name in ('Floor', 'Plants and rocks', 'Pipes')
#     if hasattr(layer, 'data') and layer.visible:
#         for x, y, surf in layer.tiles():
#             pos = ((x * size), (y * size))
#             # Tile(pos=pos, surf=surf, groups=sprite_group)
#     if hasattr(layer, 'data') and not layer.visible:
#         for x, y, surf in layer.tiles():
#             pos = ((x * size), (y * size))
#             Tile(pos=pos, surf=surf, groups=sprite_group)
# object_layer = tmx_data.get_layer_by_name('Spawnpoint')


    # Check if the object has the 'Marker' class


# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#     screen.fill('black')
#     sprite_group.draw(screen)

#     pygame.display.update()
