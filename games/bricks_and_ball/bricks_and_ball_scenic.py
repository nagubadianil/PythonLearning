from bricks_and_ball_basic import BreakoutGame, Paddle, Ball, Brick, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
import pygame
import sys
import os

BLACK = (0, 0, 0)

def resource_path(relative_path):
    """Get the absolute path to a resource, works for both dev and PyInstaller."""
    try:
        # For PyInstaller, the resource is extracted to sys._MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # For normal development, use the current directory
        base_path = os.path.abspath("./assets")
    return os.path.join(base_path, relative_path)

class ScenicPaddle(Paddle):
    def __init__(self, img="stick.png"):
        super().__init__()
        self.stick_image = pygame.image.load(resource_path(img))
        self.stick_image = pygame.transform.scale(self.stick_image, (self.width, self.height))
        self.height = 20
    def draw(self,screen):
        screen.blit(self.stick_image, (self.x, self.y))   

class ScenicBall(Ball):
    def __init__(self, img="ball.png"):
        super().__init__()
        self.size = 20
        self.ball_image = pygame.image.load(resource_path(img))
        self.ball_image = pygame.transform.scale(self.ball_image, (self.size, self.size))

    def draw(self,screen):
        screen.blit(self.ball_image, (self.x, self.y))   

class ScenicBrick(Brick):
    def __init__(self, x, y, img="brick.png"):
        super().__init__(x, y)
        self.brick_image = pygame.image.load(resource_path(img))
        self.brick_image = pygame.transform.scale(self.brick_image, (self.width, self.height))

    def draw(self,screen):
        screen.blit(self.brick_image, (self.x, self.y))   

    
class ScenicBreakoutGame(BreakoutGame):  
    def __init__(self, game_name, bg_img="nature_bg.png"):
        super().__init__(game_name)
        self.background_image = pygame.image.load(resource_path(bg_img))
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale image to fit screen

    def populate_objects(self, paddle=None, ball=None, bricks=None, game_score=None):
       
        if paddle is not None:
            self.paddle = paddle
        else:
            self.paddle = ScenicPaddle()
        
        if ball is not None:
           self.ball = ball
        else: 
            self.ball = ScenicBall()
        
        if bricks is not None:
            self.bricks = bricks
        else:
            self.bricks = [ScenicBrick(col * 80 + 10, row * 40 + 10) for row in range(5) for col in range(10)]
        
        if game_score is not None:
           self.game_score = game_score
        else: 
            self.game_score = None
        
        super().populate_objects(paddle=self.paddle,
                                 ball=self.ball, 
                                 bricks=self.bricks,
                                 game_score=self.game_score)
             
    def draw_screen(self):
         self.screen.blit(self.background_image, (0, 0))
         
    def show_end_dialog(self, message):
        # Clear the screen
        self.screen.fill(WHITE)
        
        font = pygame.font.Font(None, 36)
        
        # Render the message
        text = font.render(message, True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)
        # Render instructions to restart or quit
        restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)
        restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_text_rect)
        pygame.display.flip()     

 
def run_main_loop():        
    game = ScenicBreakoutGame("Bhavesh, yet to build GAME")
    game.populate_objects()
    game.run_game()
    if not game.bricks:
        game.show_end_dialog(f"YOU WON! Score: {game.game_score["score"]}")
    else:
        game.show_end_dialog(f"Your Score is {game.game_score["score"]}")
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                     run_main_loop()
                if event.key == pygame.K_q:  # Quit
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":    
    try:               
        run_main_loop()
    except:
        pass