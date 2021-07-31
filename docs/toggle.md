# Toggle

Allows switching between true and false options

## Example Usage

```Python
import pygame
from pygame_widgets import Toggle

pygame.init()
win = pygame.display.set_mode((1000, 600))

toggle = Toggle(win, 100, 100, 100, 40)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((255, 255, 255))

    toggle.listen(events)
    toggle.draw()

    pygame.display.update()
```

## Optional Parameters

| Parameter | Description | Type | Default |
| :---: | --- | :---: | :---: |
| startOn | Default value. | bool | False |
| onColour | Colour of toggle when on. | (int, int, int) | (141, 185, 244) |
| offColour | Colour of toggle when off. | (int, int, int) | (150, 150, 150) |
| handleOnColour | Thickness of toggle handle when on. | (int, int, int) | (26, 115, 232) |
| handleOffColour | Thickness of toggle handle when off. | (int, int, int) | (200, 200, 200) |
| handleRadius | Radius of handle. | int | height / 1.3 |