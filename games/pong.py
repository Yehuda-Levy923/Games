import pygame, random, os
from assets.highscore_manager import HighScoreManager

# ---------------- Setup ---------------- #
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# High-score manager
hsm = HighScoreManager()
high_score = hsm.get_high_score("pong")

# Paths
BASE_PATH = os.path.dirname(__file__)
ASSETS_PATH = os.path.abspath(os.path.join(BASE_PATH, "..", "assets"))

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)

# Fonts
font = pygame.font.SysFont("Times New Roman", 28)
big_font = pygame.font.SysFont("Times New Roman", 56)

clock = pygame.time.Clock()

# Game constants
BORDER_WIDTH = 5
BALL_RADIUS = 10
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
TARGET_SCORE = 3
current_rally = 0
longest_rally_game = 0

# ---------------- Screens ---------------- #

def load_icon():
    icons = {}
    for file in os.listdir(ASSETS_PATH):
        if file.endswith(".png"):
            name = file.split("_icon")[0]
            img = pygame.image.load(os.path.join(ASSETS_PATH, file))
            img = pygame.transform.scale(img, (600, 500))
            icons[name.lower()] = img
    return icons

icons = load_icon()
icon = icons["pong"].convert_alpha()
icon.set_alpha(128)


def start_screen():
    while True:
        screen.fill(BLACK)
        icon_rect = icon.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(icon, icon_rect)

        title_text = big_font.render("Welcome to Pong!", True, GREEN)
        prompt_text = font.render("Press SPACE to Start or Q to Quit", True, WHITE)
        rally_text = font.render(f"Longest Rally: {high_score}", True, YELLOW)


        screen.blit(title_text, (WIDTH // 2 - 200, HEIGHT // 2 - 200))
        screen.blit(rally_text, (WIDTH // 2 - 100, HEIGHT // 2 - 60))
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


def game_over_screen(winner, p1_score, p2_score, score):
    global high_score

    # Check for new high score and save it
    new_high_score = hsm.update_high_score("pong", score)
    if new_high_score:
        high_score = score

    while True:
        screen.fill(BLACK)

        game_over_text = big_font.render(f"GAME OVER!", True, RED)
        winner_text = big_font.render(f"{winner} wins!", True, YELLOW)
        score_text = font.render(f"Final Score: {p1_score} - {p2_score}", True, WHITE)

        this_game_text = font.render(f"This Game's Longest Rally: {score} hits", True, WHITE)
        if new_high_score:
            high_rally_text = font.render(f"Congratulations New All-Time Longest Rally: {high_score} hits", True, YELLOW)
        else:
            high_rally_text = font.render(f"All-Time Longest Rally: {high_score} hits", True, WHITE)

        restart_text = font.render("Press SPACE to Restart or Q to Quit", True, WHITE)

        screen.blit(game_over_text,(WIDTH//2 - game_over_text.get_width()//2, HEIGHT//4))
        screen.blit(winner_text,(WIDTH//2 - winner_text.get_width()//2,    HEIGHT//3))
        screen.blit(score_text,(WIDTH//2 - score_text.get_width()//2,     HEIGHT//2))
        screen.blit(this_game_text,(WIDTH//2 - this_game_text.get_width()//2, HEIGHT//2 + 40))
        screen.blit(high_rally_text,(WIDTH//2 - high_rally_text.get_width()//2,HEIGHT//2 + 80))
        screen.blit(restart_text,(WIDTH//2 - restart_text.get_width()//2,   HEIGHT//2 + 120))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "QUIT"
                elif event.key == pygame.K_SPACE:
                    return "RESTART"

# ---------------- Gameplay ---------------- #

def draw_board():
    screen.fill(BLACK)
    for start in range(0, HEIGHT, 50):
        pygame.draw.line(screen, GRAY,(WIDTH // 2, start),(WIDTH // 2, start + 25), 5)

def draw_border():
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), width=BORDER_WIDTH)

def draw_ball(ball_x, ball_y):
    pygame.draw.circle(screen, GREEN, (int(ball_x), int(ball_y)), BALL_RADIUS)

def draw_paddle(x, y, color):
    pygame.draw.rect(screen, color, (x, y, PADDLE_WIDTH, PADDLE_HEIGHT))

def game_loop():
    global current_rally, high_score, longest_rally_game
    longest_rally_game = 0
    paddle1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    paddle2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2

    ball_dx, ball_dy = 1, 1
    base_speed = 4
    p1_score, p2_score = 0, 0
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2

    running = True
    while running:
        paddle_speed = min(9, 6 + current_rally * 0.1)
        ball_speed = min(10, base_speed + current_rally * 0.1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle1_y -= paddle_speed
        if keys[pygame.K_s]:
            paddle1_y += paddle_speed
        if keys[pygame.K_UP]:
            paddle2_y -= paddle_speed
        if keys[pygame.K_DOWN]:
            paddle2_y += paddle_speed

        paddle1_y = max(BORDER_WIDTH, min(HEIGHT - BORDER_WIDTH - PADDLE_HEIGHT, paddle1_y))
        paddle2_y = max(BORDER_WIDTH, min(HEIGHT - BORDER_WIDTH - PADDLE_HEIGHT, paddle2_y))


        ball_x += ball_dx * ball_speed
        ball_y += ball_dy * ball_speed


        if ball_y - BALL_RADIUS <= BORDER_WIDTH or ball_y + BALL_RADIUS >= HEIGHT - BORDER_WIDTH:
            ball_dy *= -1

        paddle1_rect = pygame.Rect(20, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        paddle2_rect = pygame.Rect(WIDTH - 25, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball_rect = pygame.Rect(ball_x-10, ball_y-10, 20, 20)

        if ball_rect.colliderect(paddle1_rect):
            ball_dx = abs(ball_dx)
            current_rally += 1
        elif ball_rect.colliderect(paddle2_rect):
            ball_dx = -abs(ball_dx)
            current_rally += 1


        if ball_rect.left <= BORDER_WIDTH:
            p2_score += 1
            if current_rally > longest_rally_game:
                longest_rally_game = current_rally
            if current_rally > high_score:
                high_score = current_rally
            current_rally = 0
            if p2_score >= TARGET_SCORE:
                return "GAME_OVER", p1_score, p2_score, "Player 2", longest_rally_game
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx = abs(ball_dx)
            ball_dy = random.choice([-1, 1])

        elif ball_rect.right >= WIDTH - BORDER_WIDTH:
            p1_score += 1
            if current_rally > longest_rally_game:
                longest_rally_game = current_rally
            if current_rally > high_score:
                high_score = current_rally
            current_rally = 0
            if p1_score >= TARGET_SCORE:
                return "GAME_OVER", p1_score, p2_score, "Player 1", longest_rally_game
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx = -abs(ball_dx)
            ball_dy = random.choice([-1, 1])

        draw_board()
        draw_border()
        draw_ball(ball_x, ball_y)
        draw_paddle(15, paddle1_y, RED)
        draw_paddle(WIDTH - 25, paddle2_y, BLUE)

        score_text = big_font.render(f"{p1_score} - {p2_score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(60)


# ---------------- Main Loop ---------------- #
while True:
    choice = start_screen()
    if choice == "QUIT": break

    result = game_loop()
    if result == "QUIT":
        break
    elif isinstance(result, tuple) and result[0] == "GAME_OVER":
        _, p1, p2, winner, rally = result
        choice = game_over_screen(winner, p1, p2, rally)
        if choice == "QUIT": break

pygame.quit()
