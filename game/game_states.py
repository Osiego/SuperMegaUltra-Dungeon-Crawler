from settings import *

def handle_exploration(player, level, enemies, game_state):
    player.update(pygame.key.get_pressed(), level.tiles)
    for enemy in enemies:
        if pygame.sprite.collide_rect(player, enemy) and pygame.math.Vector2(player.rect.center).distance_to(enemy.rect.center) <= 50:
            print("Switching to fighting mode")
            return FIGHTING
    for enemy in enemies:
        enemy.update(player)
    return game_state

def handle_fighting():
    print("Player's turn")
    return PLAYER_TURN

def handle_player_turn(player, mouse_pos, enemies, click_radius):
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
                return WAIT, EXPLORATION
            else:
                return WAIT, ENEMY_TURN
    return PLAYER_TURN, None

def handle_enemy_turn(enemies, current_enemy_index, player):
    if current_enemy_index < len(enemies.sprites()):
        print("Enemies' turn")
        enemy = enemies.sprites()[current_enemy_index]
        enemy.attack(player)
        current_enemy_index += 1
        if player.health <= 0:
            print("Game Over")
            return WAIT, GAME_OVER, current_enemy_index
    else:
        return WAIT, PLAYER_TURN, 0
    return ENEMY_TURN, None, current_enemy_index

def handle_wait(next_turn):
    pygame.time.wait(500)
    print(f"Switching to {next_turn}")
    return next_turn
