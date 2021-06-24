# Button

A button that allows fully customisable text, images, colours and functions.

## Example Usage

```Python
import pygame
from pygame_widgets import Button

pygame.init()
win = pygame.display.set_mode((600, 600))

button = Button(
    win, 100, 100, 300, 150, text='Hello',
    fontSize=50, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=lambda: print('Click')
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

    button.listen(events)
    button.draw()

    pygame.display.update()
```

This button will be placed at (100, 100) with a width of 300 and a height of 150, display the text 'Hello' with font
size 50, leaving a margin of 20 and a radius of 20. When clicked, the button will change colour from red to green and '
Click' will be printed to the console.

## Optional Parameters

| Parameter | Description | Type | Default |
| :---: | --- | :---: | :---: |
| inactiveColour | Default colour when not pressed or hovered over. | (int, int, int) | (150, 150, 150) |
| pressedColour | Colour when pressed. | (int, int, int) | (100, 100, 100) |
| hoverColour | Colour when hovered over. | (int, int, int) | (125, 125, 125) |
| shadowDistance | Distance to projected shadow. Set to 0 if no shadow desired. | int | 0 |
| shadowColour | Colour of shadow | (int, int, int) | (210, 210, 180) |
| onClick | Function to be called when clicked. | function | None |
| onClickParams | Parameters to be fed into onClick function. | (*any) | () |
| onRelease | Function to be called when released. | function | None |
| onReleaseParams | Parameters to be fed into onRelease function. | (*any) | () |
| textColour | Colour of text. | (int, int, int) | (0, 0, 0) |
| fontSize | Size of text. | int | 20 |
| text | String to be displayed. | str | '' |
| font | Font of text. | pygame.font.Font | Calibri |
| textHAlign | Horizontal alignment of text. Can be 'centre', 'left' or 'right'. | str | 'centre' |
| textVAlign | Vertical alignment of text. Can be 'centre', 'top' or 'bottom'. | str | 'centre' |
| margin | Minimum distance between text / image and edge. | int | 20 |
| image | Image to be displayed. | pygame.Surface | None |
| imageHAlign | Horizontal alignment of image. Can be 'centre', 'left' or 'right'. | str | 'centre' |
| imageVAlign | Vertical alignment of image. Can be 'centre', 'top' or 'bottom'. | str | 'centre' |
| radius | Border radius. Set to half of width for circular button. Set to 0 for no radius. | int | 0 |
