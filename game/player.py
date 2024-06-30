import pygame

TILE_SIZE = 32


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100
        self.max_hp = 100
        self.mp = 50
        self.max_mp = 50
        self.attack = 10
        self.defense = 5
        self.level = 1
        self.xp = 0
        self.gold = 0
        self.inventory = []
        self.equipped_item = None
        self.sprite = pygame.image.load("assets/player.png")
        self.sprite = pygame.transform.scale(self.sprite, (TILE_SIZE, TILE_SIZE))

    def move(self, dx, dy, level):
        new_x = self.x + dx
        new_y = self.y + dy
        if level.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y

    def pickup_item(self, item):
        self.inventory.append(item)

    def use_item(self):
        if self.equipped_item:
            stat, value = self.equipped_item.effect
            if stat == 'hp':
                self.hp = min(self.hp + value, self.max_hp)
            elif stat == 'mp':
                self.mp = min(self.mp + value, self.max_mp)
            elif stat == 'attack':
                self.attack += value
            elif stat == 'defense':
                self.defense += value
            self.inventory.remove(self.equipped_item)
            self.equipped_item = None

    def cycle_equipped_item(self):
        if self.inventory:
            if self.equipped_item:
                index = (self.inventory.index(self.equipped_item) + 1) % len(self.inventory)
            else:
                index = 0
            self.equipped_item = self.inventory[index]

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= 100 * self.level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp -= 100 * (self.level - 1)
        self.max_hp += 10
        self.hp = self.max_hp
        self.max_mp += 5
        self.mp = self.max_mp
        self.attack += 2
        self.defense += 1

    def draw(self, screen):
        screen.blit(self.sprite, (self.x * TILE_SIZE, self.y * TILE_SIZE))
        # Draw health bar
        pygame.draw.rect(screen, (255, 0, 0), (self.x * TILE_SIZE, self.y * TILE_SIZE - 5, TILE_SIZE, 3))
        pygame.draw.rect(screen, (0, 255, 0),
                         (self.x * TILE_SIZE, self.y * TILE_SIZE - 5, int(TILE_SIZE * (self.hp / self.max_hp)), 3))
