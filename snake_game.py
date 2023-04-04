import sys
import pygame
from pygame.locals import *
import random

# Game settings / Constants
WIDTH = 640
HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
SPEED = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
LIGHT_BROWN = (210, 180, 140)

# Snake class
class Snake:
    ...

# Hamster class
class Hamster:
    ...

def game_loop(screen, clock):
    ...

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake 'n Hamster!")
    clock = pygame.time.Clock()

    # Splash screen function
    def splash_screen():
        running = True
        # Create font and render text
        font = pygame.font.Font(None, 36)
        text = font.render("Snake 'n Hamster!", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))

        # Create New Game and Exit buttons
        new_game_button = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 - 30, 160, 60)
        exit_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 40, 120, 40)

        while running:
            for event in pygame.event.get():
                # Handle quit and key events
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                # Check for mouse button clicks on the buttons
                elif event.type == MOUSEBUTTONDOWN:
                    if new_game_button.collidepoint(event.pos):
                        running = False
                    elif exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            # Draw the screen, text, and buttons
            screen.fill(BLACK)
            screen.blit(text, text_rect)
            pygame.draw.rect(screen, GREEN, new_game_button, 2)
            pygame.draw.rect(screen, GREEN, exit_button, 2)

            # Draw button labels
            new_game_text = font.render("New Game", True, WHITE)
            new_game_text_rect = new_game_text.get_rect(center=new_game_button.center)
            screen.blit(new_game_text, new_game_text_rect)

            exit_text = font.render("Exit", True, WHITE)
            exit_text_rect = exit_text.get_rect(center=exit_button.center)
            screen.blit(exit_text, exit_text_rect)

            pygame.display.flip()
            clock.tick(30)

    # Show splash screen and start the game loop
    splash_screen()
    game_loop(screen, clock)

if __name__ == "__main__":
    main()

# Load sound function
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

# Snake class
class Snake:
    def __init__(self):
        self.segments = [[GRID_WIDTH // 2, GRID_HEIGHT // 2]]
        self.direction = (1, 0)

    # Move snake
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

    # Change snake direction
    def change_direction(self, new_direction):
        if new_direction[0] * self.direction[0] + new_direction[1] * self.direction[1] == 0:
            self.direction = new_direction

# Hamster class
class Hamster:
    def __init__(self):
        self.position = [0, 0]
        self.respawn()

    # Respawn hamster
    def respawn(self, snake=None):
        while self.position == [0, 0] or (snake and self.position in snake.segments):
            self.position = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]

# Check for collisions
def check_collision(snake):
    head_x, head_y = snake.segments[0]
    if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
        return True  # Collision with wall
    if snake.segments[0] in snake.segments[1:]:
        return True  # Collision with itself
    return False

# Game over screen
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
    # Event handling
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

    # Move the snake
    snake.move()

    # Check for collisions
    if check_collision(snake):
        game_over(screen, score)
        pygame.quit()
        sys.exit()

    # Clear screen
    screen.fill(LIGHT_BROWN)

    # Draw snake segments
    for segment in snake.segments:
        pygame.draw.rect(screen, GREEN, Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw snake eyes on the head
    eye_size = GRID_SIZE // 4
    eye_offset = GRID_SIZE // 4
    eye1_rect = Rect(snake.segments[0][0] * GRID_SIZE + eye_offset, snake.segments[0][1] * GRID_SIZE + eye_offset, eye_size, eye_size)
    eye2_rect = Rect(snake.segments[0][0] * GRID_SIZE + GRID_SIZE - eye_offset * 1.5, snake.segments[0][1] * GRID_SIZE + eye_offset, eye_size, eye_size)
    dark_green = (0, 100, 0)
    pygame.draw.rect(screen, dark_green, eye1_rect)
    pygame.draw.rect(screen, dark_green, eye2_rect)

    # Draw hamster body
    hamster_rect = Rect(hamster.position[0] * GRID_SIZE, hamster.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, RED, hamster_rect)

    # Draw hamster ears
    ear_size = GRID_SIZE // 4
    ear1_rect = Rect(hamster_rect.left, hamster_rect.top - ear_size, ear_size, ear_size)
    ear2_rect = Rect(hamster_rect.right - ear_size, hamster_rect.top - ear_size, ear_size, ear_size)
    pygame.draw.rect(screen, RED, ear1_rect)
    pygame.draw.rect(screen, RED, ear2_rect)

    # Draw hamster eyes
    eye_size = GRID_SIZE // 4
    eye_offset = GRID_SIZE // 4
    eye1_rect = Rect(hamster_rect.left + eye_offset, hamster_rect.top + eye_offset, eye_size, eye_size)
    eye2_rect = Rect(hamster_rect.right - eye_offset * 1.5, hamster_rect.top + eye_offset, eye_size, eye_size)
    pygame.draw.rect(screen, (0, 0, 0), eye1_rect)
    pygame.draw.rect(screen, (0, 0, 0), eye2_rect)

    # Display score
    font = pygame.font.Font(None, 24)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (5, 5))

    # Update display
    pygame.display.flip()
    clock.tick(10)
