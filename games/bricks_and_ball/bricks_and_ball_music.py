from bricks_and_ball_scenic import ScenicBreakoutGame, ScenicBall, resource_path
import pygame
import sys


class MusicBall(ScenicBall):
    def __init__(self,
                 break_bricks_sound="break_bricks_sound.mp3",
                 collision_sound="collision_sound.mp3",
                 bounce_x_sound="bounce_x_sound.mp3",
                 bounce_y_sound=""):
        super().__init__()
        self.break_bricks_music = pygame.mixer.Sound(resource_path(break_bricks_sound)) 
        self.collision_music = pygame.mixer.Sound(resource_path(collision_sound)) 
        self.bounce_x_music = pygame.mixer.Sound(resource_path(bounce_x_sound)) 
        
    def handle_break_bricks(self, bricks, brick, score_card):
        self.break_bricks_music.play() 
        super().handle_break_bricks( bricks, brick, score_card)
         
    def handle_collision(self):
        self.collision_music.play()
        super().handle_collision() 
    
    def handle_bounce_x(self):
        self.bounce_x_music.play()
        super().handle_bounce_x() 
    
    def handle_bounce_y(self):
        super().handle_bounce_y

class MusicBreakoutGame(ScenicBreakoutGame):
    def __init__(self, game_name,bg_music="background_music.mp3"):
        super().__init__(game_name)
        pygame.mixer.init()
        pygame.mixer.music.load(resource_path('background_music.mp3'))
        pygame.mixer.music.set_volume(0.5) 
        
    def run_game(self):
        pygame.mixer.music.play(loops=-1, start=0.0)
        super().run_game()
        
    def populate_objects(self, paddle=None, ball=None, bricks=None, game_score=None):
        
        if paddle is not None:
            self.paddle = paddle
        else:
            self.paddle = None
        
        if ball is not None:
            self.ball = ball
        else: 
            self.ball = MusicBall()
        
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

def run_main_loop():        
    game = MusicBreakoutGame("Bhavesh, Game with Music")
    game.populate_objects()
    game.run_game()
    
    pygame.mixer.music.stop()
    
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