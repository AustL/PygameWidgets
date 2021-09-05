import pygame

import pygame_widgets
from pygame_widgets.button import ButtonArray

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
    texts=('1', '2', '3', '4'),  # Sets the texts of each button (counts left to right then top to bottom)
    # When clicked, print number
    onClicks=(lambda: print('1'), lambda: print('2'), lambda: print('3'), lambda: print('4'))
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

    pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
    pygame.display.update()
