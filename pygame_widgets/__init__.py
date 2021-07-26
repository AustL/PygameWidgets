from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button, ButtonArray
from pygame_widgets.slider import Slider
from pygame_widgets.animations.animation import AnimationBase, Translate, Resize
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.toggle import Toggle
from pygame_widgets.progressbar import ProgressBar
from pygame_widgets.combobox import ComboBox
from pygame_widgets.mouse import Mouse, MouseState
from pygame_widgets.widget import WidgetBase, WidgetHandler

from pygame.event import Event


def update(events: [Event]):
    Mouse.updateMouseState()
    for widget in WidgetHandler.getActiveWidgets():
        widget.listen(events)
        widget.draw()
