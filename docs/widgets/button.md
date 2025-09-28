# Button

A button that allows fully customisable text, images, colours and functions.

## Example Usage

<i>Note: See <a href="https://github.com/AustL/PygameWidgets/blob/master/examples/button_example.py" target="_blank">example</a></i>

```Python
import pygame

import pygame_widgets
from pygame_widgets.button import Button

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
    inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
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

    pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
    pygame.display.update()
```

This button will be placed at (100, 100) with a width of 300 and a height of 150, display the text 'Hello' with font
size 50, leaving a margin of 20 and a radius of 20. When hovered over, the button changes to a darker red.
When clicked, the button will change colour from red to green and 'Click' will be printed to the console.

## Optional Parameters

|      Parameter       | Description                                                                      |       Type       |     Default     |
|:--------------------:|----------------------------------------------------------------------------------|:----------------:|:---------------:|
|    inactiveColour    | Default colour when not pressed or hovered over.                                 | (int, int, int)  | (150, 150, 150) |
|    pressedColour     | Colour when pressed.                                                             | (int, int, int)  | (100, 100, 100) |
|     hoverColour      | Colour when hovered over.                                                        | (int, int, int)  | (125, 125, 125) |
|    shadowDistance    | Distance to projected shadow. Set to 0 if no shadow desired.                     |       int        |        0        |
|     shadowColour     | Colour of shadow                                                                 | (int, int, int)  | (210, 210, 180) |
|       onClick        | Function to be called when clicked.                                              |     function     |      None       |
|    onClickParams     | Parameters to be fed into onClick function.                                      |      (*any)      |       ()        |
|      onRelease       | Function to be called when released.                                             |     function     |      None       |
|   onReleaseParams    | Parameters to be fed into onRelease function.                                    |      (*any)      |       ()        |
|    onHoverRelease    | Function to be continuously called when the mouse hovers over the button.        |     function     |      None       |
| onHoverReleaseParams | Parameters to be fed into onHover function.                                      | (*any) | () |
|       onHover        | Function to be called once when the mouse stops hovering over the button.        |     function     |      None       |
|    onHoverParams     | Parameters to be fed into onHoverRelease function.                               | (*any) | () |
|      textColour      | Colour of text.                                                                  | (int, int, int)  |    (0, 0, 0)    |
|       fontSize       | Size of text.                                                                    |       int        |       20        |
|         text         | String to be displayed.                                                          |       str        |       ''        |
|         font         | Font of text.                                                                    | pygame.font.Font |     Calibri     |
|      textHAlign      | Horizontal alignment of text. Can be 'centre', 'left' or 'right'.                |       str        |    'centre'     |
|      textVAlign      | Vertical alignment of text. Can be 'centre', 'top' or 'bottom'.                  |       str        |    'centre'     |
|        margin        | Minimum distance between text / image and edge.                                  |       int        |       20        |
|        image         | Image to be displayed.                                                           |  pygame.Surface  |      None       |
|     imageHAlign      | Horizontal alignment of image. Can be 'centre', 'left' or 'right'.               |       str        |    'centre'     |
|     imageVAlign      | Vertical alignment of image. Can be 'centre', 'top' or 'bottom'.                 |       str        |    'centre'     |
|        radius        | Border radius. Set to half of width for circular button. Set to 0 for no radius. |       int        |        0        |
