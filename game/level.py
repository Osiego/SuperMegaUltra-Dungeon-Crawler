import pygame
from settings import TILE_SIZE

class Level:
    def __init__(self, layout, wall_tile_sprite, floor_tile_sprite):
        self.tiles = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.spawn_point = None
        self.end_point = None
        self.create_level(layout, wall_tile_sprite, floor_tile_sprite)

    def create_level(self, layout, wall_tile_sprite, floor_tile_sprite):
        for y, row in enumerate(layout):
            for x, tile in enumerate(row):
                if tile == '1':
                    wall = Wall(x * TILE_SIZE, y * TILE_SIZE, wall_tile_sprite)
                    self.tiles.add(wall)
                    self.walls.add(wall)
                elif tile == '0':
                    floor = Floor(x * TILE_SIZE, y * TILE_SIZE, floor_tile_sprite)
                    self.tiles.add(floor)
                elif tile == 'S':
                    self.spawn_point = (x * TILE_SIZE, y * TILE_SIZE)
                    print(f"Spawn point set at: {self.spawn_point}")
                elif tile == 'E':
                    self.end_point = (x * TILE_SIZE, y * TILE_SIZE)
                    print(f"End point set at: {self.end_point}")

    def draw(self, screen, offset_x, offset_y):
        for tile in self.tiles:
            screen.blit(tile.image, (tile.rect.x + offset_x, tile.rect.y + offset_y))

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
