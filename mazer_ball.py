# Mazer Ball

import pygame
import os
import sys

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

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if the music has stopped, and play the next track
    if not pygame.mixer.music.get_busy():
        play_next_track()

    # Fill the screen with a color (optional)
    screen.fill((0, 0, 0))  # Black background

    # Draw bricks
    for h in range(0, 750, 150):
        for i in range(0, 800, 50):
            screen.blit(image, (i, h))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
