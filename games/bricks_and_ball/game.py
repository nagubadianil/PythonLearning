import bricks_and_ball_basic
import bricks_and_ball_scenic
import bricks_and_ball_music
import bricks_and_ball_animation
import sys

if __name__=="__main__":
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == "basic":
                bricks_and_ball_basic.run_main_loop()
            elif sys.argv[1] == "scenic":
                bricks_and_ball_scenic.run_main_loop()
            elif sys.argv[1] == "music":
                bricks_and_ball_music.run_main_loop()
            elif sys.argv[1] == "animation":
                bricks_and_ball_animation.run_main_loop()
        else: 
            bricks_and_ball_animation.run_main_loop() 
    except:
        pass
