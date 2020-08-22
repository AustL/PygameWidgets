import pygame

from pygame_widgets.widget import WidgetBase


class Checkbox(WidgetBase):
    def __init__(self, win, x, y, width, height, items, **kwargs):
        """ A collection of buttons

        :param win: Surface on which to draw
        :type win: pygame.Surface
        :param x: X-coordinate of top left
        :type x: int
        :param y: Y-coordinate of top left
        :type y: int
        :param width: Width of button
        :type width: int
        :param height: Height of button
        :type height: int
        :param items: Names of list items
        :type items: tuple of str
        :param kwargs: Optional parameters
        """
        super().__init__(win, x, y, width, height)

        self.items = items
        self.rows = len(items)
        self.rowHeight = self.height // self.rows
        self.selected = [False for _ in range(self.rows)]

        # TODO: border

        self.boxSize = kwargs.get('boxSize', self.height / self.rows // 3)
        self.boxThickness = kwargs.get('boxThickness', 3)
        self.boxColour = kwargs.get('boxColour', (0, 0, 0))
        # TODO: selected image (tick) / colour

        self.colour = kwargs.get('colour', (255, 255, 255))

        # Alternating colours: overrides colour
        self.colour1 = kwargs.get('colour1', self.colour)
        self.colour2 = kwargs.get('colour2', self.colour)
        self.textColour = kwargs.get('textColour', (0, 0, 0))

        self.fontSize = kwargs.get('fontSize', 20)
        self.font = kwargs.get('font', pygame.font.SysFont('calibri', self.fontSize))
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
                        self.x + self.boxSize * 2 + (self.width - self.boxSize * 2) // 2,
                        self.y + self.rowHeight * row + self.rowHeight // 2
                    )
                )
            )

        return textRects

    def createBoxLocations(self):
        boxes = []
        for row in range(self.rows):
            boxes.append(pygame.Rect(
                self.x + self.boxSize,
                self.y + self.rowHeight * row + self.boxSize,
                self.boxSize, self.boxSize
            ))
        return boxes

    def listen(self, events):
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if not self.hidden:
            pressed = pygame.mouse.get_pressed()[0]
            x, y = pygame.mouse.get_pos()

            if self.contains(x, y):
                if pressed:
                    if not self.clicked:
                        self.clicked = True
                        for row in range(self.rows):
                            if self.boxes[row].collidepoint(x, y):
                                self.selected[row] = not self.selected[row]

                elif self.clicked:
                    self.clicked = False

            elif not pressed:
                self.clicked = False

    def draw(self):
        """ Display to surface """
        if not self.hidden:
            for row in range(self.rows):
                colour = self.colour1 if not row % 2 else self.colour2
                pygame.draw.rect(self.win, colour, (self.x, self.y + self.rowHeight * row, self.width, self.rowHeight))

                width = 0 if self.selected[row] else self.boxThickness
                pygame.draw.rect(
                    self.win, self.boxColour,
                    self.boxes[row],
                    width=width
                )

                self.win.blit(self.texts[row], self.textRects[row])

    def getSelected(self):
        return [self.items[row] for row in range(self.rows) if self.selected[row]]


if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode((800, 800))

    checkbox = Checkbox(win, 100, 100, 400, 300, ('Apples', 'Bananas', 'Pears'), colour1=(0, 180, 0),
                        colour2=(0, 50, 200), fontSize=30)

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill((255, 255, 255))

        checkbox.listen(events)
        checkbox.draw()

        pygame.display.update()
