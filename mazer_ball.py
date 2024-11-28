# Mazer Ball

import pygame
import os
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Music folder path
music_folder = "assets/musics"

# List all MP3 files in the music folder
music_files = [os.path.join(music_folder, file) for file in os.listdir(music_folder) if file.endswith('.mp3')]

# Function to play the next track
def play_next_track():
    global current_track_index
    if music_files:
        current_track_index = (current_track_index + 1) % len(music_files)
        pygame.mixer.music.load(music_files[current_track_index])
        pygame.mixer.music.play()
        print(f"Now playing: {music_files[current_track_index]}")

# Initialize the first track
current_track_index = -1
play_next_track()

# Screen dimensions
screen_width, screen_height = 800, 600

# Create the display surface
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mazer Ball")

# Load the image
image = pygame.image.load("assets/sprites/wall/Black_Brick.png")

# Resize the image
new_width, new_height = 50, 50  # Desired dimensions
image = pygame.transform.scale(image, (new_width, new_height))

# Brick movement settings
brick_speed = 50  # Speed to move downward (pixels per second)
time_interval = 1000  # Time interval in milliseconds (1 second)
rows_on_screen = screen_height // new_height  # Number of rows visible on the screen

# Initialize brick rows with random patterns
brick_rows = [row * new_height for row in range(rows_on_screen)]

# Function to generate a new random row pattern
def generate_row_pattern():
    return [1 if random.random() > 0.5 else 0 for _ in range(screen_width // new_width)]

# Create initial rows
brick_patterns = [generate_row_pattern() for _ in range(rows_on_screen)]

# Set up a timer for brick movement
pygame.time.set_timer(pygame.USEREVENT + 1, time_interval)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT + 1:
            # Move all rows downward
            brick_rows = [y + new_height for y in brick_rows]

            # Remove rows that move off-screen
            if brick_rows[0] >= screen_height:
                brick_rows.pop(0)
                brick_patterns.pop(0)

            # Add a new row at the top
            brick_rows.insert(0, -new_height)
            brick_patterns.insert(0, generate_row_pattern())

    # Check if the music has stopped, and play the next track
    if not pygame.mixer.music.get_busy():
        play_next_track()

    # Fill the screen with a color (optional)
    screen.fill((0, 0, 0))  # Black background

    # Draw bricks
    for row_index, row_y in enumerate(brick_rows):
        for col_index, is_brick in enumerate(brick_patterns[row_index]):
            if is_brick:
                screen.blit(image, (col_index * new_width, row_y))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
