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
BRICK_WIDTH, BRICK_HEIGHT = 50, 50
INITIAL_BRICK_SPEED = 50  # Pixels per second
BASE_TIME_INTERVAL = 1000  # Base time interval in milliseconds (1 second)
BRICK_START_DELAY = 3000  # Initial delay before bricks start falling
BRICKS_ON_SCREEN = SCREEN_WIDTH // BRICK_WIDTH
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Directories
ASSETS_DIR = "assets"
MUSIC_DIR = os.path.join(ASSETS_DIR, "sounds", "musics")
EFFECTS_DIR = os.path.join(ASSETS_DIR, "sounds", "effects")
WALL_SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites", "wall")
BALL_SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites", "ball")

# Load resources
music_files = [
    os.path.join(MUSIC_DIR, file)
    for file in os.listdir(MUSIC_DIR)
    if file.endswith(".mp3")
]
brick_image = pygame.image.load(os.path.join(WALL_SPRITES_DIR, "Black_Brick.png"))
brick_image = pygame.transform.scale(brick_image, (BRICK_WIDTH, BRICK_HEIGHT))
ball_image = pygame.image.load(os.path.join(BALL_SPRITES_DIR, "default_red_ball.png"))
ball_size = 40
ball_image = pygame.transform.scale(ball_image, (ball_size, ball_size))

# Ball initial position
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT - (BRICK_HEIGHT * 2)

# Game state variables
brick_rows = []
brick_patterns = []
bricks_falling = False
gap_start = (BRICKS_ON_SCREEN // 2) - 1

# Speeding mechanism variables
speed_multiplier = 1.0
speed_increase_interval = 10000  # 10 seconds in milliseconds
last_speed_increase_time = pygame.time.get_ticks()

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mazer Ball")

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
score_font = pygame.font.Font(None, 48)

# Collision detection variables
game_over = False
brick_speed = 50  # Pixels per second (initial speed)
last_frame_time = pygame.time.get_ticks()

# Initialize score
score = 0
score_increment_interval = 1000  # Score increases every second
last_score_update_time = pygame.time.get_ticks()

# Music functions
def play_next_track():
    """Play the next music track in the playlist."""
    global current_track_index
    if music_files:
        current_track_index = (current_track_index + 1) % len(music_files)
        pygame.mixer.music.load(music_files[current_track_index])
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play()
        print(f"Now playing: {music_files[current_track_index]}")

def play_sound_effect(filename):
    sound_mixer = pygame.mixer.Sound(os.path.join(EFFECTS_DIR, filename))
    sound_mixer.play() 

def play_init_sound(filename="game-countdown.mp3"):
    play_sound_effect(filename)

# Maze generation
def generate_maze_row():
    """Generate a maze row with a random contiguous gap of 0s."""
    global gap_start
    gap_width = 4
    row = [1] * BRICKS_ON_SCREEN
    while True:
        new_gap_start = random.randint(
            max(1, gap_start - 1), min(BRICKS_ON_SCREEN - gap_width - 1, gap_start + 1)
        )
        if new_gap_start != 1 or new_gap_start != BRICKS_ON_SCREEN - gap_width - 1:
            gap_start = new_gap_start
            break
    for i in range(gap_width):
        row[gap_start + i] = 0
    return row

# scoring mechanism
def draw_score():
    """Draw the score on the screen."""
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
    pygame.draw.rect(screen, BLACK, score_rect.inflate(20, 20), border_radius=10)
    screen.blit(score_text, score_rect)

# Function to display Game Over screen
def show_game_over():
    # screen behavior
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    instructions_text = small_font.render("Press any key to restart", True, WHITE)
    final_score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, SCREEN_HEIGHT // 3))
    screen.blit(final_score_text, ((SCREEN_WIDTH - final_score_text.get_width()) // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(instructions_text, ((SCREEN_WIDTH - instructions_text.get_width()) // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    # sound behavior
    pygame.mixer.music.stop()
    play_sound_effect("game-fx-9-40197.mp3")

    # Wait for key press to restart or exit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False
                play_init_sound()
                pygame.time.set_timer(pygame.USEREVENT + 2, BRICK_START_DELAY)

# Initialize timers
current_time_interval = BASE_TIME_INTERVAL
pygame.time.set_timer(pygame.USEREVENT + 1, current_time_interval)
pygame.time.set_timer(pygame.USEREVENT + 2, BRICK_START_DELAY)

# Start the first track
current_track_index = random.randint(0, len(music_files) - 1)  # random selection of the init song

# play the initial starting sound
play_init_sound()

# Game loop
while True:
    running = True
    game_over = False
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT - (BRICK_HEIGHT * 2)
    brick_rows = []
    brick_patterns = []
    bricks_falling = False
    gap_start = (BRICKS_ON_SCREEN // 2) - 1
    speed_multiplier = 1.0
    brick_speed = INITIAL_BRICK_SPEED
    last_speed_increase_time = pygame.time.get_ticks()
    score = 0
    
    while running:
        current_time = pygame.time.get_ticks()
        dt = (current_time - last_frame_time) / 1000.0  # Convert ms to seconds
        last_frame_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.USEREVENT + 2:
                bricks_falling = True
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, _ = event.pos
                ball_x = mouse_x - ball_size // 2
                ball_x = max(0, min(SCREEN_WIDTH - ball_size, ball_x))
                ball_y = SCREEN_HEIGHT // 2 - ball_size // 2
        
        # Check if the music has stopped, and play the next track
        if bricks_falling and not pygame.mixer.music.get_busy():
            play_next_track()

        # Update brick positions
        if bricks_falling:
            brick_rows = [y + brick_speed * dt for y in brick_rows]
            if brick_rows and brick_rows[0] >= SCREEN_HEIGHT:
                brick_rows.pop(0)
                brick_patterns.pop(0)
            if not brick_rows or brick_rows[-1] >= 0:
                brick_rows.append(-BRICK_HEIGHT)
                brick_patterns.append(generate_maze_row())
            # Update score
            if current_time - last_score_update_time >= score_increment_interval / (speed_multiplier*5):
                score += 1
                last_score_update_time = current_time

        # Speeding mechanism
        if current_time - last_speed_increase_time >= speed_increase_interval:
            speed_multiplier += 0.2
            brick_speed = INITIAL_BRICK_SPEED * speed_multiplier
            last_speed_increase_time = current_time
            print(f"Game speed increased! Multiplier: {speed_multiplier:.1f}")
            play_sound_effect("cute-level-up.mp3")

        # Collision detection
        ball_rect = pygame.Rect(ball_x, ball_y, ball_size, ball_size)
        for row_idx, row_y in enumerate(brick_rows):
            for col_idx, is_brick in enumerate(brick_patterns[row_idx]):
                if is_brick:
                    brick_rect = pygame.Rect(col_idx * BRICK_WIDTH, row_y, BRICK_WIDTH, BRICK_HEIGHT)
                    if ball_rect.colliderect(brick_rect):
                        game_over = True
                        print("Collision detected! Game Over!")
                        running = False

        # Draw everything
        screen.fill(BLACK)
        if bricks_falling:
            for row_idx, row_y in enumerate(brick_rows):
                for col_idx, is_brick in enumerate(brick_patterns[row_idx]):
                    if is_brick:
                        screen.blit(brick_image, (col_idx * BRICK_WIDTH, row_y))
        screen.blit(ball_image, (ball_x, SCREEN_HEIGHT // 2 - ball_size // 2))
        draw_score()
        pygame.display.flip()

    show_game_over()
