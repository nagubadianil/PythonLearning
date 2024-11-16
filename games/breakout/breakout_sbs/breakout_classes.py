import pygame
import random

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)


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



class BreakoutGame:
    def __init__(self, game_name):
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption(game_name)
        self.screen =  pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
        self.clock = pygame.time.Clock()
        
    def populate_objects(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = [Brick(col * 80 + 10, row * 40 + 10) for row in range(5) for col in range(10)]
        self.game_score = {"name":"unknown", "score": 0 }     

    def draw_screen(self):
         self.screen.fill(WHITE)  # Set background color

    def run_game(self):    
        # Main loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move("left")
            if keys[pygame.K_RIGHT]:
                self.paddle.move("right")

            self.ball.move()

            self.ball.bounce_on_collision(self.paddle)
            self.ball.break_bricks(self.bricks, self.game_score)
            
            # Ball falls below paddle
            if self.ball.y > SCREEN_HEIGHT:
                print("Game Over!")
                running = False

            if not self.bricks:
                print("You Win!")
                running = False

            self.draw_screen()
           
            self.paddle.draw(self.screen)  # Draw paddle
           
            self.ball.draw(self.screen)  # Draw ball
            
            for brick in self.bricks:
                brick.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(60)

        print(f"Final Score: {self.game_score["score"]}")
        
        

if __name__ == "__main__":
    game = BreakoutGame("Simple Game")
    game.populate_objects()
    game.run_game()
    pygame.quit()