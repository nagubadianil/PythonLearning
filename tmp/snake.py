import pygame
import time
import random

# Initialize pygame
pygame.init()

# Define the colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Set the display dimensions
dis_width = 600
dis_height = 400

# Define the snake block size
block_size = 10
snake_speed = 15

# Set up the display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Define the clock
clock = pygame.time.Clock()

# Define the font for messages
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Function to display the score
def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, black)
    dis.blit(value, [0, 0])

# Function to display messages
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

# Function to draw the snake
def draw_snake(block_size, snake_body):
    for x in snake_body:
        pygame.draw.rect(dis, green, [x[0], x[1], block_size, block_size])

# Game loop
def gameLoop():
    game_over = False
    game_close = False

    # Initialize the snake
    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_body = []
    length_of_snake = 1

    # Randomly generate food
    foodx = round(random.randrange(0, dis_width - block_size) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - block_size) / 10.0) * 10.0

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            your_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = block_size
                    x1_change = 0

        # Check for boundary collisions
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        # Update the position of the snake
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, yellow, [foodx, foody, block_size, block_size])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_body.append(snake_head)

        if len(snake_body) > length_of_snake:
            del snake_body[0]

        # Check for snake collision with itself
        for x in snake_body[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(block_size, snake_body)
        your_score(length_of_snake - 1)

        pygame.display.update()

        # Check for food collision
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - block_size) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - block_size) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Start the game
gameLoop()