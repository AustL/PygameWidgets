import pygame
import math

import pygame_widgets
from pygame_widgets.widget import WidgetBase
from pygame_widgets.mouse import Mouse, MouseState


class Checkbox(WidgetBase):
    def __init__(self, win, x, y, width, height, items, **kwargs):
        """ A list of buttons that allows multiple selections

        :param win: Surface on which to draw
        :type win: pygame.Surface
        :param x: X-coordinate of top left
        :type x: int
        :param y: Y-coordinate of top left
        :type y: int
        :param width: Width of list
        :type width: int
        :param height: Height of list
        :type height: int
        :param items: Names of list items
        :type items: tuple of str
        :param kwargs: Optional parameters
        """
        super().__init__(win, x, y, width, height)

        self.items = items
        self.rows = len(items)
        self.rowHeight = self._height // self.rows
        self.selected = [False for _ in range(self.rows)]

        # Border
        self.borderThickness = kwargs.get('borderThickness', 3)
        self.borderColour = kwargs.get('borderColour', (0, 0, 0))
        self.radius = kwargs.get('radius', 0)

        # Checkbox
        self.boxSize = int(kwargs.get('boxSize', self._height / self.rows // 3))
        self.boxThickness = kwargs.get('boxThickness', 3)
        self.boxColour = kwargs.get('boxColour', (0, 0, 0))
        # TODO: selected image (tick) / colour

        # Colour
        self.colour = kwargs.get('colour', (255, 255, 255))

        # Alternating colours: overrides colour
        self.colour1 = kwargs.get('colour1', self.colour)
        self.colour2 = kwargs.get('colour2', self.colour)

        # Text
        self.textColour = kwargs.get('textColour', (0, 0, 0))
        self.fontSize = kwargs.get('fontSize', 20)
        self.font = kwargs.get('font', pygame.font.SysFont('sans-serif', self.fontSize))
        self.texts = [self.font.render(self.items[row], True, self.textColour) for row in range(self.rows)]
        self.textRects = self.createTextRects()

        self.clicked = False

        self.boxes = self.createBoxLocations()

    def createTextRects(self):
        textRects = []
        for row in range(self.rows):
            textRects.append(
                self.texts[row].get_rect(
                    center=(
                        self._x + self.boxSize * 2 + (self._width - self.boxSize * 2) // 2,
                        self._y + self.rowHeight * row + self.rowHeight // 2
                    )
                )
            )

        return textRects

    def createBoxLocations(self):
        boxes = []
        for row in range(self.rows):
            boxes.append(pygame.Rect(
                self._x + self.boxSize,
                self._y + self.rowHeight * row + self.boxSize,
                self.boxSize, self.boxSize
            ))
        return boxes

    def listen(self, events):
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                if mouseState == MouseState.CLICK:
                    for row in range(self.rows):
                        if self.boxes[row].collidepoint(x, y):
                            self.selected[row] = not self.selected[row]

    def draw(self):
        """ Display to surface """
        if not self._hidden:
            for row in range(self.rows):
                colour = self.colour1 if not row % 2 else self.colour2
                if pygame.version.vernum[0] < 2:
                    pygame.draw.rect(
                        self.win, colour, (self._x, self._y + self.rowHeight * row, self._width, self.rowHeight)
                    )
                else:
                    if row == 0:
                        pygame.draw.rect(
                            self.win, colour, (self._x, self._y + self.rowHeight * row, self._width, self.rowHeight),
                            border_top_left_radius=self.radius, border_top_right_radius=self.radius
                        )

                    elif row == self.rows - 1:
                        pygame.draw.rect(
                            self.win, colour, (self._x, self._y + self.rowHeight * row, self._width, self.rowHeight),
                            border_bottom_left_radius=self.radius, border_bottom_right_radius=self.radius
                        )

                    else:
                        pygame.draw.rect(
                            self.win, colour, (self._x, self._y + self.rowHeight * row, self._width, self.rowHeight)
                        )

                width = 0 if self.selected[row] else self.boxThickness
                pygame.draw.rect(
                    self.win, self.boxColour,
                    self.boxes[row],
                    width
                )

                self.win.blit(self.texts[row], self.textRects[row])

    def getSelected(self):
        return [self.items[row] for row in range(self.rows) if self.selected[row]]


class Radio(WidgetBase):
    def __init__(self, win, x, y, width, height, items, **kwargs):
        """ A list of buttons that allows a single selections

        :param win: Surface on which to draw
        :type win: pygame.Surface
        :param x: X-coordinate of top left
        :type x: int
        :param y: Y-coordinate of top left
        :type y: int
        :param width: Width of list
        :type width: int
        :param height: Height of list
        :type height: int
        :param items: Names of list items
        :type items: tuple of str
        :param kwargs: Optional parameters
        """
        super().__init__(win, x, y, width, height)

        self.items = items
        self.rows = len(items)
        self.rowHeight = self._height // self.rows
        self.selected = kwargs.get('default', 0)

        # Border
        self.borderThickness = kwargs.get('borderThickness', 3)
        self.borderColour = kwargs.get('borderColour', (0, 0, 0))
        self.radius = kwargs.get('radius', 0)

        # Radio
        self.circleRadius = int(kwargs.get('circleRadius', self._height / self.rows // 6))
        self.circleThickness = kwargs.get('circleThickness', 3)
        self.circleColour = kwargs.get('circleColour', (0, 0, 0))

        # Colour
        self.colour = kwargs.get('colour', (255, 255, 255))

        # Alternating colours: overrides colour
        self.colour1 = kwargs.get('colour1', self.colour)
        self.colour2 = kwargs.get('colour2', self.colour)

        # Text
        self.textColour = kwargs.get('textColour', (0, 0, 0))
        self.fontSize = kwargs.get('fontSize', 20)
        self.font = kwargs.get('font', pygame.font.SysFont('sans-serif', self.fontSize))
        self.texts = [self.font.render(self.items[row], True, self.textColour) for row in range(self.rows)]
        self.textRects = self.createTextRects()

        self.clicked = False

        self.circles = self.createCircleLocations()

    def createTextRects(self):
        textRects = []
        for row in range(self.rows):
            textRects.append(
                self.texts[row].get_rect(
                    center=(
                        self._x + self.circleRadius * 6 + (self._width - self.circleRadius * 6) // 2,
                        self._y + self.rowHeight * row + self.rowHeight // 2
                    )
                )
            )

        return textRects

    def createCircleLocations(self):
        circles = []
        for row in range(self.rows):
            circles.append((
                self._x + self.circleRadius * 3,
                self._y + self.rowHeight * row + self.rowHeight // 2,
            ))
        return circles

    def listen(self, events):
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                if mouseState == MouseState.CLICK:
                    for row in range(self.rows):
                        if math.sqrt((self.circles[row][0] - x) ** 2 +
                                     (self.circles[row][1] - y) ** 2) <= self.circleRadius:
                            self.selected = row

    def draw(self):
        """ Display to surface """
        if not self._hidden:
            for row in range(self.rows):
                colour = self.colour1 if not row % 2 else self.colour2
                if pygame.version.vernum[0] < 2:
                    pygame.draw.rect(
                        self.win, colour, (self._x, self._y + self.rowHeight * row, self._width, self.rowHeight)
                    )

                else:
                    if row == 0:
                        pygame.draw.rect(
                            self.win, colour, (self._x, self._y + self.rowHeight * row, self._width, self.rowHeight),
                            border_top_left_radius=self.radius, border_top_right_radius=self.radius
                        )

                    elif row == self.rows - 1:
                        pygame.draw.rect(
                            self.win, colour, (self._x, self._y + self.rowHeight * row, self._width, self.rowHeight),
                            border_bottom_left_radius=self.radius, border_bottom_right_radius=self.radius
                        )

                    else:
                        pygame.draw.rect(
                            self.win, colour, (self._x, self._y + self.rowHeight * row, self._width, self.rowHeight)
                        )

                width = 0 if row == self.selected else self.circleThickness
                pygame.draw.circle(
                    self.win, self.circleColour,
                    self.circles[row], self.circleRadius,
                    width
                )

                self.win.blit(self.texts[row], self.textRects[row])


if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode((1000, 800))

    checkbox = Checkbox(win, 100, 100, 400, 300, ('Apples', 'Bananas', 'Pears'), colour1=(0, 180, 0),
                        colour2=(0, 50, 200), fontSize=30, radius=10)
    radio = Radio(win, 550, 400, 400, 300, ('Apples', 'Bananas', 'Pears'), colour1=(0, 180, 0),
                  colour2=(0, 50, 200), fontSize=30, radius=10)

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
