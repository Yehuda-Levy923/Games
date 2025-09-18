import pygame
import random
import os
from assets.highscore_manager import HighScoreManager

# Initialize pygame
pygame.init()

# Paths
ASSETS_PATH = "assets"

# Screen settings
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
PLAYABLE_X = range(1, GRID_WIDTH - 1)
PLAYABLE_Y = range(1, GRID_HEIGHT - 1)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colours
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
BROWN =  (137 ,81 ,41)

# Fonts and clock
clock = pygame.time.Clock()
FPS = 10
font = pygame.font.SysFont("Times New Roman", 24)
big_font = pygame.font.SysFont("Times New Roman", 72)

# Initialize high score manager
hsm = HighScoreManager()
high_score = hsm.get_high_score("snake")

# Drawing the game border on the board
def draw_border():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if x == 0 or x == GRID_WIDTH - 1 or y == 0 or y == GRID_HEIGHT - 1:
                pygame.draw.rect(screen, BROWN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Drawing the game border bricks on the board
def draw_grid():
    # Vertical lines
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    # Horizontal lines
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

# Drawing the snake on the board
def draw_snake(snake):
    for x, y in snake:
        pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))


# Drawing the food on the board
def draw_food(x, y):
    pygame.draw.rect(screen, RED, (x, y, CELL_SIZE, CELL_SIZE))


# Drawing the score on the game-screen
def draw_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(high_text, (10, 40))

# Automatically load the PNG in assets folder
def load_icon():
    icons = {}
    for file in os.listdir(ASSETS_PATH):
        if file.endswith(".png"):
            name = file.split("_icon")[0]
            img = pygame.image.load(os.path.join(ASSETS_PATH, file))
            img = pygame.transform.scale(img, (500, 500))
            icons[name.lower()] = img

    return icons

icons = load_icon()
icon = icons["snake"].convert_alpha()
icon.set_alpha(128)

# Start screen
def start_screen():
    while True:
        screen.fill(BLACK)
        icon_rect = icon.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(icon, icon_rect)

        title_text = big_font.render("Welcome to Snake!", True, GREEN)
        prompt_text = font.render("Press SPACE to Start or Q to Quit", True, WHITE)
        high_text = font.render(f"Current High Score: {high_score}", True, GOLD)

        screen.blit(title_text, (WIDTH // 2 - 275, HEIGHT // 2 - 200))
        screen.blit(high_text, (WIDTH // 2 - 135, HEIGHT // 2 - 60))
        screen.blit(prompt_text, (WIDTH // 2 - 180, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "QUIT"
                elif event.key == pygame.K_SPACE:
                    return "START"


# The game itself
def game_loop():
    # Snake setup
    snake = [(100, 100), (90, 100), (80, 100)]
    direction = "RIGHT"

    # Food setup
    food_x = random.choice(PLAYABLE_X) * CELL_SIZE
    food_y = random.choice(PLAYABLE_Y) * CELL_SIZE

    running = True
    while running:
        screen.fill(BLACK)
        draw_border()
        draw_grid()

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != "DOWN":
                    direction = "UP"
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != "UP":
                    direction = "DOWN"
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != "RIGHT":
                    direction = "LEFT"
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != "LEFT":
                    direction = "RIGHT"

        # Move snake
        head_x, head_y = snake[0]
        if direction == "UP":
            head_y -= CELL_SIZE
        elif direction == "DOWN":
            head_y += CELL_SIZE
        elif direction == "LEFT":
            head_x -= CELL_SIZE
        elif direction == "RIGHT":
            head_x += CELL_SIZE

        new_head = (head_x, head_y)

        # Check collisions
        if (head_x // CELL_SIZE not in PLAYABLE_X or
                head_y // CELL_SIZE not in PLAYABLE_Y or
                new_head in snake):
            return "GAME_OVER", len(snake) - 3

        # Check food
        if head_x == food_x and head_y == food_y:
            snake.insert(0, new_head)
            while True:
                food_x = random.choice(PLAYABLE_X) * CELL_SIZE
                food_y = random.choice(PLAYABLE_Y) * CELL_SIZE
                if (food_x, food_y) not in snake:
                    break
        else:
            snake.insert(0, new_head)
            snake.pop()

        # Draw
        draw_snake(snake)
        draw_food(food_x, food_y)
        score = len(snake) - 3
        draw_score(score)

        # Speed up over time
        fps = min(30, 10 + score // 2)
        pygame.display.flip()
        clock.tick(fps)


# Game over screen for when you die
def game_over_screen(score):
    global high_score

    # Check for new high score and save it
    new_high_score = hsm.update_high_score("snake", score)
    if new_high_score:
        high_score = score  # Update local variable

    while True:
        screen.fill(BLACK)
        icon_rect = icon.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(icon, icon_rect)
        game_over_text = big_font.render("GAME OVER!", True, RED)
        score_text = font.render(f"Final Score: {score}", True, WHITE)

        # Show different message for new high score
        if new_high_score:
            high_text = font.render(f"NEW HIGH SCORE: {high_score}!", True, GOLD)
            celebration_text = font.render("Congratulations!", True, GOLD)
            screen.blit(celebration_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        else:
            high_text = font.render(f"High Score: {high_score}", True, WHITE)

        restart_text = font.render("Press Space to Restart or Q to Quit", True, WHITE)

        screen.blit(game_over_text, (WIDTH // 2 - 225, HEIGHT // 2 - 150))
        screen.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
        if new_high_score:
            screen.blit(high_text, (WIDTH // 2 - 115, HEIGHT // 2 + 10))
        else:
            screen.blit(high_text, (WIDTH // 2 - 80, HEIGHT // 2 + 10))
        screen.blit(restart_text, (WIDTH // 2 - 180, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "QUIT"
                elif event.key == pygame.K_SPACE:
                    return "RESTART"


# Main control loop
while True:
    choice = start_screen()
    if choice == "QUIT":
        break

    result = game_loop()
    if result == "QUIT":
        break
    elif isinstance(result, tuple) and result[0] == "GAME_OVER":
        score = result[1]
        choice = game_over_screen(score)
        if choice == "QUIT":
            break

pygame.quit()