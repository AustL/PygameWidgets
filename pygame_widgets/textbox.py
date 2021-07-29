import pygame
import time

import pygame_widgets
from pygame_widgets.widget import WidgetBase
from pygame_widgets.mouse import Mouse, MouseState


class TextBox(WidgetBase):
    # Times in ms
    REPEAT_DELAY = 400
    REPEAT_INTERVAL = 70
    CURSOR_INTERVAL = 400

    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        """ A customisable textbox for Pygame

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
        :param kwargs: Optional parameters
        """
        super().__init__(win, x, y, width, height, isSubWidget)

        self.selected = False
        self.showCursor = False
        self.cursorTime = 0
        self.cursorPosition = 0

        self.repeatTime = 0
        self.repeatKey = None
        self.firstRepeat = True
        self.keyDown = False

        self.text = []

        self.escape = False

        self.maxLengthReached = False

        # Border
        self.borderThickness = kwargs.get('borderThickness', 3)
        self.borderColour = kwargs.get('borderColour', (0, 0, 0))
        self.radius = kwargs.get('radius', 0)

        # Colour
        self.colour = kwargs.get('colour', (220, 220, 220))

        # Text
        self.placeholderText = kwargs.get('placeholderText', '')
        self.textColour = kwargs.get('textColour', (0, 0, 0))
        self.fontSize = kwargs.get('fontSize', 20)
        self.font = kwargs.get('font', pygame.font.SysFont('sans-serif', self.fontSize))

        self.textOffsetBottom = self.fontSize // 3
        self.textOffsetLeft = self.fontSize // 3
        self.textOffsetRight = self.fontSize // 2
        self.cursorOffsetTop = self._height // 6

        # Functions
        self.onSubmit = kwargs.get('onSubmit', lambda *args: None)
        self.onSubmitParams = kwargs.get('onSubmitParams', ())
        self.onTextChanged = kwargs.get('onTextChanged', lambda *args: None)
        self.onTextChangedParams = kwargs.get('onTextChangedParams', ())

    def listen(self, events):
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if not self._hidden and not self._disabled:
            if self.keyDown:
                self.updateRepeatKey()

            # Selection
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if mouseState == MouseState.CLICK:
                if self.contains(x, y):
                    self.selected = True
                    self.showCursor = True
                    self.cursorTime = time.time()

                else:
                    self.selected = False
                    self.showCursor = False
                    self.cursorTime = time.time()

            # Keyboard Input
            if self.selected:
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        self.showCursor = True
                        self.keyDown = True
                        self.repeatKey = event
                        self.repeatTime = time.time()

                        if event.key == pygame.K_BACKSPACE:
                            if self.cursorPosition != 0:
                                self.maxLengthReached = False
                                self.text.pop(self.cursorPosition - 1)
                                self.onTextChanged(*self.onTextChangedParams)

                            self.cursorPosition = max(self.cursorPosition - 1, 0)

                        elif event.key == pygame.K_DELETE:
                            if not self.cursorPosition >= len(self.text):
                                self.maxLengthReached = False
                                self.text.pop(self.cursorPosition)
                                self.onTextChanged(*self.onTextChangedParams)

                        elif event.key == pygame.K_RETURN:
                            self.onSubmit(*self.onSubmitParams)

                        elif event.key == pygame.K_RIGHT:
                            self.cursorPosition = min(self.cursorPosition + 1, len(self.text))

                        elif event.key == pygame.K_LEFT:
                            self.cursorPosition = max(self.cursorPosition - 1, 0)

                        elif event.key == pygame.K_END:
                            self.cursorPosition = len(self.text)

                        elif event.key == pygame.K_ESCAPE:
                            if not self.escape:
                                self.selected = False
                                self.showCursor = False
                                self.escape = True
                                self.repeatKey = None
                                self.keyDown = None
                                self.firstRepeat = True

                        elif not self.maxLengthReached:
                            if len(event.unicode) > 0:
                                self.text.insert(self.cursorPosition, event.unicode)
                                self.cursorPosition += 1
                                self.onTextChanged(*self.onTextChangedParams)

                    elif event.type == pygame.KEYUP:
                        self.repeatKey = None
                        self.keyDown = None
                        self.firstRepeat = True
                        self.escape = False

    def draw(self):
        """ Display to surface """
        if not self._hidden:
            if self.selected:
                self.updateCursor()

            borderRects = [
                (self._x + self.radius, self._y, self._width - self.radius * 2, self._height),
                (self._x, self._y + self.radius, self._width, self._height - self.radius * 2),
            ]

            borderCircles = [
                (self._x + self.radius, self._y + self.radius),
                (self._x + self.radius, self._y + self._height - self.radius),
                (self._x + self._width - self.radius, self._y + self.radius),
                (self._x + self._width - self.radius, self._y + self._height - self.radius)
            ]

            backgroundRects = [
                (
                    self._x + self.borderThickness + self.radius,
                    self._y + self.borderThickness,
                    self._width - 2 * (self.borderThickness + self.radius),
                    self._height - 2 * self.borderThickness
                ),
                (
                    self._x + self.borderThickness,
                    self._y + self.borderThickness + self.radius,
                    self._width - 2 * self.borderThickness,
                    self._height - 2 * (self.borderThickness + self.radius)
                )
            ]

            backgroundCircles = [
                (self._x + self.radius + self.borderThickness,
                 self._y + self.radius + self.borderThickness),
                (self._x + self.radius + self.borderThickness,
                 self._y + self._height - self.radius - self.borderThickness),
                (self._x + self._width - self.radius - self.borderThickness,
                 self._y + self.radius + self.borderThickness),
                (self._x + self._width - self.radius - self.borderThickness,
                 self._y + self._height - self.radius - self.borderThickness)
            ]

            for rect in borderRects:
                pygame.draw.rect(self.win, self.borderColour, rect)

            for circle in borderCircles:
                pygame.draw.circle(self.win, self.borderColour, circle, self.radius)

            for rect in backgroundRects:
                pygame.draw.rect(self.win, self.colour, rect)

            for circle in backgroundCircles:
                pygame.draw.circle(self.win, self.colour, circle, self.radius)

            x = [self._x + self.textOffsetLeft]
            for c in self.text:
                text = self.font.render(c, True, self.textColour)
                textRect = text.get_rect(bottomleft=(x[-1], self._y + self._height - self.textOffsetBottom))
                self.win.blit(text, textRect)
                x.append(x[-1] + text.get_width())

            if self.showCursor:
                try:
                    pygame.draw.line(
                        self.win, (0, 0, 0),
                        (x[self.cursorPosition], self._y + self.cursorOffsetTop),
                        (x[self.cursorPosition], self._y + self._height - self.cursorOffsetTop)
                    )
                except IndexError:
                    self.cursorPosition -= 1

            if x[-1] > self._x + self._width - self.textOffsetRight:
                self.maxLengthReached = True

    def updateCursor(self):
        now = time.time()

        if now - self.cursorTime >= self.CURSOR_INTERVAL / 1000:
            self.showCursor = not self.showCursor
            self.cursorTime = now

    def updateRepeatKey(self):
        now = time.time()

        if self.firstRepeat:
            if now - self.repeatTime >= self.REPEAT_DELAY / 1000:
                self.firstRepeat = False
                self.repeatTime = now
                pygame.event.post(
                    pygame.event.Event(
                        pygame.KEYDOWN,
                        {'key': self.repeatKey.key, 'unicode': self.repeatKey.unicode}
                    )
                )

        elif now - self.repeatTime >= self.REPEAT_INTERVAL / 1000:
            self.repeatTime = now
            pygame.event.post(
                pygame.event.Event(
                    pygame.KEYDOWN,
                    {'key': self.repeatKey.key, 'unicode': self.repeatKey.unicode}
                )
            )

    def setText(self, text):
        self.text = [c for c in str(text)]
        self.cursorPosition = len(self.text)
        self.maxLengthReached = False

    def getText(self):
        return ''.join(self.text)


if __name__ == '__main__':
    def output():
        print(len(textbox.getText()))
        textbox.setText('')


    pygame.init()
    win = pygame.display.set_mode((1000, 600))

    textbox = TextBox(win, 100, 100, 800, 80, fontSize=50, borderColour=(255, 0, 0),
                      textColour=(0, 200, 0), onSubmit=output, radius=10,
                      borderThickness=5)

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
