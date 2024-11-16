import pygame
import json
import re
from datetime import datetime

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = SCREEN_WIDTH // BRICK_COLS
BRICK_HEIGHT = 30
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_SIZE = 15

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Decorator to measure function execution time
def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        print(f"{func.__name__} executed in {end_time - start_time}")
        return result
    return wrapper

# Base class for game objects
class GameObject:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Paddle class
class Paddle(GameObject):
    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= 10
        elif direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += 10

# Ball class
class Ball(GameObject):
    def __init__(self, x, y, size, color, dx, dy):
        super().__init__(x, y, size, size, color)
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def bounce(self, axis):
        if axis == "x":
            self.dx = -self.dx
        elif axis == "y":
            self.dy = -self.dy

# Brick class with difficulty levels
class Brick(GameObject):
    def __init__(self, x, y, width, height, color, points):
        super().__init__(x, y, width, height, color)
        self.points = points

    def __lt__(self, other):
        return self.points < other.points  # Compare bricks by points (difficulty)

# Game engine class
class BreakoutGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Breakout Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paddle = Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT, GREEN)
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BLUE, 5, -5)
        self.bricks = self.generate_bricks()
        self.score = 0
        self.start_time = None

    @measure_time
    def generate_bricks(self):
        return [
            Brick(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH - 2, BRICK_HEIGHT - 2, RED, (row + 1) * 10)
            for row in range(BRICK_ROWS)
            for col in range(BRICK_COLS)
        ]

    def save_score(self, player_name):
        try:
            # Validate player name with regex
            if not re.match(r"^[A-Za-z0-9_]{3,15}$", player_name):
                raise ValueError("Invalid player name. Must be 3-15 characters, letters, digits, or underscores.")
            # Save score to a file
            with open("high_scores.json", "a") as file:
                json.dump({"player": player_name, "score": self.score, "date": str(datetime.now())}, file)
                file.write("\n")
        except Exception as e:
            print(f"Error saving score: {e}")

    def play(self):
        self.start_time = datetime.now()
        while self.running:
            self.screen.fill(WHITE)
            self.handle_events()
            self.update_game_state()
            self.draw_objects()
            pygame.display.flip()
            self.clock.tick(60)
        print(f"Game session lasted: {datetime.now() - self.start_time}")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.move("left")
        if keys[pygame.K_RIGHT]:
            self.paddle.move("right")

    def update_game_state(self):
        self.ball.move()

        # Ball collision with walls
        if self.ball.x <= 0 or self.ball.x >= SCREEN_WIDTH - self.ball.width:
            self.ball.bounce("x")
        if self.ball.y <= 0:
            self.ball.bounce("y")

        # Ball collision with paddle
        if pygame.Rect(self.ball.x, self.ball.y, self.ball.width, self.ball.height).colliderect(
            pygame.Rect(self.paddle.x, self.paddle.y, self.paddle.width, self.paddle.height)
        ):
            self.ball.bounce("y")

        # Ball collision with bricks
        for brick in self.bricks:
            if pygame.Rect(self.ball.x, self.ball.y, self.ball.width, self.ball.height).colliderect(
                pygame.Rect(brick.x, brick.y, brick.width, brick.height)
            ):
                self.ball.bounce("y")
                self.bricks.remove(brick)
                self.score += brick.points
                break

        # Ball falls below screen
        if self.ball.y > SCREEN_HEIGHT:
            print("Game Over!")
            self.running = False

    def draw_objects(self):
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)

# Main
if __name__ == "__main__":
    player_name = input("Enter your player name: ")
    if not player_name.strip():
        print("Player name cannot be empty!")
    else:
        game = BreakoutGame()
        try:
            game.play()
        finally:
            game.save_score(player_name)
        pygame.quit()
