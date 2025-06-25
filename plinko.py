import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modern Plinko Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_BG = (20, 20, 40)
YELLOW = (255, 255, 0)
BRIGHT_SLOT = (200, 200, 255)

# Peg settings
PEG_RADIUS = 5
PEG_SPACING_X = 60
PEG_SPACING_Y = 60
OFFSET_X = WIDTH // 2
OFFSET_Y = 100

# Ball settings
BALL_RADIUS = 8
BALL_COLOR = RED
GRAVITY = 0.2
BOUNCE_DAMPENING = 0.5

# Bin settings
NUM_BINS = 12
BIN_WIDTH = WIDTH // NUM_BINS
BIN_HEIGHT = 100
prize_multipliers = [10, 5, 2, 1, 0.5, 0.5, 0.5, 0.5, 1, 2, 5, 1000]  # More realistic distribution list
prize_values = [f"${multiplier}x" for multiplier in prize_multipliers]

# Betting input
bet_amount = "10.00"
current_winnings = 0.00
user_text = bet_amount
input_active = False

# Generate pegs
pegs = []
for row in range(12):
    for col in range(row + 1):
        x = OFFSET_X + (col - row / 2) * PEG_SPACING_X
        y = OFFSET_Y + row * PEG_SPACING_Y
        pegs.append((x, y))

# Function to draw pegs
def draw_pegs():
    for peg in pegs:
        pygame.draw.circle(screen, WHITE, peg, PEG_RADIUS)

# Function to draw bins
def draw_bins():
    for i in range(NUM_BINS):
        x = i * BIN_WIDTH
        pygame.draw.rect(screen, BRIGHT_SLOT, (x, HEIGHT - BIN_HEIGHT, BIN_WIDTH, BIN_HEIGHT))
        font = pygame.font.Font(None, 24)
        text = font.render(prize_values[i], True, YELLOW)
        screen.blit(text, (x + BIN_WIDTH // 4, HEIGHT - BIN_HEIGHT // 2))

# Ball class with physics
class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = 50
        self.vx = random.uniform(-2, 2)
        self.vy = 0
        self.finished = False

    def update(self):
        global current_winnings
        if not self.finished:
            self.vy += GRAVITY
            self.y += self.vy
            self.x += self.vx

            for peg in pegs:
                if math.hypot(self.x - peg[0], self.y - peg[1]) < PEG_RADIUS + BALL_RADIUS:
                    self.vy *= -BOUNCE_DAMPENING
                    self.vx = random.uniform(-2, 2)
                    self.y -= 5

            if self.y >= HEIGHT - BIN_HEIGHT:
                bin_index = min(range(NUM_BINS), key=lambda i: abs(self.x - (i * BIN_WIDTH + BIN_WIDTH // 2)))
                winnings = float(bet_amount) * prize_multipliers[bin_index]
                current_winnings = winnings
                self.finished = True

    def draw(self):
        pygame.draw.circle(screen, BALL_COLOR, (int(self.x), int(self.y)), BALL_RADIUS)

# Function to display betting info and input
def display_bet_info():
    font = pygame.font.Font(None, 36)
    bet_text = font.render(f"Bet: ${user_text}", True, WHITE)
    winnings_text = font.render(f"Winnings: ${current_winnings:.2f}", True, YELLOW)
    screen.blit(bet_text, (WIDTH // 2 - 50, 20))
    screen.blit(winnings_text, (WIDTH // 2 - 50, 50))

# Main game loop
def main():
    global bet_amount, user_text, input_active
    clock = pygame.time.Clock()
    ball = Ball()
    running = True

    while running:
        screen.fill(DARK_BG)
        draw_pegs()
        draw_bins()
        display_bet_info()
        ball.update()
        ball.draw()
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                input_active = True
                user_text = ""
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if user_text.replace(".", "").isdigit():  # Ensure valid input
                        bet_amount = user_text
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and ball.finished:
                ball = Ball()  # Restart game on SPACE press
    
    pygame.quit()

if __name__ == "__main__":
    main()
