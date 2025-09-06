from typing import final

import pygame
import random
import time

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 600
FPS = 120
TARGET_RADIUS = 25
GAME_DURATION = 30  # seconds
MAX_TARGETS = 5
FEEDBACK_DURATION = 0.15  # seconds

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GET A1M")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Hide default cursor
pygame.mouse.set_visible(False)


# --- Target Class ---
class Target:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(TARGET_RADIUS, WIDTH - TARGET_RADIUS)
        self.y = random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS)
        self.hit_time = None  # Time when it was last hit

    def draw(self, surface):
        # Animate hit flash
        if self.hit_time and time.time() - self.hit_time < FEEDBACK_DURATION:
            pygame.draw.circle(surface, WHITE, (self.x, self.y), TARGET_RADIUS + 5)
        else:
            pygame.draw.circle(surface, RED, (self.x, self.y), TARGET_RADIUS)

    def is_hit(self, mouse_pos):
        dist = ((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2) ** 0.5
        return dist <= TARGET_RADIUS


# --- Feedback Marker Class ---
class Feedback:
    def __init__(self, pos, result):
        self.x, self.y = pos
        self.result = result  # 'hit' or 'miss'
        self.start_time = time.time()

    def draw(self, surface):
        if time.time() - self.start_time > FEEDBACK_DURATION:
            return False  # remove it
        color = GREEN if self.result == 'hit' else RED
        symbol = "✔" if self.result == 'hit' else "✖"
        text = font.render(symbol, True, color)
        screen.blit(text, (self.x - 10, self.y - 10))
        return True


# Game variables
score = 0
shots_fired = 0
start_time = time.time()
targets = [Target() for _ in range(MAX_TARGETS)]
feedbacks = []  # click feedback

# Main loop
running = True
while running:
    screen.fill(BLACK)

    # Timer
    elapsed_time = time.time() - start_time
    time_left = max(0, GAME_DURATION - elapsed_time)

    if time_left <= 0:
        running = False

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse click logic
        if event.type == pygame.MOUSEBUTTONDOWN:
            shots_fired += 1
            mouse_pos = pygame.mouse.get_pos()

            hit = False
            for target in targets:
                if target.is_hit(mouse_pos):
                    score += 1
                    target.hit_time = time.time()
                    target.reset()
                    hit = True
                    break  # only 1 hit per click

            feedbacks.append(Feedback(mouse_pos, 'hit' if hit else 'miss'))

    # Draw targets
    for target in targets:
        target.draw(screen)

    # Accuracy
    accuracy = (score / shots_fired) * 100 if shots_fired > 0 else 0.0

    # Draw UI
    ui_text = font.render(f"Score: {score}   Accuracy: {accuracy:.1f}%   Time Left: {int(time_left)}s", True, WHITE)
    screen.blit(ui_text, (10, 10))

    # Draw custom crosshair
    mouse_x, mouse_y = pygame.mouse.get_pos()
    crosshair_length = 4
    crosshair_thickness = 3

    pygame.draw.line(screen, GREEN,
                     (mouse_x - crosshair_length, mouse_y),
                     (mouse_x + crosshair_length, mouse_y),
                     crosshair_thickness)

    pygame.draw.line(screen, GREEN,
                     (mouse_x, mouse_y - crosshair_length),
                     (mouse_x, mouse_y + crosshair_length),
                     crosshair_thickness)

    pygame.display.flip()
    clock.tick(FPS)

# Game Over Screen
screen.fill(BLACK)
missed_hits = shots_fired - score
total_hits = shots_fired

total_hits_text=font.render(f"Total Hits: {total_hits}",True, GREEN)
hits_text = font.render(f"Perfect Hits: {score}", True, GREEN)
miss_text = font.render(f"Missed Hits: {missed_hits}", True, GREEN)
final_accuracy_text = font.render(f"Accuracy: {accuracy:.1f}%", True, GREEN)

screen.blit(total_hits_text,(WIDTH // 2 - total_hits_text.get_width() // 2, HEIGHT // 2 - 120))
screen.blit(hits_text, (WIDTH // 2 - hits_text.get_width() // 2, HEIGHT // 2 - 60))
screen.blit(miss_text, (WIDTH // 2 - miss_text.get_width() // 2, HEIGHT // 2 - 0))
screen.blit(final_accuracy_text, (WIDTH // 2 - final_accuracy_text.get_width() // 2, HEIGHT // 2 +60))

pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()



