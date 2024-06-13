import pygame
import sys
import random
from settings import *
from player import Player
from enemy import Enemy
from level import Level
from hud import HUD

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cody's Dungeon")

# Load player sprite from the assets folder
try:
    player_sprite = pygame.image.load('/home/shokk/PycharmProjects/Game/.venv/assets/human_male.png')
    player_sprite = pygame.transform.scale(player_sprite, (50, 50))  # Resize if necessary
except pygame.error as e:
    print(f"Unable to load player sprite image: {e}")
    sys.exit(1)

# Load rat sprite from the assets folder
try:
    rat_sprite = pygame.image.load('/home/shokk/PycharmProjects/Game/.venv/game/Rat.png')
    rat_sprite = pygame.transform.scale(rat_sprite, (50, 50))  # Resize if necessary
except pygame.error as e:
    print(f"Unable to load rat sprite image: {e}")
    sys.exit(1)

# Load end point sprite from the assets folder
try:
    end_point_sprite = pygame.image.load('/home/shokk/PycharmProjects/Game/.venv/assets/end_point.png')
    end_point_sprite = pygame.transform.scale(end_point_sprite, (50, 50))  # Resize if necessary
except pygame.error as e:
    print(f"Unable to load end point sprite image: {e}")
    sys.exit(1)

# function to randomly generate level layout
def generate_random_level(grid_width, grid_height):
    layout = [['1'] * grid_width for _ in range(grid_height)]
    start_x, start_y = 1, 1
    end_x, end_y = grid_width - 2, grid_height - 2

    # use DFS to create a random path from Start - Finish
    def create_path(x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x +dx, y + dy
            if 1 <= nx < grid_width -1 and 1 <= ny < grid_height -1 and layout[ny][nx] == '1':
                layout[ny][nx] = '0'
                create_path(nx, ny)

        layout[start_y][start_x] = 'S'  # start point
        layout[end_y][end_x] = 'E'   # End Point
        create_path(start_x, start_y)

        return_layout

    # generate random level layout
    level_layout = generate_random_level(GRID_WIDTH, GRID_HEIGHT)

    # create level
    level = Level(level_layout)


# Check if the spawn point was set correctly
if Level.spawn_point is None:
    print("Error: No spawn point defined in the level layout.")
    sys.exit(1)

# Create player
player = Player(*level.spawn_point)  # Use the spawn point from the level
player.image = player_sprite  # Assign the loaded player sprite
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Create enemies group fix here
enemies = pygame.sprite.Group()

# load and scale rat sprite
rat_image = pygame.image.load("/home/shokk/PycharmProjects/Game/.venv/game/Rat.png")
rat_image = pygame.transform.scale(rat_image, (TILE_SIZE, TILE_SIZE))

# Create one enemy (rat)
# Ensure the rat is not placed directly at the spawn point
rat_position = (level.spawn_point[0] + TILE_SIZE * 2, level.spawn_point[1])
rat = Enemy(*rat_position)
rat.image = rat_image # Ensure the rat sprite is loaded
rat.rect = rat.image.get_rect(topleft=rat_position)
all_sprites.add(rat)
enemies.add(rat)

# Create end point sprite
end_point = pygame.sprite.Sprite()
end_point.image = end_point_sprite
end_point.rect = end_point.image.get_rect()
end_point.rect.topleft = level.end_point
all_sprites.add(end_point)

# Create HUD
hud = HUD(player)

# Game states
EXPLORATION = 1
FIGHTING = 2
PLAYER_TURN = 3
ENEMY_TURN = 4
WAIT = 5

game_state = EXPLORATION
next_turn = None
current_enemy_index = 0  # To track which enemy is attacking

click_radius = 20  # Increase this value to make the clickable area larger

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == PLAYER_TURN:
            mouse_pos = pygame.mouse.get_pos()
            print(f"Mouse click detected at {mouse_pos}")
            for enemy in enemies:
                enemy_click_box = pygame.Rect(
                    enemy.rect.left - click_radius,
                    enemy.rect.top - click_radius,
                    enemy.rect.width + 2 * click_radius,
                    enemy.rect.height + 2 * click_radius
                )
                print(f"Checking enlarged enemy click box at {enemy_click_box.topleft} with size {enemy_click_box.size}")
                if enemy_click_box.collidepoint(mouse_pos):
                    print(f"Enemy {enemy} clicked at position {mouse_pos}")
                    player.attack_enemy(enemy)
                    if enemy.health <= 0:
                        enemy.kill()
                        game_state = WAIT
                        next_turn = EXPLORATION
                    else:
                        game_state = WAIT
                        next_turn = ENEMY_TURN
                    break

    # Get key states
    keys = pygame.key.get_pressed()

    if game_state == EXPLORATION:
        # Update player with collision detection
        player.update(keys, level.tiles)

        # Check for proximity to switch to fighting mode
        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy) and pygame.math.Vector2(player.rect.center).distance_to(enemy.rect.center) <= 50:
                print("Switching to fighting mode")
                game_state = FIGHTING
                break

        # Update enemies
        for enemy in enemies:
            enemy.update(player)

        # Calculate offset to center the player
        offset_x = WIDTH // 2 - player.rect.centerx
        offset_y = HEIGHT // 2 - player.rect.centery

        # Draw everything with the offset
        screen.fill(BLACK)
        level.draw(screen, offset_x, offset_y)
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))
            if isinstance(sprite, Player) or isinstance(sprite, Enemy):
                sprite.draw_health_bar(screen, offset_x, offset_y)

    elif game_state == FIGHTING:
        print("Player's turn")
        game_state = PLAYER_TURN

    elif game_state == PLAYER_TURN:
        # Wait for the player to click an enemy
        pass

    elif game_state == ENEMY_TURN:
        if current_enemy_index < len(enemies.sprites()):
            print("Enemies' turn")
            enemy = enemies.sprites()[current_enemy_index]
            enemy.attack(player)
            current_enemy_index += 1
            if player.health <= 0:
                print("Game Over")
                running = False
        else:
            game_state = WAIT
            next_turn = PLAYER_TURN
            current_enemy_index = 0

    elif game_state == WAIT:
        # Pause briefly to allow the game state to change
        pygame.time.wait(500)
        game_state = next_turn
        print(f"Switching to {game_state}")

    # Draw the HUD
    hud.draw(screen)

    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()
