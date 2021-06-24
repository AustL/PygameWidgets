# Dropdown

A dropdown menu allowing the selection of various elements.

![dropdown.gif](images/dropdown.gif)

```Python
import pygame
from pygame_widgets import Button, Dropdown

pygame.init()
win = pygame.display.set_mode((400, 280))

dropdown = Dropdown(
    win, 120, 10, 100, 50, name='Select Color',
    choices=[
        'Red',
        'Blue',
        'Yellow',
    ],
    borderRadius=3, colour=pygame.Color('green'), values=[1, 2, 'true'], direction='down', textHAlign='left'
)


def print_value():
    print(dropdown.getSelected())


button = Button(
    win, 10, 10, 100, 50, text='Print Value', fontSize=30,
    margin=20, inactiveColour=(255, 0, 0), pressedColour=(0, 255, 0),
    radius=5, onClick=print_value, font=pygame.font.SysFont('calibri', 10),
    textVAlign='bottom'
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

    dropdown.listen(events)
    dropdown.draw()
    button.listen(events)
    button.draw()

    pygame.display.update()
```

This is a classic dropdown, but with a twist: if you right-click on the top, it reset itself. To get the current value
of the dropdown, we use the `getSelected()` methods.

It returns:

- `None` if nothing is selected
- A string with the choice you selected if the optional arg `value` is not set
- If the optional arg `value` is set, we return the value corresponding to the choice.

For the example above:

| Choice | Value |
| :---: | :---: |
| Red | 1 |
| Blue | 2 |
| Yellow | 3 |

## Mandatory Parameters

_Note: Mandatory parameters must be supplied in order._

| Parameter | Description | Type |
| :---: | --- | :---: |
| name | Main name of the dropdown | str | 
| choices | Choices to display | list of str | 

## Optional Parameters

| Parameter | Description | Type | Default |
| :---: | --- | :---: | :---: |
| direction | Expansion direction. Can be 'down', 'up', 'left' or 'right'. | str | down |
| values | optional return value corresponding to the choices. Must be the same length as `choices` |list|a copy of choices|
| inactiveColour | Default colour when not pressed or hovered over. | (int, int, int) | (150, 150, 150) |
| pressedColour | Colour when pressed. | (int, int, int) | (100, 100, 100) |
| hoverColour | Colour when hovered over. | (int, int, int) | (125, 125, 125) |
| onClick | Function to be called when clicked. | function | None |
| onClickParams | Parameters to be fed into onClick function. | (*any) | () |
| onRelease | Function to be called when released. | function | None |
| onReleaseParams | Parameters to be fed into onRelease function. | (*any) | () |
| textColour | Colour of text. | (int, int, int) | (0, 0, 0) |
| fontSize | Size of text. | int | 20 |
| font | Font of text. | pygame.font.Font | sans-serif |
| textHAlign | Horizontal alignment of text. Can be 'centre', 'left' or 'right'. | str | 'centre' |
| borderColour | Colour of border. | (int, int, int) | (0, 0, 0) |
| borderThickness | Thickness of border. | int | 3 |
| borderRadius | Border radius. Set to 0 for no radius. | int | 0 |
