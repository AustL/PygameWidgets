import pygame
from pygame import gfxdraw

import pygame_widgets
from pygame_widgets.widget import WidgetBase
from pygame_widgets.mouse import Mouse, MouseState


class Toggle(WidgetBase):
    def __init__(self, win, x, y, width, height, **kwargs):
        super().__init__(win, x, y, width, height)

        self.value = kwargs.get('startOn', False)
        self.onColour = kwargs.get('onColour', (141, 185, 244))
        self.offColour = kwargs.get('offColour', (150, 150, 150))
        self.handleOnColour = kwargs.get('handleOnColour', (26, 115, 232))
        self.handleOffColour = kwargs.get('handleOffColour', (200, 200, 200))

        self.handleRadius = kwargs.get('handleRadius', int(self._height / 1.3))
        self.radius = self._height // 2

        self.colour = self.onColour if self.value else self.offColour
        self.handleColour = self.handleOnColour if self.value else self.handleOffColour

    def toggle(self):
        self.value = not self.value
        self.colour = self.onColour if self.value else self.offColour
        self.handleColour = self.handleOnColour if self.value else self.handleOffColour

    def listen(self, events):
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                if mouseState == MouseState.CLICK:
                    self.toggle()

    def draw(self):
        pygame.draw.rect(self.win, self.colour, (self._x, self._y, self._width, self._height))

        pygame.draw.circle(self.win, self.colour, (self._x, self._y + self._height // 2), self.radius)
        pygame.draw.circle(self.win, self.colour, (self._x + self._width, self._y + self._height // 2), self.radius)

        circle = (
            self._x + (
                self._width - self.handleRadius + self.radius if self.value else self.handleRadius - self.radius
            ),
            self._y + self._height // 2
        )

        gfxdraw.filled_circle(self.win, *circle, self.handleRadius, self.handleColour)
        gfxdraw.aacircle(self.win, *circle, self.handleRadius, self.handleColour)

    def getValue(self):
        return self.value


if __name__ == '__main__':
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

        pygame_widgets.update(events)
        pygame.display.update()
