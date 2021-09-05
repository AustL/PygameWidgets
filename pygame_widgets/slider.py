import pygame
from pygame import gfxdraw
import math

import pygame_widgets
from pygame_widgets.widget import WidgetBase
from pygame_widgets.mouse import Mouse, MouseState


class Slider(WidgetBase):
    def __init__(self, win, x, y, width, height, **kwargs):
        super().__init__(win, x, y, width, height)

        self.selected = False

        self.min = kwargs.get('min', 0)
        self.max = kwargs.get('max', 99)
        self.step = kwargs.get('step', 1)

        self.colour = kwargs.get('colour', (200, 200, 200))
        self.handleColour = kwargs.get('handleColour', (0, 0, 0))

        self.borderThickness = kwargs.get('borderThickness', 3)
        self.borderColour = kwargs.get('borderColour', (0, 0, 0))

        self.value = self.round(kwargs.get('initial', (self.max + self.min) / 2))
        self.value = max(min(self.value, self.max), self.min)

        self.curved = kwargs.get('curved', True)

        self.vertical = kwargs.get('vertical', False)

        if self.curved:
            if self.vertical:
                self.radius = self._width // 2
            else:
                self.radius = self._height // 2

        if self.vertical:
            self.handleRadius = kwargs.get('handleRadius', int(self._width / 1.3))
        else:
            self.handleRadius = kwargs.get('handleRadius', int(self._height / 1.3))

    def listen(self, events):
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                if mouseState == MouseState.CLICK:
                    self.selected = True

            if mouseState == MouseState.RELEASE:
                self.selected = False

            if self.selected:
                if self.vertical:
                    self.value = self.max - self.round((y - self._y) / self._height * self.max)
                    self.value = max(min(self.value, self.max), self.min)
                else:
                    self.value = self.round((x - self._x) / self._width * self.max + self.min)
                    self.value = max(min(self.value, self.max), self.min)

    def draw(self):
        if not self._hidden:
            pygame.draw.rect(self.win, self.colour, (self._x, self._y, self._width, self._height))

            if self.vertical:
                if self.curved:
                    pygame.draw.circle(self.win, self.colour, (self._x + self._width // 2, self._y), self.radius)
                    pygame.draw.circle(self.win, self.colour, (self._x + self._width // 2, self._y + self._height),
                                       self.radius)
                circle = (self._x + self._width // 2,
                          int(self._y + (self.max - self.value) / (self.max - self.min) * self._height))
            else:
                if self.curved:
                    pygame.draw.circle(self.win, self.colour, (self._x, self._y + self._height // 2), self.radius)
                    pygame.draw.circle(self.win, self.colour, (self._x + self._width, self._y + self._height // 2),
                                       self.radius)
                circle = (int(self._x + (self.value - self.min) / (self.max - self.min) * self._width),
                          self._y + self._height // 2)

            gfxdraw.filled_circle(self.win, *circle, self.handleRadius, self.handleColour)
            gfxdraw.aacircle(self.win, *circle, self.handleRadius, self.handleColour)

    def contains(self, x, y):
        if self.vertical:
            handleX = self._x + self._width // 2
            handleY = int(self._y + (self.max - self.value) / (self.max - self.min) * self._height)
        else:
            handleX = int(self._x + (self.value - self.min) / (self.max - self.min) * self._width)
            handleY = self._y + self._height // 2

        if math.sqrt((handleX - x) ** 2 + (handleY - y) ** 2) <= self.handleRadius:
            return True

        return False

    def round(self, value):
        return self.step * round(value / self.step)

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value


if __name__ == '__main__':
    from pygame_widgets.textbox import TextBox

    pygame.init()
    win = pygame.display.set_mode((1000, 600))

    slider = Slider(win, 100, 100, 800, 40, min=0, max=99, step=1)
    output = TextBox(win, 475, 200, 50, 50, fontSize=30)

    v_slider = Slider(win, 900, 200, 40, 300, min=0, max=99, step=1, vertical=True)
    v_output = TextBox(win, 800, 320, 50, 50, fontSize=30)

    output.disable()
    v_output.disable()

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill((255, 255, 255))

        output.setText(slider.getValue())
        v_output.setText(v_slider.getValue())

        pygame_widgets.update(events)
        pygame.display.update()
