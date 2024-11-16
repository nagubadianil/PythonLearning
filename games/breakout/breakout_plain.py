import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Paddle dimensions
PADDLE_WIDTH = 150  # Increased from 100 to 150
PADDLE_HEIGHT = 20

# Ball dimensions
BALL_SIZE = 15

# Brick dimensions
BRICK_WIDTH = 75
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = 10

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game")

# Clock to control game speed
clock = pygame.time.Clock()

# Paddle class
class Paddle:
    def __init__(self):
        self.x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        self.y = SCREEN_HEIGHT - 50
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.color = GREEN
        self.speed = 20  # Rushi : Left and right arrow speed

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Ball class
class Ball:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.size = BALL_SIZE
        self.color = BLUE
        self.dx = random.choice([-5, 5])
        self.dy = -5

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def bounce(self, axis):
        if axis == "x":
            self.dx = -self.dx
        if axis == "y":
            self.dy = -self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

# Brick class
class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = RED

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Generate bricks
def create_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = col * (BRICK_WIDTH + 5) + 10
            y = row * (BRICK_HEIGHT + 5) + 10
            bricks.append(Brick(x, y))
    return bricks

# Main game function
def main():
    running = True
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()
    score = 0

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move("left")
        if keys[pygame.K_RIGHT]:
            paddle.move("right")

        # Ball movement
        ball.move()

        # Ball collision with walls
        if ball.x <= 0 or ball.x >= SCREEN_WIDTH - ball.size:
            ball.bounce("x")
        if ball.y <= 0:
            ball.bounce("y")

        # Ball collision with paddle
        if (
            paddle.x < ball.x < paddle.x + paddle.width
            and paddle.y < ball.y + ball.size < paddle.y + paddle.height
        ):
            ball.bounce("y")

        # Ball collision with bricks
        for brick in bricks[:]:
            if (
                brick.x < ball.x < brick.x + brick.width
                and brick.y < ball.y < brick.y + brick.height
            ):
                bricks.remove(brick)
                ball.bounce("y")
                score += 10

        # Ball falls below paddle
        if ball.y > SCREEN_HEIGHT:
            print("Game Over!")
            running = False

        # Draw everything
        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)

        # Update display
        pygame.display.flip()
        clock.tick(60)

    print(f"Final Score: {score}")
    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
