# Mazer Ball

import pygame
import os
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BRICK_WIDTH, BRICK_HEIGHT = 50, 50  # Brick dimensions
BRICK_SPEED = 50  # Pixels per second
TIME_INTERVAL = 1000  # Time interval in milliseconds (1 second)
BRICK_START_DELAY = 3000  # Delay before bricks start falling
BRICKS_ON_SCREEN = SCREEN_WIDTH // BRICK_WIDTH  # Number of bricks visible horizontally
BLACK = (0, 0, 0)  # Background color

# Directories
ASSETS_DIR = "assets"
MUSIC_DIR = os.path.join(ASSETS_DIR, "musics")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites", "wall")

# Load music files
music_files = [
    os.path.join(MUSIC_DIR, file)
    for file in os.listdir(MUSIC_DIR)
    if file.endswith(".mp3")
]
current_track_index = -1

# Load and resize brick image
brick_image = pygame.image.load(os.path.join(SPRITES_DIR, "Black_Brick.png"))
brick_image = pygame.transform.scale(brick_image, (BRICK_WIDTH, BRICK_HEIGHT))

# Game state variables
brick_rows = []  # Tracks the vertical positions of rows
brick_patterns = []  # Stores the brick patterns
prev_gaps = [random.randint(0, 1) for _ in range(BRICKS_ON_SCREEN + 1)]  # Initial gap pattern
bricks_falling = False  # Flag for brick movement

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mazer Ball")


# Music functions
def play_next_track():
    """Play the next music track in the playlist."""
    global current_track_index
    if music_files:
        current_track_index = (current_track_index + 1) % len(music_files)
        pygame.mixer.music.load(music_files[current_track_index])
        pygame.mixer.music.play()
        print(f"Now playing: {music_files[current_track_index]}")


# Maze generation
gap_start = BRICKS_ON_SCREEN // 2
def generate_maze_row():
    """
    Generate a maze row with a random contiguous gap of 0s.
    Ensures the gap overlaps at least two 0s from the previous row.
    Returns:
        list: A row of 1s (bricks) with a gap of 0s.
    """
    global gap_start
    gap_width = 3  # Width of the gap (number of 0s)
    row = [1] * BRICKS_ON_SCREEN  # Start with all bricks (1s)

    # Randomize the new gap position
    while True:
        new_gap_start = random.randint(
            max(1, gap_start - 1), min(BRICKS_ON_SCREEN - gap_width - 1, gap_start + 1)
        )
        # Ensure valid overlap and avoid invalid edges
        if new_gap_start != 1 or new_gap_start != BRICKS_ON_SCREEN - gap_width - 1:
            gap_start = new_gap_start
            break

    # Create the gap
    for i in range(gap_width):
        row[gap_start + i] = 0

    print(row)
    return row


# Initialize timers
pygame.time.set_timer(pygame.USEREVENT + 1, TIME_INTERVAL)  # Brick movement
pygame.time.set_timer(pygame.USEREVENT + 2, BRICK_START_DELAY)  # Start delay

# Start the first track
play_next_track()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT + 1 and bricks_falling:
            # Move rows downward
            brick_rows = [y + BRICK_HEIGHT for y in brick_rows]

            # Remove off-screen rows
            if brick_rows and brick_rows[0] >= SCREEN_HEIGHT:
                brick_rows.pop(0)
                brick_patterns.pop(0)

            # Add a new row at the top
            brick_rows.insert(0, -BRICK_HEIGHT)
            brick_patterns.insert(0, generate_maze_row())
        elif event.type == pygame.USEREVENT + 2:
            bricks_falling = True

    # Play next track if the current one stops
    if not pygame.mixer.music.get_busy():
        play_next_track()

    # Draw everything
    screen.fill(BLACK)  # Clear the screen
    if bricks_falling:
        for row_idx, row_y in enumerate(brick_rows):
            for col_idx, is_brick in enumerate(brick_patterns[row_idx]):
                if is_brick:
                    screen.blit(brick_image, (col_idx * BRICK_WIDTH, row_y))

    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()
