from bricks_and_ball_music import MusicBreakoutGame, MusicBall, resource_path

import pygame
import sys
import threading
import random


# Ripple class
class Ripple:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 0
        self.alpha = 255  # Opacity (0 = fully transparent, 255 = fully opaque)

    def update(self):
        self.radius += 2  # Increase the radius
        self.alpha -= 3  # Decrease the opacity
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, surface):
        if surface and self.alpha > 0:
            # Create a transparent surface
            ripple_surface = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
            pygame.draw.circle(ripple_surface, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), self.alpha), (self.x, self.y), self.radius)
            surface.blit(ripple_surface, (0, 0))

class AnimationBall(MusicBall): #["ball.png", "bal_90c.png","bal_180c.png", "bal_270c.png"]
    def __init__(self, ball_image_files = ["ball.png", "bal_90.png","bal_180.png", "bal_270.png"]):
        
        super().__init__()
        self.ball_images = {}
        
        self.size = 25
        for index, ball_img in enumerate(ball_image_files):
            self.ball_images[index] = pygame.image.load(resource_path(ball_img))
            self.ball_images[index] = pygame.transform.scale(self.ball_images[index], (self.size, self.size))
        
        
        self.next_index = 0

        self.MY_TIMER_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MY_TIMER_EVENT, 50)
        thread = threading.Thread(target=self.timer_loop, args=(self,2))
        thread.start()
        
        self.screen = None
        self.ripples = []
        
        self.clock = pygame.time.Clock()
        
    def draw(self, screen):
       
        screen.blit(self.ball_images[self.next_index], (self.x, self.y))   
        self.screen = screen
        
    def set_next(self):          
       
        if  self.dx <0:
            if self.next_index == len(self.ball_images)-1:
                self.next_index = 0
            else:
                self.next_index+=1
        else:
            if self.next_index == 0:
                self.next_index = len(self.ball_images)-1
            else:
                self.next_index -=1
                
   
   
    @staticmethod
    def timer_loop(self, dummy):     
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == self.MY_TIMER_EVENT:
                    self.set_next()   
            
            try:
               # Update ripples
                for ripple in self.ripples:
                    ripple.update()
                    if ripple.alpha == 0:  # Remove the ripple if it's fully faded
                        self.ripples.remove(ripple)
            except Exception:
                pass
               
            try:
                for ripple in self.ripples:
                    ripple.draw(self.screen) 
            except Exception:
                pass 
            
            try:
              pass
              #  self.clock.tick(60)
            except Exception:
                pass 
        
    def bounce(self, axis):
        super().bounce(axis)
        self.set_next()
        self.ripples.append(Ripple(self.x, self.y))

        
class AnimationBreakoutGame(MusicBreakoutGame):
    def __init__(self, game_name):
        super().__init__(game_name)
        
    def populate_objects(self, paddle=None, ball=None, bricks=None, game_score=None):
        
        if paddle is not None:
            self.paddle = paddle
        else:
            self.paddle = None
        
        if ball is not None:
            self.ball = ball
        else: 
            self.ball = AnimationBall()
        
        if bricks is not None:
            self.bricks = bricks
        else:
            self.bricks = None
        
        if game_score is not None:
           self.game_score = game_score
        else: 
            self.game_score = None
        
        super().populate_objects(paddle=self.paddle,
                                 ball=self.ball, 
                                 bricks=self.bricks,
                                 game_score=self.game_score)
    
    def run_game(self):
        
        super().run_game()


def run_main_loop():        
    game = AnimationBreakoutGame("Bhavesh, Game with Animation")
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