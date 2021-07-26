from pygame_widgets.mouse import Mouse
from pygame_widgets.widget import WidgetHandler

from pygame.event import Event


def update(events: [Event]):
    Mouse.updateMouseState()
    for widget in WidgetHandler.getActiveWidgets():
        widget.listen(events)
        widget.draw()
