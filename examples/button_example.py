import pygame
from pygame_widgets import Button

# Set up Pygame
pygame.init()
win = pygame.display.set_mode((600, 600))

# Creates the button with optional parameters
button = Button(
    # Mandatory Parameters
    win,  # Surface to place button on
    100,  # X-coordinate of top left corner
    100,  # Y-coordinate of top left corner
    300,  # Width
    150,  # Height

    # Optional Parameters
    text='Hello',  # Text to display
    fontSize=50,  # Size of font
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=(255, 0, 0),  # Colour of button when not being interacted with
    hoverColour=(200, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 255, 0),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=lambda: print('Click')  # Function to call when clicked on
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

    # Allows button to check for clicks/events
    button.listen(events)

    # Renders button to screen
    button.draw()

    pygame.display.update()
