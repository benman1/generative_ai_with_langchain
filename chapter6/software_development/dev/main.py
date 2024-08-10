# This code is written in PEP8 syntax and includes comments to explain the code

# Import the necessary modules
import pygame
import sys

# Initialize pygame
pygame.init()

# Set the window size
window_width = 800
window_height = 600

# Create the window
window = pygame.display.set_mode((window_width, window_height))

# Set the window title
pygame.display.set_caption('My Game')

# Set the background color
background_color = (255, 255, 255)

# Main game loop
while True:
    # Check for events
    for event in pygame.event.get():
        # Quit if the user closes the window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill the background with the background color
    window.fill(background_color)

    # Update the display
    pygame.display.update()