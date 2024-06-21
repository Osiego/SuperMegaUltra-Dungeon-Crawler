import pygame
import sys
import random
from settings import *
from player import Player
from enemy import Enemy
from level import Level
from hud import HUD
from assets import player_sprite, rat_sprite, end_point_sprite, wall_tile_sprite, floor_tile_sprite

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cody's Dungeon")

# Level layout (1s are walls, 0s are open space, 'S' is spawn point, 'E' is end point)
level_layout = [
    "1S1111111111111111111111111111111111111111111111111111E111111111111",
    "1001000000000000000000000000000000000000000000000000100010000000001",
    "1000000000000000000000100000000000010000000000000000100001000000001",
    "1000000000000000000000100110000000010000000000000000100001000000001",
    "1000000000000000000000100110000100000000000000000000001000010000001",
    "1000000000000110001000100000000100000000010000000010010000010000001",
    "1000000000000000001000000000000000000000010000000000000000010000001",
    "1000000000000000000000000100000000000000000001000000000000000000011",
    "100000000000010000011111110000000000000000000100000000000000000000E",
    "1111111111111111111111111111111111111111111111111111111111111111111",
]

# Create level with tile sprites
level = Level(level_layout, wall_tile_sprite, floor_tile_sprite)

# Check if the spawn point was set correctly
if level.spawn_point is None:
    print("Error: No spawn point defined in the level layout.")
    sys.exit(1)

# Create player
player = Player(*level.spawn_point)  # Use the spawn point from the level
player.image = player_sprite  # Assign the loaded player sprite
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Create enemies group
enemies = pygame.sprite.Group()

# Load and scale rat sprite
rat_image = rat_sprite

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
GAME_OVER = 6

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
        player.update(keys, level.walls)  # Pass walls for collision detection

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
                game_state = GAME_OVER
        else:
            game_state = WAIT
            next_turn = PLAYER_TURN
            current_enemy_index = 0

    elif game_state == WAIT:
        # Pause briefly to allow the game state to change
        pygame.time.wait(500)
        game_state = next_turn
        print(f"Switching to {game_state}")

    elif game_state == GAME_OVER:
        print("Game Over")
        running = False

    # Draw the HUD
    hud.draw(screen)

    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()
