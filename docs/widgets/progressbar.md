# Progress Bar

Displays a continuously changing percentage

## Example Usage

```Python
import pygame_widgets
import pygame
import time
from pygame_widgets.progressbar import ProgressBar

startTime = time.time()

pygame.init()
win = pygame.display.set_mode((1000, 600))

progressBar = ProgressBar(win, 100, 100, 500, 40, lambda: 1 - (time.time() - startTime) / 10, curved=True)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((255, 255, 255))

    pygame_widgets.update(events)
    pygame.display.update()
```

This progress bar uses time to fill up, however, the progress function can be replaced by
any other function call that provides a percentage.


## Mandatory Parameters

| Parameter | Description | Type |
| :---: | --- | :---: |
| progress | Function that defines the percentage of the bar filled. | function -> float |

## Optional Parameters

| Parameter | Description | Type | Default |
| :---: | --- | :---: | :---: |
| curved | Adds curved ends to the progress bar. | bool | False |
| completedColour | Colour of completed section of progress bar. | (int, int, int) | (0, 200, 0) |
| incompletedColour | Colour of incompleted section of progress bar. | (int, int, int) | (100, 100, 100) |
