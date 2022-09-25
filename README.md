# Pygame Widgets

![](https://img.shields.io/pypi/dm/pygame-widgets)

A helper module for common widgets that may be required in developing applications with Pygame. It supports fully
customisable buttons, collections of buttons, textboxes, sliders and many more! If there are any widgets that you would like to see
added, please create an issue!

## Changes in Pygame Widgets v1.0.0
In v1.0.0, there are some minor changes to the use of the module, which may affect existing projects.
This outlines the changes that will affect current users in the new version.

* As more widgets are added, importing is now different
```Python
# Now
from pygame_widgets.button import Button

# Instead of
from pygame_widgets import Button  # Will not work
```
* All widgets are now updated (draw and listen) by the update method

```Python
import pygame
import pygame_widgets
from pygame_widgets.button import Button

pygame.init()
win = pygame.display.set_mode((600, 600))
button = Button(win, 100, 100, 300, 150)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
            
    win.fill((255, 255, 255))
    
    # Now
    pygame_widgets.update(events)
    
    # Instead of
    button.listen(events)
    button.draw()
    
    pygame.display.update()
```


## Prerequisites

* [Python 3](https://www.python.org/downloads) `>= 3.10`
* [Pygame](https://www.pygame.org/wiki/GettingStarted) `>= 2.0.0`

## Installation

Ensure that Python 3 and pip are installed and added to your environment PATH.

```python -m pip install pygame-widgets```

Open a Python console and run the following command.

```import pygame_widgets```

If you receive no errors, the installation was successful.

## Usage

For full documentation, see [pygamewidgets.readthedocs.io](https://pygamewidgets.readthedocs.io/en/latest/).

* [Common](docs/widgets/common.md)
* [Button](docs/widgets/button.md)
* [ButtonArray](docs/widgets/buttonarray.md)
* [TextBox](docs/widgets/textbox.md)
* [Slider](docs/widgets/slider.md)
* [Toggle](docs/widgets/toggle.md)
* [ProgressBar](docs/widgets/progressbar.md)
* [Dropdown](docs/widgets/dropdown.md)
* [ComboBox](docs/widgets/combobox.md)
* [Animations](docs/animations/animations.md)

## How to Contribute

Any contribution to this project would be greatly appreciated.
This can include:
* Finding errors or bugs and creating a new issue
* Addressing active issues
* Adding functionality
* Improving documentation

If applicable, you should make any changes in a forked repository and then create a pull
request once the changes are ***complete*** and preferably tested if possible.

_Note: If writing any code, please attempt to follow the [Code Style Guide](docs/CONTRIBUTING.md)_
