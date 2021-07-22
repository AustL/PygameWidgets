import pygame

from pygame_widgets.widget import WidgetBase
from pygame_widgets.textbox import TextBox


class SearchBar(WidgetBase):
    def __init__(self, win, x, y, width, height, choices, **kwargs):
        """Initialize a customisable search bar for Pygame.

        The bar can be written on, and displays under it the results.

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
        :param choices: Possible search values
        :type choices: list(str)
        :param kwargs: Optional parameters
        """
        super().__init__(win, x, y, width, height)
        self._dropped = False
        self.__chosen = None

        self.choices = choices

        self.text_bar = TextBox(win, x, y, width, height, **kwargs)

    def listen(self, events):
        """Wait for input.

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if not self._hidden:
            self.text_bar.listen(events)

    def draw(self):
        """Draw the widget."""
        if not self._hidden:
            self.text_bar.draw()
            if self.dropped:
                print('Must show possbilities.')
                print('Should also check wheter to update')


    @property
    def dropped(self):
        return self._dropped

    @dropped.setter
    def dropped(self, new_dropped):
        if isinstance(new_dropped, bool):
            self._dropped = new_dropped
        else:
            raise TypeError('Wrong type for \'dropped\' property, boolean is expected')