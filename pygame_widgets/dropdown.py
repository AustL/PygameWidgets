import pygame

import pygame_widgets
from pygame_widgets.widget import WidgetBase
from pygame_widgets.mouse import Mouse, MouseState


class Dropdown(WidgetBase):
    def __init__(self, win, x, y, width, height, name, choices, isSubWidget=False, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget)
        self._dropped = False
        self.__chosen = None

        values = kwargs.get('values', None)
        if values is None:
            values = choices[:]  # we copy the choices if value is empty

        if len(values) != len(choices):
            raise Exception(
                '\'choices\' and \'values\' arguments should be identical in size'
            )

        # we create the DropdownChoice(s)
        direction = kwargs.get('direction', 'down')
        self.__choices = []
        for i, text in enumerate(choices):
            last = (i == len(choices) - 1)

            if direction == 'down':
                x = 0
                y = (i + 1) * height

            elif direction == 'up':
                x = 0
                y = -(i + 1) * height

            elif direction == 'right':
                x = (i + 1) * width
                y = 0

            elif direction == 'left':
                x = -(i + 1) * width
                y = 0

            choice = DropdownChoice(
                self.win, x, y, width, height,
                text=text, dropdown=self, value=values[i], last=last,
                **kwargs
            )
            choice.hide()
            self.__choices.append(choice)

        self.__main = HeadDropdown(
            self.win, 0, 0, width, height,
            text=name, dropdown=self,
            **kwargs
        )

        # Function
        self.onClick = kwargs.get('onClick', lambda *args: None)
        self.onRelease = kwargs.get('onRelease', lambda *args: None)
        self.onClickParams = kwargs.get('onClickParams', ())
        self.onReleaseParams = kwargs.get('onReleaseParams', ())

    def listen(self, events):
        """ Wait for input

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                if mouseState == MouseState.CLICK:
                    self.onClick(*self.onClickParams)

                elif mouseState == MouseState.RELEASE:
                    self.onRelease(*self.onReleaseParams)

            # Then we handle the DropdownChoices
            self.__main.listen(events)
            for c in self.__choices:
                c.listen(events)

    def draw(self):
        if not self._hidden:
            self.__main.draw()
            for c in self.__choices:
                c.draw()

    def contains(self, x, y):
        return super().contains(x, y) or (any([c.contains(x, y) for c in self.__choices]) and self._dropped)

    def reset(self):
        self.__chosen = None

    def getSelected(self):
        return self.__chosen._value if self.__chosen is not None else None

    def toggleDropped(self):
        self._dropped = not self._dropped
        if self._dropped:
            for c in self.__choices:
                c.show()
                self.moveToTop()
        else:
            for c in self.__choices:
                c.hide()

    def isDropped(self):
        return self._dropped

    @property
    def chosen(self):
        return self.__chosen

    @chosen.setter
    def chosen(self, newChosen):
        if isinstance(newChosen, DropdownChoice):
            self.__chosen = newChosen
        else:
            raise TypeError(
                'Wrong type for \'chosen\' property, DropdownChoice is expected'
            )

    def setDropped(self, drop):
        if drop != self._dropped:
            self.toggleDropped()


class DropdownChoice(WidgetBase):
    def __init__(self, win, x, y, width, height, text: str, dropdown: Dropdown, last: bool, **kwargs):
        super().__init__(win, x, y, width, height, isSubWidget=True)

        self.__text = text

        self._dropdown = dropdown
        self._value = kwargs.get('value', text)
        # Border
        self.borderThickness = kwargs.get('borderThickness', 3)
        self.borderColour = kwargs.get('borderColour', (0, 0, 0))
        self.borderRadius = kwargs.get('borderRadius', 0)

        # Colour
        self.inactiveColour = kwargs.get('inactiveColour', (150, 150, 150))
        self.hoverColour = kwargs.get('hoverColour', (125, 125, 125))
        self.pressedColour = kwargs.get('pressedColour', (100, 100, 100))
        self.colour = kwargs.get('colour', self.inactiveColour)  # Allows colour to override inactiveColour
        self.inactiveColour = self.colour

        # Text
        self.textColour = kwargs.get('textColour', (0, 0, 0))
        self.fontSize = kwargs.get('fontSize', 20)
        self.font = kwargs.get('font', pygame.font.SysFont('sans-serif', self.fontSize))
        self.textHAlign = kwargs.get('textHAlign', 'centre')

        self.textOffsetLeft = self.fontSize // 5
        self.textOffsetRight = self.fontSize // 5

        # action
        self.clicked = False

        self.__direction = kwargs.get('direction', 'down')
        self.__last = last

    def draw(self):
        if not self._hidden:
            rect = pygame.Rect(
                self.computedX,
                self.computedY,
                self._width,
                self._height,
            )
            pygame.draw.rect(
                self.win,
                self.colour,
                rect,
                **self._computeBorderRadii()
            )

            text_rendered = self.font.render(self.text, True, self.textColour)

            if self.textHAlign == 'centre':
                text_rect = text_rendered.get_rect(
                    center=(
                        self.computedX + self._width // 2,
                        self.computedY + self._height // 2,
                    )
                )
            elif self.textHAlign == 'left':
                text_rect = text_rendered.get_rect(
                    center=(
                        self.computedX + text_rendered.get_width() // 2 + self.textOffsetLeft,
                        self.computedY + self._height // 2,
                    )
                )
            elif self.textHAlign == 'right':
                text_rect = text_rendered.get_rect(
                    center=(
                        self.computedX - text_rendered.get_width() // 2 + self._width - self.textOffsetRight,
                        self.computedY + self._height // 2,
                    )
                )

            self.win.blit(text_rendered, text_rect)

    def listen(self, events):
        """Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                if mouseState == MouseState.RELEASE and self.clicked:
                    self.clicked = False
                    self._dropdown.setDropped(False)
                    self._dropdown.chosen = self

                elif mouseState == MouseState.CLICK:
                    self.clicked = True
                    self.colour = self.pressedColour

                elif mouseState == MouseState.DRAG and self.clicked:
                    self.colour = self.pressedColour

                elif mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    self.colour = self.hoverColour

            else:
                self.clicked = False
                self.colour = self.inactiveColour

    def contains(self, x, y) -> bool:
        return (
                self.computedX < x < self.computedX + self._width
                and self.computedY < y < self.computedY + self._height
        )

    def _computeBorderRadii(self):
        borderRadius = {}
        if not self.last:
            return borderRadius
        if self.direction == 'up':
            borderRadius['border_top_left_radius'] = self.borderRadius
            borderRadius['border_top_right_radius'] = self.borderRadius

        elif self.direction == 'down':
            borderRadius['border_bottom_left_radius'] = self.borderRadius
            borderRadius['border_bottom_right_radius'] = self.borderRadius

        elif self.direction == 'right':
            borderRadius['border_top_right_radius'] = self.borderRadius
            borderRadius['border_bottom_right_radius'] = self.borderRadius

        elif self.direction == 'left':
            borderRadius['border_top_left_radius'] = self.borderRadius
            borderRadius['border_bottom_left_radius'] = self.borderRadius

        return borderRadius

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, newText):
        if isinstance(newText, str):
            self.__text = newText
        else:
            raise TypeError('Wrong type for \'text\' property, str is expected')

    @property
    def direction(self):
        return self.__direction

    @property
    def last(self):
        return self.__last

    @last.setter
    def last(self, newLast):
        if isinstance(newLast, bool):
            self.__last = newLast
        else:
            raise TypeError('Wrong type for \'last\' property, boolean is expected')

    @direction.setter
    def direction(self, newDirection):
        if isinstance(newDirection, str):
            self.__direction = newDirection
        else:
            raise TypeError('Wrong type for \'direction\' property, str is expected')

    @property
    def computedX(self):
        return self._dropdown.getX() + self._x

    @property
    def computedY(self):
        return self._dropdown.getY() + self._y


class HeadDropdown(DropdownChoice):
    def __init__(self, win, x, y, width, height, text, dropdown, **kwargs):
        super().__init__(
            win, x, y, width, height,
            text, dropdown, last=True,
            **kwargs
        )
        self.__head_text = text

    def listen(self, events):
        """Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                if mouseState == MouseState.CLICK:
                    self.clicked = True
                    self._dropdown.toggleDropped()

                elif mouseState == MouseState.DRAG and self.clicked:
                    self.colour = self.pressedColour

                elif mouseState == MouseState.RELEASE:
                    self.clicked = False

                elif mouseState == MouseState.HOVER or mouseState == MouseState.DRAG:
                    self.colour = self.hoverColour

                elif mouseState == MouseState.RIGHT_CLICK:
                    self._dropdown.reset()

            else:
                self.clicked = False
                self.colour = self.inactiveColour

    def _computeBorderRadii(self):
        borderRadius = {}
        if not self.last:
            return borderRadius
        if self._dropdown.isDropped():
            if self.direction == 'up':
                borderRadius['border_bottom_left_radius'] = self.borderRadius
                borderRadius['border_bottom_right_radius'] = self.borderRadius

            elif self.direction == 'down':
                borderRadius['border_top_left_radius'] = self.borderRadius
                borderRadius['border_top_right_radius'] = self.borderRadius

            elif self.direction == 'left':
                borderRadius['border_top_right_radius'] = self.borderRadius
                borderRadius['border_bottom_right_radius'] = self.borderRadius

            elif self.direction == 'right':
                borderRadius['border_top_left_radius'] = self.borderRadius
                borderRadius['border_bottom_left_radius'] = self.borderRadius
        else:
            borderRadius['border_top_left_radius'] = self.borderRadius
            borderRadius['border_bottom_left_radius'] = self.borderRadius
            borderRadius['border_top_right_radius'] = self.borderRadius
            borderRadius['border_bottom_right_radius'] = self.borderRadius

        return borderRadius

    @property
    def text(self):
        return self._dropdown.chosen.text if self._dropdown.chosen is not None else self.__head_text


if __name__ == '__main__':
    from pygame_widgets.button import Button

    pygame.init()
    win = pygame.display.set_mode((400, 280))
    width, height = pygame.display.get_window_size()

    dropdown = Dropdown(
        win, 120, 10, 100, 50, name='Select Colour',
        choices=['Red', 'Blue', 'Yellow'], colour=(200, 0, 0),
        borderRadius=3, values=[1, 2, 'true'], direction='down', textHAlign='left'
    )


    def printValue():
        print(dropdown.getSelected())


    button = Button(
        win, 120, 100, 100, 50, text='Print Value', fontSize=30,
        margin=20, inactiveColour=(255, 0, 0), pressedColour=(0, 255, 0),
        radius=5, onClick=printValue, font=pygame.font.SysFont('calibri', 10),
        textVAlign='bottom'
    )

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
