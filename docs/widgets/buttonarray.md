# ButtonArray

A collection of buttons with similar properties.

## Example Usage

<i>Note: See <a href="https://github.com/AustL/PygameWidgets/blob/master/examples/button_array_example.py" target="_blank">example</a></i>

```Python
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
```

## Mandatory Parameters

_Note: Mandatory parameters must be supplied in order._

| Parameter | Description | Type |
| :---: | --- | :---: |
| shape | Number of columns and rows of buttons (columns, rows). | (int, int) |

## Optional Parameters

_Note: Optional parameters of ButtonArray are similar to those of Button._

| Parameter | Description | Type | Default |
| :---: | --- | :---: | :---: |
| colour | Background colour of array. | (int, int, int) | (210, 210, 180) |
| border | Thickness between buttons and between the edges of array and buttons. | int | 10 |
| topBorder | Thickness between top of array and top of button. Overrides border. | int | border |
| bottomBorder | Thickness between bottom of array and bottom of button. Overrides border. | int | border |
| leftBorder | Thickness between left of array and left of button. Overrides border. | int | border |
| rightBorder | Thickness between right of array and right of button. Overrides border. | int | border |
| separationThickness | Thickness between buttons. Overrides border. | int | border |
