import pygame
from Game import settings

class Player(pygame.sprite.Sprite):
# Initializing the player
    def __init__(self,position, groups, obstacle_sprites, exits):
        super().__init__(groups)
        self.image = pygame.image.load('Sprites\\Player\\Village boy #1.png').convert_alpha()
        # Scale the image to 32x32 pixels
        self.image = pygame.transform.scale(self.image, (settings.Tilesize, settings.Tilesize))
        self.rect  = self.image.get_rect(topleft = position)
        # Setting the player hitbox
        self.hitbox = self.rect.inflate(-10*settings.scale,-10*settings.scale)
        # Variables used within the player class
        self.direction = pygame.math.Vector2()
        self.speed = 500
        self.obstacle_sprites = obstacle_sprites
        self.exit_rects = exits 

        self.first_frame = True

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.y = 0
        self.direction.x = 0
        # Vertical movement of the player input
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        # Horizontal movement of the player input
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, speed,dt):
        # If the player is moving making sure that the velocity stays the same and that the player is not moving faster when moving diagonally
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        # Moving the player
        move_vector = self.direction * speed * dt
        self.hitbox.x +=move_vector.x
        self.collision('horizontal')
        self.hitbox.y +=move_vector.y
        self.collision('vertical')
        self.rect.center=self.hitbox.center

    # Checks for the collision of the player hitbox with the obstacles
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #Moving to the rigth
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #Moving to the left
                        self.hitbox.left = sprite.hitbox.right           

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #Moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #Moving up
                        self.hitbox.top = sprite.hitbox.bottom

    # checks for the collision between the player hitbox and the exit hitboxes
    def collision_exit(self):
        for obj in self.exit_rects:
                if obj.hitbox.colliderect(self.hitbox):
                    return obj.name

    def update(self,dt):
        if self.first_frame is False:
            self.input()
            self.move(self.speed,dt)
        else:
            self.first_frame = False