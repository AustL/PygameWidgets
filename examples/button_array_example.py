import pygame
from pygame_widgets import ButtonArray

# Set up Pygame
pygame.init()
win = pygame.display.set_mode((600, 600))

# Creates an array of buttons
buttonArray = ButtonArray(
    # Mandatory Parameters
    win,  # Surface to place button array on
    50,  # X-coordinate
    50,  # Y-coordinate
    500,  # Width
    500,  # Height
    (2, 2),  # Shape: 2 buttons wide, 2 buttons tall
    border=100,  # Distance between buttons and edge of array
    texts=('1', '2', '3', '4')  # Sets the texts of each button (counts left to right then top to bottom)
)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((255, 255, 255))

    # Allows button array to check for clicks/events
    buttonArray.listen(events)

    # Renders button array to screen
    buttonArray.draw()

    pygame.display.update()
