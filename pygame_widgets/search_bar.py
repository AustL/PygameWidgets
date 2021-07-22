import pygame

from pygame_widgets.widget import WidgetBase


class SearchBar(WidgetBase):
    def __init__(self, win, x, y, width, height, **kwargs):
        """A customisable search bar for Pygame.

        It is possible to write in the bar.

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