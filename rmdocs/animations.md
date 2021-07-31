# Animations

Create an animation by using the default Translate or Resize, inheriting from AnimationBase, or using AnimationBase
directly.

## Example Usage

```Python
import pygame
from pygame_widgets import Button, Resize

pygame.init()
win = pygame.display.set_mode((600, 600))

button = Button(win, 100, 100, 300, 150)

animation = Resize(button, 3, 200, 200)
animation.start()

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

Over 3 seconds, the width of the button was changed from 300 to 200 and its height from 150 to 200. Since it is
performed on a separate thread, the button is still able to function during the animation.
