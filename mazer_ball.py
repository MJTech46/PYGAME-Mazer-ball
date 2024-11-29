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
bricks_on_screen = screen_width // new_width  # Number of bricks visible on the screen

# Game initialization
brick_rows = []  # No rows initially
brick_patterns = []  # Patterns for bricks
brick_start_delay = 3000  # Delay in milliseconds before the bricks start falling
bricks_falling = False  # Flag to start brick generation
prev_gapes = [1 if random.random() > 0.5 else 0 for _ in range(bricks_on_screen+1)]
print(prev_gapes)
print(bricks_on_screen)

# Function to generate a maze row with a random gap
def generate_maze_row():
    maze_row = []
    for i in range(bricks_on_screen):
        if random.random() > 0.5:
            if not (prev_gapes[i-1] and prev_gapes[i] and prev_gapes[i+1]): 
                maze_row.append(1)
            else:
                maze_row.append(0)
        else:
            maze_row.append(0)
    # prev_gapes = maze_row + [1]       # ERROR HERE
    print(maze_row)
    return maze_row 


# Set up a timer for brick movement
pygame.time.set_timer(pygame.USEREVENT + 1, time_interval)
pygame.time.set_timer(pygame.USEREVENT + 2, brick_start_delay)  # Timer for brick start delay

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT + 1 and bricks_falling:
            # Move all rows downward
            brick_rows = [y + new_height for y in brick_rows]

            # Remove rows that move off-screen
            if brick_rows and brick_rows[0] >= screen_height:
                brick_rows.pop(0)
                brick_patterns.pop(0)

            # Add a new maze row at the top
            brick_rows.insert(0, -new_height)
            brick_patterns.insert(0, generate_maze_row())
        elif event.type == pygame.USEREVENT + 2:
            # Start generating bricks after delay
            bricks_falling = True

    # Check if the music has stopped, and play the next track
    if not pygame.mixer.music.get_busy():
        play_next_track()

    # Fill the screen with a color (optional)
    screen.fill((0, 0, 0))  # Black background

    # Draw bricks
    if bricks_falling:
        for row_index, row_y in enumerate(brick_rows):
            for col_index, is_brick in enumerate(brick_patterns[row_index]):
                if is_brick:
                    screen.blit(image, (col_index * new_width, row_y))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
