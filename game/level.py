import random
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from enemy import Enemy # Import the Enemy class correctly
from item import Item

GRID_WIDTH = 32
GRID_HEIGHT = 24
TILE_SIZE = 32

class Room:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def intersects(self, other):
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)

    def center(self):
        return (self.x + self.width // 2, self.y + self.height // 2)


class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.tiles = [[1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.rooms = []
        self.enemies = []
        self.items = []
        self.stairs_pos = None
        self.generate_rooms()
        self.connect_rooms()
        self.place_stairs()
        self.place_enemies()
        self.place_items()

    def generate_rooms(self):
        num_rooms = random.randint(3, 6)  # Generate between 3 and 6 rooms
        for _ in range(num_rooms):
            room_width = random.randint(4, 8)
            room_height = random.randint(4, 8)
            room_x = random.randint(1, GRID_WIDTH - room_width - 1)
            room_y = random.randint(1, GRID_HEIGHT - room_height - 1)
            room = Room(room_x, room_y, room_width, room_height)
            self.rooms.append(room)

    def connect_rooms(self):
        if len(self.rooms) < 2:
            return  # No need to connect rooms if there's only one room

        room_centers = [room.center() for room in self.rooms]
        room_pairs = [(room_centers[i], room_centers[j])
            for i in range(len(room_centers))
            for j in range(i + 1, len(room_centers))]

        # Connect each pair of rooms with a tunnel
        for room1_center, room2_center in room_pairs:
            self.create_tunnel(room1_center, room2_center)

    def create_tunnel(self, start, end):
        # Implementation for creating a tunnel between two points
        pass
        # Extra closing parenthesis here
