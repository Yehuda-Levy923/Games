import pygame, random, os
from assets.highscore_manager import HighScoreManager

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Initialize high score manager
hsm = HighScoreManager()
high_score = hsm.get_high_score("pong")

# Paths
BASE_PATH = os.path.dirname(__file__)
ASSETS_PATH = os.path.join(BASE_PATH, "..", "assets")
ASSETS_PATH = os.path.abspath(ASSETS_PATH)

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

center = (WIDTH // 2, HEIGHT // 2)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PLAYABLE_X = range(5,795)
PLAYABLE_Y = range(5,595)
TARGET_SCORE = 3
current_rally = 0

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
        high_score = score  # Update local variable

    while True:
        screen.fill(BLACK)

        game_over_text = big_font.render(f"GAME OVER!", True, RED)
        winner_text = big_font.render(f"{winner} wins!", True, YELLOW)
        score_text = font.render(f"Final Score: {p1_score} - {p2_score}", True, WHITE)
        high_rally_text = font.render(f"Congratulations New Longest Rally: {high_score} hits", True, YELLOW)
        rally_text = font.render(f"Longest Rally: {high_score} hits", True, WHITE)
        restart_text = font.render("Press SPACE to Restart or Q to Quit", True, WHITE)

        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//4))
        screen.blit(winner_text, (WIDTH//2 - winner_text.get_width()/2, HEIGHT//3))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        if new_high_score:
            screen.blit(high_rally_text, (WIDTH//2 - high_rally_text.get_width()//2, HEIGHT//2 + 40))
        else:
            screen.blit(rally_text, (WIDTH//2 - rally_text.get_width()//2, HEIGHT//2 + 40))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 80))

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
    for beginning_of_line in range(0, HEIGHT, 50):
        pygame.draw.line(screen, GRAY, (WIDTH // 2, beginning_of_line), (WIDTH // 2, beginning_of_line + 25), 5)

def draw_border():
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), width=5)

def draw_ball(ball_location):
    pygame.draw.circle(screen, GREEN, ball_location, 10)

def draw_paddle(x, y, color):
    pygame.draw.rect(screen, color, (x, y, PADDLE_WIDTH, PADDLE_HEIGHT))

def game_loop():
    global current_rally, high_score
    paddle1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    paddle2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    paddle_speed = 6

    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_dx, ball_dy = 4, 4
    p1_score, p2_score = 0, 0

    running = True
    while running:
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

        paddle1_y = max(0, min(HEIGHT - PADDLE_HEIGHT, paddle1_y))
        paddle2_y = max(0, min(HEIGHT - PADDLE_HEIGHT, paddle2_y))

        ball_x += ball_dx
        ball_y += ball_dy

        if ball_y <= 0 or ball_y >= HEIGHT:
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

        if ball_rect.left <= min(PLAYABLE_X):
            p2_score += 1
            if current_rally > high_score:
                high_score = current_rally
            current_rally = 0
            if p2_score >= TARGET_SCORE:
                return "GAME_OVER", p1_score, p2_score, "Player 2", high_score
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx = abs(ball_dx)
            ball_dy = random.choice([-4, -3, -2, 2, 3, 4])
        elif ball_rect.right >= max(PLAYABLE_X):
            p1_score += 1
            if current_rally > high_score:
                high_score = current_rally
            current_rally = 0
            if p1_score >= TARGET_SCORE:
                return "GAME_OVER", p1_score, p2_score, "Player 1", high_score
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx = -abs(ball_dx)
            ball_dy = random.choice([-4, -3, -2, 2, 3, 4])

        draw_board()
        draw_border()
        draw_ball((ball_x, ball_y))
        draw_paddle(20, paddle1_y, RED)
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
