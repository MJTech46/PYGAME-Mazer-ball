# Mazer ball

import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load("assets/musics/Density & Time - MAZE  NO COPYRIGHT 8-bit Music.mp3")
pygame.mixer.music.set_volume(0.75)  # Set volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play indefinitely (-1 for looping)

# Screen dimensions
screen_width, screen_height = 800, 600

# Create the display surface
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Display Image in Pygame")

# Load the image
image = pygame.image.load("assets/sprites/wall/Black_Brick.png")

# Resize the image
new_width, new_height = 50, 50  # Desired dimensions
image = pygame.transform.scale(image, (new_width, new_height))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (optional)
    screen.fill((0, 0, 0))  # Black background

    for h in range(0, 750, 150):
        for i in range(0,800, 50):
            # Display the image at (x, y) coordinates
            screen.blit(image, (i, h))  

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
