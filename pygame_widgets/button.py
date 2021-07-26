import pygame

import pygame_widgets
from pygame_widgets.widget import WidgetBase
from pygame_widgets.mouse import Mouse, MouseState


class Button(WidgetBase):
    def __init__(self, win, x, y, width, height, isSubWidget=False, **kwargs):
        """ A customisable button for Pygame

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

        # Colour
        self.inactiveColour = kwargs.get('inactiveColour', (150, 150, 150))
        self.hoverColour = kwargs.get('hoverColour', (125, 125, 125))
        self.pressedColour = kwargs.get('pressedColour', (100, 100, 100))
        self.colour = kwargs.get('colour', self.inactiveColour)  # Allows colour to override inactiveColour
        self.inactiveColour = self.colour
        self.shadowDistance = kwargs.get('shadowDistance', 0)
        self.shadowColour = kwargs.get('shadowColour', (210, 210, 180))

        # Function
        self.onClick = kwargs.get('onClick', lambda *args: None)
        self.onRelease = kwargs.get('onRelease', lambda *args: None)
        self.onClickParams = kwargs.get('onClickParams', ())
        self.onReleaseParams = kwargs.get('onReleaseParams', ())
        self.clicked = False

        # Text (Remove if using PyInstaller)
        self.textColour = kwargs.get('textColour', (0, 0, 0))
        self.fontSize = kwargs.get('fontSize', 20)
        self.string = kwargs.get('text', '')
        self.font = kwargs.get('font', pygame.font.SysFont('sans-serif', self.fontSize))
        self.text = self.font.render(self.string, True, self.textColour)
        self.textHAlign = kwargs.get('textHAlign', 'centre')
        self.textVAlign = kwargs.get('textVAlign', 'centre')
        self.margin = kwargs.get('margin', 20)

        self.textRect = self.text.get_rect()
        self.alignTextRect()

        # Image
        self.image = kwargs.get('image', None)
        self.imageHAlign = kwargs.get('imageHAlign', 'centre')
        self.imageVAlign = kwargs.get('imageVAlign', 'centre')

        if self.image:
            self.imageRect = self.image.get_rect()
            self.alignImageRect()

        # Border
        self.borderThickness = kwargs.get('borderThickness', 0)
        self.inactiveBorderColour = kwargs.get('inactiveBorderColour', (0, 0, 0))
        self.hoverBorderColour = kwargs.get('hoverBorderColour', (80, 80, 80))
        self.pressedBorderColour = kwargs.get('pressedBorderColour', (100, 100, 100))
        self.borderColour = kwargs.get('borderColour', self.inactiveBorderColour)
        self.inactiveBorderColour = self.borderColour
        self.radius = kwargs.get('radius', 0)

    def alignImageRect(self):
        self.imageRect.center = (self._x + self._width // 2, self._y + self._height // 2)

        if self.imageHAlign == 'left':
            self.imageRect.left = self._x + self.margin
        elif self.imageHAlign == 'right':
            self.imageRect.right = self._x + self._width - self.margin

        if self.imageVAlign == 'top':
            self.imageRect.top = self._y + self.margin
        elif self.imageVAlign == 'bottom':
            self.imageRect.bottom = self._y + self._height - self.margin

    def alignTextRect(self):
        self.textRect.center = (self._x + self._width // 2, self._y + self._height // 2)

        if self.textHAlign == 'left':
            self.textRect.left = self._x + self.margin
        elif self.textHAlign == 'right':
            self.textRect.right = self._x + self._width - self.margin

        if self.textVAlign == 'top':
            self.textRect.top = self._y + self.margin
        elif self.textVAlign == 'bottom':
            self.textRect.bottom = self._y + self._height - self.margin

    def listen(self, events):
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                if mouseState == MouseState.RELEASE and self.clicked:
                    self.clicked = False
                    self.onRelease(*self.onReleaseParams)

                elif mouseState == MouseState.CLICK:
                    self.clicked = True
                    self.onClick(*self.onClickParams)
                    self.colour = self.pressedColour
                    self.borderColour = self.pressedBorderColour

                elif mouseState == MouseState.DRAG and self.clicked:
                    self.colour = self.pressedColour
                    self.borderColour = self.pressedBorderColour

                elif mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    self.colour = self.hoverColour
                    self.borderColour = self.hoverBorderColour

            else:
                self.clicked = False
                self.colour = self.inactiveColour
                self.borderColour = self.inactiveBorderColour

    def draw(self):
        """ Display to surface """
        if not self._hidden:
            if pygame.version.vernum[0] < 2:
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
            else:
                pygame.draw.rect(
                    self.win, self.shadowColour,
                    (self._x + self.shadowDistance, self._y + self.shadowDistance, self._width, self._height),
                    border_radius=self.radius
                )

                pygame.draw.rect(
                    self.win, self.borderColour, (self._x, self._y, self._width, self._height),
                    border_radius=self.radius
                )

                pygame.draw.rect(
                    self.win, self.colour, (self._x + self.borderThickness, self._y + self.borderThickness,
                                            self._width - self.borderThickness * 2,
                                            self._height - self.borderThickness * 2),
                    border_radius=self.radius
                )

            if self.image:
                self.imageRect = self.image.get_rect()
                self.alignImageRect()
                self.win.blit(self.image, self.imageRect)

            self.textRect = self.text.get_rect()
            self.alignTextRect()
            self.win.blit(self.text, self.textRect)

    def setImage(self, image):
        self.image = image
        self.imageRect = self.image.get_rect()
        self.alignImageRect()

    def setOnClick(self, onClick, params=()):
        self.onClick = onClick
        self.onClickParams = params

    def setOnRelease(self, onRelease, params=()):
        self.onRelease = onRelease
        self.onReleaseParams = params

    def setInactiveColour(self, colour):
        self.inactiveColour = colour

    def setPressedColour(self, colour):
        self.pressedColour = colour

    def setHoverColour(self, colour):
        self.hoverColour = colour

    def get(self, attr):
        parent = super().get(attr)
        if parent is not None:
            return parent

        if attr == 'colour':
            return self.colour

    def set(self, attr, value):
        super().set(attr, value)

        if attr == 'colour':
            self.inactiveColour = value


class ButtonArray(WidgetBase):
    def __init__(self, win, x, y, width, height, shape, **kwargs):
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
        :param shape: The 2d shape of the array (columns, rows)
        :type shape: tuple of int
        :param kwargs: Optional parameters
        """
        super().__init__(win, x, y, width, height)

        self.shape = shape
        self.numButtons = shape[0] * shape[1]

        # Array
        self.colour = kwargs.get('colour', (210, 210, 180))
        self.border = kwargs.get('border', 10)
        self.topBorder = kwargs.get('topBorder', self.border)
        self.bottomBorder = kwargs.get('bottomBorder', self.border)
        self.leftBorder = kwargs.get('leftBorder', self.border)
        self.rightBorder = kwargs.get('rightBorder', self.border)
        self.borderRadius = kwargs.get('borderRadius', 0)
        self.separationThickness = kwargs.get('separationThickness', self.border)

        self.buttonAttributes = {
            # Colour
            'inactiveColour': kwargs.get('inactiveColours', None),
            'hoverColour': kwargs.get('hoverColours', None),
            'pressedColour': kwargs.get('pressedColours', None),
            'shadowDistance': kwargs.get('shadowDistances', None),
            'shadowColour': kwargs.get('shadowColours', None),

            # Function
            'onClick': kwargs.get('onClicks', None),
            'onRelease': kwargs.get('onReleases', None),
            'onClickParams': kwargs.get('onClickParams', None),
            'onReleaseParams': kwargs.get('onReleaseParams', None),

            # Text
            'textColour': kwargs.get('textColours', None),
            'fontSize': kwargs.get('fontSizes', None),
            'text': kwargs.get('texts', None),
            'font': kwargs.get('fonts', None),
            'textHAlign': kwargs.get('textHAligns', None),
            'textVAlign': kwargs.get('textVAligns', None),
            'margin': kwargs.get('margins', None),

            # Image
            'image': kwargs.get('images', None),
            'imageHAlign': kwargs.get('imageHAligns', None),
            'imageVAlign': kwargs.get('imageVAligns', None),
            'imageRotation': kwargs.get('imageRotations', None),
            'imageFill': kwargs.get('imageFills', None),
            'imageZoom': kwargs.get('imageZooms', None),
            'radius': kwargs.get('radii', None)
        }

        self.buttons = []
        self.createButtons()

    def createButtons(self):
        across, down = self.shape
        width = (self._width - self.separationThickness * (across - 1) - self.leftBorder - self.rightBorder) // across
        height = (self._height - self.separationThickness * (down - 1) - self.topBorder - self.bottomBorder) // down

        count = 0
        for i in range(across):
            for j in range(down):
                x = self._x + i * (width + self.separationThickness) + self.leftBorder
                y = self._y + j * (height + self.separationThickness) + self.topBorder
                self.buttons.append(Button(self.win, x, y, width, height, isSubWidget=True,
                                           **{k: v[count] for k, v in self.buttonAttributes.items() if v is not None})
                                    )
                count += 1

    def listen(self, events):
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if not self._hidden and not self._disabled:
            for button in self.buttons:
                button.listen(events)

    def draw(self):
        """ Display to surface """
        if not self._hidden:
            rects = [
                (self._x + self.borderRadius, self._y, self._width - self.borderRadius * 2, self._height),
                (self._x, self._y + self.borderRadius, self._width, self._height - self.borderRadius * 2)
            ]

            circles = [
                (self._x + self.borderRadius, self._y + self.borderRadius),
                (self._x + self.borderRadius, self._y + self._height - self.borderRadius),
                (self._x + self._width - self.borderRadius, self._y + self.borderRadius),
                (self._x + self._width - self.borderRadius, self._y + self._height - self.borderRadius)
            ]

            for rect in rects:
                pygame.draw.rect(self.win, self.colour, rect)

            for circle in circles:
                pygame.draw.circle(self.win, self.colour, circle, self.borderRadius)

            for button in self.buttons:
                button.draw()

    def getButtons(self):
        return self.buttons


if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode((600, 600))

    button = Button(win, 100, 100, 300, 150, text='Hello', fontSize=50, margin=20,
                    inactiveColour=(255, 0, 0), pressedColour=(0, 255, 0), radius=20,
                    onClick=lambda: print('Click'), font=pygame.font.SysFont('calibri', 10),
                    textVAlign='bottom', imageHAlign='centre', imageVAlign='centre', borderThickness=3,
                    onRelease=lambda: print('Release'), shadowDistance=5, borderColour=(0, 0, 0))

    buttonArray = ButtonArray(win, 50, 50, 500, 500, (2, 2), border=100, texts=('1', '2', '3', '4'),
                              onClicks=(lambda: print(1), lambda: print(2), lambda: print(3), lambda: print(4)))

    buttonArray.hide()

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
