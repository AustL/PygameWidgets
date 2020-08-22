import pygame
from pygame import gfxdraw
import math

from pygame_widgets.widget import WidgetBase
from pygame_widgets import TextBox


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
                self.radius = self.width // 2
            else:
                self.radius = self.height // 2

        if self.vertical:
            self.handleRadius = kwargs.get('handleRadius', int(self.width / 1.3))
        else:
            self.handleRadius = kwargs.get('handleRadius', int(self.height / 1.3))

    def listen(self, events):
        pressed = pygame.mouse.get_pressed()[0]
        x, y = pygame.mouse.get_pos()

        if pressed:
            if self.contains(x, y):
                self.selected = True

            if self.selected:
                if self.vertical:
                    self.value = self.max - self.round((y - self.y) / self.height * self.max)
                    self.value = max(min(self.value, self.max), self.min)
                else:
                    self.value = self.round((x - self.x) / self.width * self.max + self.min)
                    self.value = max(min(self.value, self.max), self.min)

        else:
            self.selected = False

    def draw(self):
        pygame.draw.rect(self.win, self.colour, (self.x, self.y, self.width, self.height))

        if self.vertical:
            if self.curved:
                pygame.draw.circle(self.win, self.colour, (self.x + self.width // 2, self.y), self.radius)
                pygame.draw.circle(self.win, self.colour, (self.x + self.width // 2, self.y + self.height), self.radius)
            circle = (self.x + self.width // 2,
                      int(self.y + (self.max - self.value) / (self.max - self.min) * self.height))
        else:
            if self.curved:
                pygame.draw.circle(self.win, self.colour, (self.x, self.y + self.height // 2), self.radius)
                pygame.draw.circle(self.win, self.colour, (self.x + self.width, self.y + self.height // 2), self.radius)
            circle = (int(self.x + (self.value - self.min) / (self.max - self.min) * self.width),
                      self.y + self.height // 2)

        gfxdraw.filled_circle(self.win, *circle, self.handleRadius, self.handleColour)
        gfxdraw.aacircle(self.win, *circle, self.handleRadius, self.handleColour)

    def contains(self, x, y):
        if self.vertical:
            handleX = self.x + self.width // 2
            handleY = int(self.y + (self.max - self.value) / (self.max - self.min) * self.height)
        else:
            handleX = int(self.x + (self.value - self.min) / (self.max - self.min) * self.width)
            handleY = self.y + self.height // 2

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
    pygame.init()
    win = pygame.display.set_mode((1000, 600))

    slider = Slider(win, 100, 100, 800, 40, min=0, max=99, step=1)
    output = TextBox(win, 475, 200, 50, 50, fontSize=30)

    v_slider = Slider(win, 900, 200, 40, 300, min=0, max=99, step=1, vertical=True)
    v_output = TextBox(win, 800, 320, 50, 50, fontSize=30)

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill((255, 255, 255))

        slider.listen(events)
        v_slider.listen(events)

        slider.draw()
        v_slider.draw()

        output.setText(slider.getValue())
        v_output.setText(v_slider.getValue())

        output.draw()
        v_output.draw()

        pygame.display.update()
