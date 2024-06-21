import pygame
from settings import *

def handle_events(game_state, player, enemies, click_radius):
    next_state = game_state
    mouse_pos = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, None, None, game_state
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
                        next_state = EXPLORATION
                    else:
                        next_state = ENEMY_TURN
                    break
    return True, mouse_pos, None, next_state
