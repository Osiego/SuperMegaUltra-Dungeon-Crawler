import pygame
from settings import TILE_SIZE  # Import TILE_SIZE from settings

def load_image(path, size):
    try:
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, size)
        return image
    except pygame.error as e:
        print(f"Unable to load image at {path}: {e}")
        return None

# Load player sprite from the assets folder
player_sprite = load_image('/home/shokk/PycharmProjects/Game/game/assets/donald.png', (50, 50))

# Load rat sprite from the assets folder
rat_sprite = load_image('/home/shokk/PycharmProjects/Game/game/assets/orange_rat.png', (50, 50))

# Load end point sprite from the assets folder
end_point_sprite = load_image('/home/shokk/PycharmProjects/Game/game/assets/open_door.png', (50, 50))

# Load tile sprites
wall_tile_sprite = load_image('/home/shokk/PycharmProjects/Game/game/assets/brick_brown_0.png', (TILE_SIZE, TILE_SIZE))
floor_tile_sprite = load_image('/home/shokk/PycharmProjects/Game/game/assets/crystal_floor_0.png', (TILE_SIZE, TILE_SIZE))

# Load spawn point sprite
spawn_point_sprite = load_image('/home/shokk/PycharmProjects/Game/game/assets/runed_door.png', (TILE_SIZE, TILE_SIZE))