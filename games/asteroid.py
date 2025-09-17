import pygame, random, math
from assets.highscore_manager import HighScoreManager  # Import our high score manager

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Dodger")

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
SAT_COLOR = (255, 200, 50)
AST_COLOR = (200, 50, 50)
POWER_COLOR = (50, 200, 255)
IMMUNE_COLOR = GREEN
BAR_BG = (80, 80, 80)
BAR_FILL_POWER = (50, 200, 255)
BAR_FILL_SHIELD = (0, 255, 100)
GOLD = (255, 215, 0)  # For new high score celebration

# Fonts
font = pygame.font.SysFont("Times New Roman", 28)
big_font = pygame.font.SysFont("Times New Roman", 56)

clock = pygame.time.Clock()

# Initialize high score manager
hsm = HighScoreManager()
high_score = hsm.get_high_score("asteroid")

center = (WIDTH // 2, HEIGHT // 2)


# ---------------- Screens ---------------- #
def start_screen():
    while True:
        screen.fill(BLACK)
        title = big_font.render("Welcome to Asteroid Dodger!", True, GREEN)
        prompt = font.render("Press SPACE to Start or Q to Quit", True, WHITE)
        high_text = font.render(f"Current High Score: {high_score}", True, GOLD)

        screen.blit(title, (WIDTH // 2 - 350, HEIGHT // 2 - 120))
        screen.blit(high_text, (WIDTH // 2 - 150, HEIGHT // 2 - 60))
        screen.blit(prompt, (WIDTH // 2 - 200, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "QUIT"
                elif event.key == pygame.K_SPACE:
                    return "START"


def game_over_screen(score):
    global high_score

    # Check for new high score and save it
    new_high_score = hsm.update_high_score("asteroid", score)
    if new_high_score:
        high_score = score  # Update local variable

    while True:
        screen.fill(BLACK)
        over = big_font.render("GAME OVER!", True, AST_COLOR)
        score_text = font.render(f"Final Score: {score}", True, WHITE)

        # Show different message for new high score
        if new_high_score:
            high_text = font.render(f"NEW HIGH SCORE: {high_score}!", True, GOLD)
            celebration_text = font.render("Outstanding Performance!", True, GOLD)
            screen.blit(celebration_text, (WIDTH // 2 - 130, HEIGHT // 2 - 50))
        else:
            high_text = font.render(f"High Score: {high_score}", True, WHITE)

        restart = font.render("Press SPACE to Restart or Q to Quit", True, WHITE)

        screen.blit(over, (WIDTH // 2 - 170, HEIGHT // 2 - 150))
        screen.blit(score_text, (WIDTH // 2 - 90, HEIGHT // 2 - 20))
        if new_high_score:
            screen.blit(high_text, (WIDTH // 2 - 130, HEIGHT // 2 + 20))
        else:
            screen.blit(high_text, (WIDTH // 2 - 90, HEIGHT // 2 + 20))
        screen.blit(restart, (WIDTH // 2 - 190, HEIGHT // 2 + 60))

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
def spawn_asteroid(speed_mult):
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x, y = random.randint(0, WIDTH), -20
    elif side == "bottom":
        x, y = random.randint(0, WIDTH), HEIGHT + 20
    elif side == "left":
        x, y = -20, random.randint(0, HEIGHT)
    else:
        x, y = WIDTH + 20, random.randint(0, HEIGHT)

    dx, dy = center[0] - x, center[1] - y
    length = math.hypot(dx, dy)
    dx, dy = dx / length, dy / length
    speed = random.uniform(1.5, 2.5) * speed_mult
    return [x, y, dx * speed, dy * speed, random.randint(8, 14)]


def spawn_powerup():
    x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
    return [x, y, pygame.time.get_ticks()]  # position + spawn time


def game_loop():
    sat_x, sat_y = WIDTH // 2, HEIGHT // 2
    base_speed = 4
    sat_speed = base_speed

    asteroids = []
    spawn_timer = 0
    score = 0
    difficulty = 1.0
    max_asteroids = 80

    trail = []
    max_trail = 10

    # Power-up
    powerup = None
    powerup_duration = 5000  # ms
    immune_time = 0  # ms

    running = True
    while running:
        screen.fill(BLACK)
        now = pygame.time.get_ticks()

        # Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

        # Movement
        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_UP]: sat_y -= sat_speed; moved = True
        if keys[pygame.K_DOWN]: sat_y += sat_speed; moved = True
        if keys[pygame.K_LEFT]: sat_x -= sat_speed; moved = True
        if keys[pygame.K_RIGHT]: sat_x += sat_speed; moved = True

        sat_x = max(10, min(WIDTH - 10, sat_x))
        sat_y = max(10, min(HEIGHT - 10, sat_y))

        if moved: score += 1

        # Spawn asteroids
        spawn_timer += 1
        spawn_rate = max(5, 40 - int(difficulty * 5))
        if spawn_timer > spawn_rate and len(asteroids) < max_asteroids:
            spawn_count = min(1 + int(difficulty // 2), 4)
            for _ in range(spawn_count):
                asteroids.append(spawn_asteroid(difficulty))
            spawn_timer = 0

        # Update asteroids
        new_asteroids = []
        for a in asteroids:
            a[0] += a[2];
            a[1] += a[3]
            if -20 <= a[0] <= WIDTH + 20 and -20 <= a[1] <= HEIGHT + 20:
                new_asteroids.append(a)
                pygame.draw.circle(screen, AST_COLOR, (int(a[0]), int(a[1])), a[4])
        asteroids = new_asteroids

        # Spawn power-up
        if powerup is None and random.random() < 0.001:
            powerup = spawn_powerup()

        # Draw power-up and bar
        if powerup:
            elapsed = now - powerup[2]
            if elapsed < powerup_duration:
                radius = 12 * (1 - elapsed / powerup_duration)
                if powerup_duration - elapsed < 1000 and (elapsed // 100) % 2 == 0:
                    color = WHITE
                else:
                    color = POWER_COLOR
                pygame.draw.circle(screen, color, (powerup[0], powerup[1]), max(4, int(radius)))

                # Power-up countdown bar
                bar_w, bar_h = 120, 15
                x_pos, y_pos = WIDTH - bar_w - 20, 20
                pygame.draw.rect(screen, BAR_BG, (x_pos, y_pos, bar_w, bar_h))
                fill = int(bar_w * (1 - elapsed / powerup_duration))
                pygame.draw.rect(screen, BAR_FILL_POWER, (x_pos, y_pos, fill, bar_h))
                num_text = font.render(str(max(1, math.ceil((powerup_duration - elapsed) / 1000))), True, WHITE)
                screen.blit(num_text, (x_pos + bar_w // 2 - 10, y_pos - 5))

                # Collect
                if math.hypot(sat_x - powerup[0], sat_y - powerup[1]) < 18:
                    immune_time = 3000
                    powerup = None
            else:
                powerup = None

        # Collision
        if immune_time <= 0:
            for a in asteroids:
                if math.hypot(sat_x - a[0], sat_y - a[1]) < a[4] + 8:
                    return "GAME_OVER", score
        else:
            immune_time -= clock.get_time()

        # Shield bar
        if immune_time > 0:
            bar_w, bar_h = 120, 15
            x_pos, y_pos = WIDTH - bar_w - 20, 45
            pygame.draw.rect(screen, BAR_BG, (x_pos, y_pos, bar_w, bar_h))
            fill = int(bar_w * (immune_time / 3000))
            pygame.draw.rect(screen, BAR_FILL_SHIELD, (x_pos, y_pos, fill, bar_h))

        # Trail
        trail.append((sat_x, sat_y))
        if len(trail) > max_trail: trail.pop(0)
        for pos in trail: pygame.draw.circle(screen, (0, 150, 0), (int(pos[0]), int(pos[1])), 6)

        # Satellite
        if immune_time > 0: pygame.draw.circle(screen, IMMUNE_COLOR, (int(sat_x), int(sat_y)), 14, 2)
        pygame.draw.circle(screen, SAT_COLOR, (int(sat_x), int(sat_y)), 8)

        # Difficulty
        if score % 200 == 0 and score > 0: difficulty += 0.2; sat_speed = base_speed + difficulty

        # Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        high_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(score_text, (10, 10));
        screen.blit(high_text, (10, 40))

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
        score = result[1]
        choice = game_over_screen(score)
        if choice == "QUIT": break

pygame.quit()