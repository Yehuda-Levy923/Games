# Game_Launcher.py
import pygame
import subprocess
import sys
import os
import random

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Launcher")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
YELLOW = (255, 215, 0)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)

# Fonts
title_font = pygame.font.Font(None, 100)
option_font = pygame.font.Font(None, 60)

# Paths
ASSETS_PATH = "assets"
GAMES_PATH = "games"

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

# Asteroid background
num_asteroids = 80
asteroids = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)] for _ in range(num_asteroids)]

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
    title_rect = title_text.get_rect(center=(WIDTH//2, 100))
    screen.blit(title_text, title_rect)

    # Draw each option with icon
    for i, option in enumerate(options):
        color = BLUE if i == selected else WHITE
        icon = icons[option]
        icon_rect = icon.get_rect(center=(550 - 450*i, 250))
        screen.blit(icon, icon_rect)
        text = option_font.render(option.capitalize(), True, color)
        text_rect = text.get_rect(midleft=(550 - 450*i, 250))
        screen.blit(text, text_rect)


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
                selected = (selected - 1) % len(options)
            elif event.key == pygame.K_LEFT:
                selected = (selected + 1) % len(options)
            elif event.key == pygame.K_RETURN:
                # Launch the selected game
                game_file = f"{options[selected]}.py"
                game_path = os.path.join(GAMES_PATH, game_file)
                if os.path.exists(game_path):
                    subprocess.run([sys.executable, game_path])
                else:
                    print(f"Game {game_file} not found!")
    clock.tick(60)
