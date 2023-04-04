import pygame
import sys
import random
import os
from pygame.locals import *

# Game settings
WIDTH = 640
HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def load_sound(file_name):
    if not pygame.mixer:
        return None
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    try:
        sound = pygame.mixer.Sound(file_path)
    except pygame.error as e:
        print(f"Cannot load sound: {file_name}")
        print(e)
        return None
    return sound

class Snake:
    def __init__(self):
        self.segments = [[GRID_WIDTH // 2, GRID_HEIGHT // 2]]
        self.direction = (1, 0)

    def move(self):
        head_x, head_y = self.segments[0]
        dx, dy = self.direction
        self.segments.insert(0, [head_x + dx, head_y + dy])

        if self.segments[0] == hamster.position:
            hamster.respawn(self)
            if squeak_sound:
                pygame.mixer.Sound.play(squeak_sound)
            global score
            score += 1
        else:
            self.segments.pop()

    def change_direction(self, new_direction):
        if new_direction[0] * self.direction[0] + new_direction[1] * self.direction[1] == 0:
            self.direction = new_direction

class Hamster:
    def __init__(self):
        self.position = [0, 0]
        self.respawn()

    def respawn(self, snake=None):
        while self.position == [0, 0] or (snake and self.position in snake.segments):
            self.position = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]

def check_collision(snake):
    head_x, head_y = snake.segments[0]
    if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
        return True  # Collision with wall
    if snake.segments[0] in snake.segments[1:]:
        return True  # Collision with itself
    return False

def game_over(screen, score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Game Over! Your score: {score}", True, (0, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

# Initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
snake = Snake()
hamster = Hamster()
squeak_sound = load_sound('squeak.wav')
score = 0

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                snake.change_direction((0, -1))
            elif event.key == K_DOWN:
                snake.change_direction((0, 1))
            elif event.key == K_LEFT:
                snake.change_direction((-1, 0))
            elif event.key == K_RIGHT:
                snake.change_direction((1, 0))

    snake.move()
    if check_collision(snake):
        game_over(screen, score)
        pygame.quit()
        sys.exit()

    screen.fill(WHITE)

    for segment in snake.segments:
        pygame.draw.rect(screen, GREEN, Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.draw.rect(screen, RED, Rect(hamster.position[0] * GRID_SIZE, hamster.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    font = pygame.font.Font(None, 24)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (5, 5))

    pygame.display.flip()
    clock.tick(10)