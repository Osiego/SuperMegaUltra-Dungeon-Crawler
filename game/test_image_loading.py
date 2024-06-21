import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test Image Loading")

# Function to load an image with error handling
def load_image(path):
    try:
        image = pygame.image.load(path).convert_alpha()
        return image
    except pygame.error as e:
        print(f"Unable to load image at {path}: {e}")
        sys.exit(1)

# Load an image (update the path to your image file)
image_path = '/game/assets/Rat.png'
image = load_image(image_path)
image = pygame.transform.scale(image, (100, 100))  # Resize if necessary

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the image
    screen.fill((0, 0, 0))
    screen.blit(image, (350, 250))
    pygame.display.flip()

pygame.quit()
sys.exit()
