import pygame

from .widget import WidgetBase


def darker(color):
    assert len(color) == 3
    assert isinstance(color, tuple)

    color = list(color)
    new_color = []
    for c in color:
        if c - 30 > 10:
            new_color.append(c - 30)
        else:
            new_color.append(10)
    return tuple(new_color)


class Dropdown(WidgetBase):
    def __init__(self, win, x, y, width, height, name, choices, **kwargs):
        super().__init__(win, x, y, width, height)
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

            self.__choices.append(
                DropdownChoice(
                    self.win,
                    x,
                    y,
                    width,
                    height,
                    text=text,
                    drop=self,
                    value=values[i],
                    last=last,
                    **kwargs,
                )
            )
        self.__main = HeadDropdown(
            self.win,
            0,
            0,
            width,
            height,
            text=name,
            drop=self,
            **kwargs,
        )
        # Function
        self.onClick = kwargs.get('onClick', lambda *args: None)
        self.onRelease = kwargs.get('onRelease', lambda *args: None)
        self.onClickParams = kwargs.get('onClickParams', ())
        self.onReleaseParams = kwargs.get('onReleaseParams', ())
        self.clicked = False

    def listen(self, events):
        """ Wait for input

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """

        if not self._hidden:
            pressed = pygame.mouse.get_pressed()[0]

            if pressed:
                if not self.clicked:
                    self.clicked = True
                    self.onClick(*self.onClickParams)

                elif self.clicked:
                    self.clicked = False
                    self.onRelease(*self.onReleaseParams)
            else:
                self.clicked = False

            # Then we handle the DropdownChoices
            self.__main.listen(events)
            for c in self.__choices:
                c.listen(events)

    def draw(self):
        if not self._hidden:
            self.__main.draw()
            if self.dropped:  # dropped
                for c in self.__choices:
                    c.draw()

    def reset(self):
        self.__chosen = None

    def contains(self, x, y) -> bool:
        return any([c.contains(x, y) for c in self.__choices])

    def getSelected(self):
        return self.__chosen._value if self.__chosen is not None else None

    @property
    def dropped(self):
        return self._dropped

    @dropped.setter
    def dropped(self, new_dropped):
        if isinstance(new_dropped, bool):
            self._dropped = new_dropped
        else:
            raise TypeError('Wrong type for \'dropped\' property, boolean is expected')

    @property
    def chosen(self):
        return self.__chosen

    @chosen.setter
    def chosen(self, new_chosen):
        if isinstance(new_chosen, DropdownChoice):
            self.__chosen = new_chosen
        else:
            raise TypeError(
                'Wrong type for \'chosen\' property, DropdownChoice is expected'
            )


class DropdownChoice(WidgetBase):
    def __init__(self, win, x, y, width, height, text, drop, last, **kwargs):
        super().__init__(win, x, y, width, height)

        self.__text = text

        self._drop = drop
        self._value = kwargs.get('value', text)
        # Border
        self.borderThickness = kwargs.get('borderThickness', 3)
        self.borderColour = kwargs.get('borderColour', (0, 0, 0))
        self.borderRadius = kwargs.get('borderRadius', 0)

        # Colour
        self.inactiveColour = kwargs.get('inactiveColour', (150, 150, 150))
        self.hoverColour = kwargs.get('hoverColour', (125, 125, 125))
        self.pressedColour = kwargs.get('pressedColour', (100, 100, 100))
        self.colour = self.inactiveColour

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
                darker(self.colour),
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
        if not self._hidden:
            pressed = pygame.mouse.get_pressed()[0]
            x, y = pygame.mouse.get_pos()

            if self.contains(x, y):
                if pressed:
                    self.colour = self.pressedColour
                    if not self.clicked:
                        self.clicked = True

                        self._drop.dropped = False
                        self._drop.chosen = self

                elif self.clicked:
                    self.clicked = False

                else:
                    self.colour = self.hoverColour

            elif not pressed:
                self.clicked = False
                self.colour = self.inactiveColour

    def contains(self, x, y) -> bool:
        return (
                self.computedX < x < self.computedX + self._width
                and self.computedY < y < self.computedY + self._height
        )

    def _computeBorderRadii(self):
        border_radius = {}
        if not self.last:
            return border_radius
        if self.direction == 'up':
            border_radius['border_top_left_radius'] = self.borderRadius
            border_radius['border_top_right_radius'] = self.borderRadius

        elif self.direction == 'down':
            border_radius['border_bottom_left_radius'] = self.borderRadius
            border_radius['border_bottom_right_radius'] = self.borderRadius

        elif self.direction == 'right':
            border_radius['border_top_right_radius'] = self.borderRadius
            border_radius['border_bottom_right_radius'] = self.borderRadius

        elif self.direction == 'left':
            border_radius['border_top_left_radius'] = self.borderRadius
            border_radius['border_bottom_left_radius'] = self.borderRadius

        return border_radius

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, new_text):
        if isinstance(new_text, str):
            self.__text = new_text
        else:
            raise TypeError('Wrong type for \'text\' property, str is expected')

    @property
    def direction(self):
        return self.__direction

    @property
    def last(self):
        return self.__last

    @last.setter
    def last(self, new_last):
        if isinstance(new_last, bool):
            self.__last = new_last
        else:
            raise TypeError('Wrong type for \'last\' property, boolean is expected')

    @direction.setter
    def direction(self, new_direction):
        if isinstance(new_direction, str):
            self.__direction = new_direction
        else:
            raise TypeError('Wrong type for \'direction\' property, str is expected')

    @property
    def computedX(self):
        return self._drop.getX() + self._x

    @property
    def computedY(self):
        return self._drop.getY() + self._y


class HeadDropdown(DropdownChoice):
    def __init__(self, win, x, y, width, height, text, drop, **kwargs):
        super().__init__(
            win,
            x,
            y,
            width,
            height,
            text,
            drop,
            True,
            **kwargs
        )
        self.__head_text = text

    def listen(self, events):
        """Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if not self._hidden:
            pressed = pygame.mouse.get_pressed()[0]
            right_click_pressed = pygame.mouse.get_pressed()[2]
            x, y = pygame.mouse.get_pos()

            if self.contains(x, y):
                if pressed:
                    self.colour = self.pressedColour
                    if not self.clicked:
                        self.clicked = True

                        self._drop.dropped = not self._drop.dropped

                elif self.clicked:
                    self.clicked = False

                else:
                    self.colour = self.hoverColour

                if right_click_pressed:
                    self._drop.reset()

            elif not pressed:
                self.clicked = False
                self.colour = self.inactiveColour

    def _computeBorderRadii(self):
        border_radius = {}
        if not self.last:
            return border_radius
        if self._drop.dropped:
            if self.direction == 'up':
                border_radius['border_bottom_left_radius'] = self.borderRadius
                border_radius['border_bottom_right_radius'] = self.borderRadius

            elif self.direction == 'down':
                border_radius['border_top_left_radius'] = self.borderRadius
                border_radius['border_top_right_radius'] = self.borderRadius

            elif self.direction == 'left':
                border_radius['border_top_right_radius'] = self.borderRadius
                border_radius['border_bottom_right_radius'] = self.borderRadius

            elif self.direction == 'right':
                border_radius['border_top_left_radius'] = self.borderRadius
                border_radius['border_bottom_left_radius'] = self.borderRadius
        else:
            border_radius['border_top_left_radius'] = self.borderRadius
            border_radius['border_bottom_left_radius'] = self.borderRadius
            border_radius['border_top_right_radius'] = self.borderRadius
            border_radius['border_bottom_right_radius'] = self.borderRadius

        return border_radius

    @property
    def text(self):
        return self._drop.chosen.text if self._drop.chosen is not None else self.__head_text


if __name__ == '__main__':
    from pygame_widgets.button import Button

    pygame.init()
    win = pygame.display.set_mode((400, 280))
    width, height = pygame.display.get_window_size()

    dropdown = Dropdown(
        win, 120, 10, 100, 50, name='Select Color',
        choices=[
            'Red',
            'Blue',
            'Yellow',
        ],
        borderRadius=3, colour=pygame.Color('green'), values=[1, 2, 'true'], direction='down', textHAlign='left'
    )


    def print_value():
        print(dropdown.getSelected())


    button = Button(
        win, 10, 10, 100, 50, text='Print Value', fontSize=30,
        margin=20, inactiveColour=(255, 0, 0), pressedColour=(0, 255, 0),
        radius=5, onClick=print_value, font=pygame.font.SysFont('calibri', 10),
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

        dropdown.listen(events)
        dropdown.draw()
        button.listen(events)
        button.draw()

        pygame.display.update()
