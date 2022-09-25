import pygame
import tkinter as tk
from tkinter import messagebox
from enum import Enum

import pygame_widgets
from pygame_widgets.widget import WidgetBase
from pygame_widgets.util import drawText

tk.Tk().wm_withdraw()


class PopupType(Enum):
    INFO = 0
    ERROR = 1
    WARNING = 2
    QUESTION = 3
    OK_CANCEL = 4
    YES_NO = 5
    YES_NO_CANCEL = 6
    RETRY_CANCEL = 7


class TKPopup(WidgetBase):
    def __init__(self, win: pygame.Surface, x: int, y: int, width: int, height: int, popupType: PopupType,
                 title: str, text: str, trigger=lambda *args: None, *buttons, **kwargs):
        super().__init__(win, x, y, width, height)
        self.popupType = popupType
        self.title = title
        self.text = text
        self.trigger = trigger
        self.buttons = buttons

        self.margin = kwargs.get('margin', 20)

        self.titleColour = kwargs.get('titleColour', (0, 0, 0))
        self.titleSize = kwargs.get('titleSize', 40)
        self.titleFont = kwargs.get('titleFont', pygame.font.SysFont('calibri', self.titleSize, True))
        self.titleRect = self.alignTitleRect()

        self.textColour = kwargs.get('textColour', (0, 0, 0))
        self.textSize = kwargs.get('textSize', 18)
        self.textFont = kwargs.get('textFont', pygame.font.SysFont('calibri', self.textSize))
        self.textRect = self.alignTextRect()

        self.radius = kwargs.get('radius', 0)

        self.colour = kwargs.get('colour', (150, 150, 150))
        self.shadowDistance = kwargs.get('shadowDistance', 0)
        self.shadowColour = kwargs.get('shadowColour', (210, 210, 180))

        self.hide()

    def alignTitleRect(self):
        return pygame.Rect(self._x + self.margin, self._y + self.margin,
                           self._width - self.margin * 2, self._height // 3 - self.margin * 2)

    def alignTextRect(self):
        return pygame.Rect(self._x + self.margin, self._y + self._height // 3,
                           self._width - self.margin * 2, self._height // 2 - self.margin * 2)

    def listen(self, events):
        if self.trigger():
            self.show()
            messagebox.showinfo(self.title, self.text)

    def draw(self):
        pass

    def show(self):
        super().show()
        messagebox.showinfo(self.title, self.text)

        # pygame.draw.rect(self.win, (255, 0, 0), self.titleRect)
        # pygame.draw.rect(self.win, (0, 255, 0), self.textRect)

        # drawText(win, self.text, self.textColour, self.textRect, self.textFont, 'centre')
        # drawText(win, self.title, self.titleColour, self.titleRect, self.titleFont, 'centre')


if __name__ == '__main__':
    from pygame_widgets.button import Button

    pygame.init()
    win = pygame.display.set_mode((600, 600))

    popup = Popup(win, 100, 100, 400, 400, PopupType.INFO, 'Popup',
                  'This is the text in the popup. Would you like to continue? The buttons below can be customised.',
                  radius=20, textSize=20)

    button = Button(win, 100, 100, 400, 400, text='Popup', onClick=lambda: popup.show())

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