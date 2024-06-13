import pygame
from settings import *

class Level:
    def __init__(self, layout):
        self.tiles = pygame.sprite.Group()
        self.spawn_point = None
        self.end_point = None
        self.create_level(layout)

    def create_level(self, layout):
        for y, row in enumerate(layout):
            for x, tile in enumerate(row):
                if tile == '1':
                    wall = Wall(x * TILE_SIZE, y * TILE_SIZE)
                    self.tiles.add(wall)
                elif tile == 'S':
                    self.spawn_point = (x * TILE_SIZE, y * TILE_SIZE)
                elif tile == 'E':
                    self.end_point = (x * TILE_SIZE, y * TILE_SIZE)

    def draw(self, screen, offset_x, offset_y):
        for tile in self.tiles:
            screen.blit(tile.image, (tile.rect.x + offset_x, tile.rect.y + offset_y))

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
