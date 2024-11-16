import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game with Background Image")

# Load background image
background_image = pygame.image.load("nature_bg.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale image to fit screen

# Main game loop
def game_loop():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw background image
        screen.blit(background_image, (0, 0))

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

# Run the game
game_loop()