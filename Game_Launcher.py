import pygame
import subprocess
import sys
import os
import random
from assets.highscore_manager import HighScoreManager

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Launcher")

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
YELLOW = (255, 215, 0)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)

# Fonts
title_font = pygame.font.Font(None, 100)
option_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 36)

# Initialize high score manager
hsm = HighScoreManager()

# Paths
ASSETS_PATH = "assets"
GAMES_PATH = "games"

# Asteroid background
num_asteroids = 80
asteroids = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)] for _ in range(num_asteroids)]


# Automatically load all PNGs in assets folder
def load_icons():
    icons = {}
    for file in os.listdir(ASSETS_PATH):
        if file.endswith(".png"):
            name = file.split("_icon")[0]
            img = pygame.image.load(os.path.join(ASSETS_PATH, file))
            img = pygame.transform.scale(img, (180, 180))
            icons[name.lower()] = img

    return icons


icons = load_icons()
options = list(icons.keys())
selected = 0


def draw_background():
    screen.fill(BLACK)
    for asteroid in asteroids:
        pygame.draw.circle(screen, GRAY, (asteroid[0], asteroid[1]), asteroid[2])
        asteroid[0] -= 1
        if asteroid[0] < 0:
            asteroid[0] = WIDTH
            asteroid[1] = random.randint(0, HEIGHT)


def draw_menu():
    draw_background()

    # Title
    title_text = title_font.render("Game Launcher", True, YELLOW)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 80))
    screen.blit(title_text, title_rect)

    # High Scores Header
    scores_header = score_font.render("High Scores", True, GOLD)
    scores_rect = scores_header.get_rect(center=(WIDTH // 2, 130))
    screen.blit(scores_header, scores_rect)

    # Draw each option with icon and high score
    for i, option in enumerate(options):
        color = BLUE if i == selected else WHITE

        # Position calculations
        x_pos = 200 + (i * 400)
        y_pos = 300

        # Draw icon
        icon = icons[option]
        icon_rect = icon.get_rect(center=(x_pos, y_pos))
        screen.blit(icon, icon_rect)

        # Draw game name
        text = option_font.render(option.capitalize(), True, color)
        text_rect = text.get_rect(center=(x_pos, y_pos + 120))
        screen.blit(text, text_rect)

        # Draw high score
        high_score = hsm.get_high_score(option)
        score_text = score_font.render(f"Best: {high_score}", True, GOLD if high_score > 0 else WHITE)
        score_rect = score_text.get_rect(center=(x_pos, y_pos + 160))
        screen.blit(score_text, score_rect)

    # Instructions
    instruction_text = score_font.render("Use LEFT/RIGHT arrows to select, ENTER to play", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    screen.blit(instruction_text, instruction_rect)

    # Reset scores instruction
    reset_text = score_font.render("Press R to reset all high scores", True, GRAY)
    reset_rect = reset_text.get_rect(center=(WIDTH // 2, HEIGHT - 30))
    screen.blit(reset_text, reset_rect)

    pygame.display.flip()


# Main loop
clock = pygame.time.Clock()
running = True

while running:
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                selected = (selected + 1) % len(options)
            elif event.key == pygame.K_LEFT:
                selected = (selected - 1) % len(options)
            elif event.key == pygame.K_RETURN:
                # Launch the selected game
                game_file = f"{options[selected]}.py"
                game_path = os.path.join(GAMES_PATH, game_file)
                if os.path.exists(game_path):
                    subprocess.run([sys.executable, game_path])
                    # Refresh high scores after playing
                    hsm = HighScoreManager()  # Reload scores from file
                else:
                    print(f"Game {game_file} not found!")
            elif event.key == pygame.K_r:
                # Reset all high scores
                hsm.reset_all_scores()
                print("All high scores have been reset!")

    clock.tick(60)