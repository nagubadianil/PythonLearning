import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game")

clock = pygame.time.Clock()

class Paddle:
    def __init__(self):
        self.x = (SCREEN_WIDTH - 100) // 2
        self.y = SCREEN_HEIGHT - 50
        self.width = 200
        self.height = 10
        self.color = (0, 255, 0)
        self.speed = 20
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

class Ball:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.size = 10
        self.color = (0, 0, 255)
        self.dx = random.choice([-5, 5])
        self.dy = -5

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.size:
            self.bounce("x")
        if self.y <= 0:
            self.bounce("y")
        
    def bounce(self, axis):
        if axis == "x":
            self.dx = -self.dx
        if axis == "y":
            self.dy = -self.dy

    def bounce_on_collision(self, paddle):
        # Ball collision with paddle
        if (
            paddle.x < self.x < paddle.x + paddle.width
            and paddle.y < self.y + self.size < paddle.y + paddle.height
        ):
            self.bounce("y")
            
    def break_bricks(self, bricks, score_card):
        for brick in bricks[:]:
            if (brick.x < self.x < brick.x + brick.width) and (brick.y < self.y < brick.y + brick.height):
                bricks.remove(brick)
                self.bounce("y")
                score_card["score"] += 10

            
# Brick class
class Brick:
    def __init__(self, x, y):
        #print(f"Brick x, y: {x}, {y}")
        self.x = x
        self.y = y
        self.width = 75
        self.height = 30
        self.color = (255, 0, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


paddle = Paddle()
ball = Ball()
bricks = [Brick(col * 80 + 10, row * 40 + 10) for row in range(5) for col in range(10)]
game_score = {"name":"unknown", "score": 0 }

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move("left")
    if keys[pygame.K_RIGHT]:
        paddle.move("right")

    ball.move()

    ball.bounce_on_collision(paddle)
    ball.break_bricks(bricks, game_score)
    
    # Ball falls below paddle
    if ball.y > SCREEN_HEIGHT:
        print("Game Over!")
        running = False

    if not bricks:
        print("You Win!")
        running = False

    screen.fill(WHITE)  # Set background color
    paddle.draw(screen)  # Draw paddle
    ball.draw(screen)  # Draw ball
    
    for brick in bricks:
        brick.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

print(f"Final Score: {game_score["score"]}")
pygame.quit()