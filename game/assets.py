import pygame
from settings import TILE_SIZE

def load_image(path, size):
    try:
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Unable to load image at {path}: {e}")
        raise SystemExit(e)

# load all sprites
player_sprite = load_image('/home/shokk/PycharmProjects/Game/game/assets/donald.png', (50, 50))
rat_sprite = load_image('/home/shokk/PycharmProjects/Game/game/assets/orange_rat.png',(50, 50))
end_point_sprite = load_image('/home/shokk/PycharmProjects/Game/game/assets/open_door.png', (50, 50))
wall_tile_sprite = load_image('/home/shokk/PycharmProjects/Game/game/assets/brick_brown_0.png', (TILE_SIZE, TILE_SIZE))
floor_tile_sprite = load_image('/home/shokk/PycharmProjects/Game/game/assets/crystal_floor_0.png', (TILE_SIZE, TILE_SIZE))