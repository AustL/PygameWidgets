# SearchBar

A dropdown menu allowing the selection of various elements using a search bar.

It is similar to `DropDown` but the main element is a `TextBox` that allows
to write selected search text.

The parameters of the `TextBox` can be made different
from the ones of the dropdown if they are specified in
the `textbox_kwargs` parameter.

![searchbar.gif](images/searchbox.gif)

```Python
import pygame
from pygame_widgets import SearchBar, Button

pygame.init()
win = pygame.display.set_mode((400, 280))

searchbar = SearchBar(
    win, 120, 10, 100, 50, name='Select Color',
    choices=pygame.colordict.THECOLORS.keys(),
    max_results=4,
    borderRadius=3, colour=pygame.Color('green'), direction='down', textHAlign='left',

)


def print_value():
    searchbar.text_bar.colour = searchbar.getText()


button = Button(
    win, 10, 10, 100, 50, text='Set Color', fontSize=30,
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

    searchbar.listen(events)
    searchbar.draw()
    button.listen(events)
    button.draw()

    pygame.display.update()
```

This is a classic searchbar. To get the current selected text
is accessed through the `getText()` methods.

It returns the current text in the search bar.


## Mandatory Parameters

_Note: Mandatory parameters must be supplied in order._

| Parameter | Description | Type |
| :---: | --- | :---: |
| choices | Choices possibility of the search | list of str |

## Optional Parameters

| Parameter | Description | Type | Default |
| :---: | --- | :---: | :---: |
| direction | Expansion direction. Can be 'down', 'up', 'left' or 'right'. | str | down |
| textbox_kwargs | Optional different parameters only for the `TextBox`. | dict | {} |
| inactiveColour | Default colour when not pressed or hovered over. | (int, int, int) | (150, 150, 150) |
| pressedColour | Colour when pressed. | (int, int, int) | (100, 100, 100) |
| hoverColour | Colour when hovered over. | (int, int, int) | (125, 125, 125) |
| onSelected | Function to be called when a search choice is selected. | function | None |
| onSelectedParams | Parameters to be fed into onSelected function. | (*any) | () |
| onStartSearch | Function to be called when a search is started by user (clicking on the search box). | function | None |
| onStartSearchParams | Parameters to be fed into onStartSearch function. | (*any) | () |
| onStopSearch | Function to be called when a search is stopped (clicking outside the search dropdown, or selecting a choice). | function | None |
| onStopSearchParams | Parameters to be fed into onStopSearch function. | (*any) | () |
| textColour | Colour of text. | (int, int, int) | (0, 0, 0) |
| fontSize | Size of text. | int | 20 |
| font | Font of text. | pygame.font.Font | sans-serif |
| textHAlign | Horizontal alignment of text. Can be 'centre', 'left' or 'right'. | str | 'centre' |
| borderColour | Colour of border. | (int, int, int) | (0, 0, 0) |
| borderThickness | Thickness of border. | int | 3 |
| borderRadius | Border radius. Set to 0 for no radius. | int | 0 |
