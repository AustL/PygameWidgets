import pygame

from pygame_widgets.widget import WidgetBase
from pygame_widgets.util import drawText


class Popup(WidgetBase):
    def __init__(self, win: pygame.Surface, x: int, y: int, width: int, height: int, title: str, text: str, *buttons,
                 **kwargs):
        super().__init__(win, x, y, width, height)
        self.title = title
        self.text = text
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

        # self.hide()

    def alignTitleRect(self):
        return pygame.Rect(self.x + self.margin, self.y + self.margin,
                           self.width - self.margin * 2, self.height // 3 - self.margin * 2)

    def alignTextRect(self):
        return pygame.Rect(self.x + self.margin, self.y + self.height // 3,
                           self.width - self.margin * 2, self.height // 2 - self.margin * 2)

    def listen(self, events):
        if not self.hidden:
            pass

    def draw(self):
        if not self.hidden:
            if pygame.version.vernum[0] < 2:
                rects = [
                    (self.x + self.radius, self.y, self.width - self.radius * 2, self.height),
                    (self.x, self.y + self.radius, self.width, self.height - self.radius * 2)
                ]

                circles = [
                    (self.x + self.radius, self.y + self.radius),
                    (self.x + self.radius, self.y + self.height - self.radius),
                    (self.x + self.width - self.radius, self.y + self.radius),
                    (self.x + self.width - self.radius, self.y + self.height - self.radius)
                ]

                for rect in rects:
                    x, y, width, height = rect
                    pygame.draw.rect(
                        self.win, self.shadowColour, (x + self.shadowDistance, y + self.shadowDistance, width, height)
                    )

                for circle in circles:
                    x, y = circle
                    pygame.draw.circle(
                        self.win, self.shadowColour, (x + self.shadowDistance, y + self.shadowDistance), self.radius
                    )

                for rect in rects:
                    pygame.draw.rect(self.win, self.colour, rect)

                for circle in circles:
                    pygame.draw.circle(self.win, self.colour, circle, self.radius)
            else:
                pygame.draw.rect(
                    self.win, self.shadowColour,
                    (self.x + self.shadowDistance, self.y + self.shadowDistance, self.width, self.height),
                    border_radius=self.radius
                )

                pygame.draw.rect(
                    self.win, self.colour, (self.x, self.y, self.width, self.height),
                    border_radius=self.radius
                )

        # pygame.draw.rect(self.win, (255, 0, 0), self.titleRect)
        # pygame.draw.rect(self.win, (0, 255, 0), self.textRect)

        drawText(win, self.text, self.textColour, self.textRect, self.textFont, 'centre')
        drawText(win, self.title, self.titleColour, self.titleRect, self.titleFont, 'centre')


if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode((600, 600))

    popup = Popup(win, 100, 100, 400, 400, 'Popup',
                  'This is the text in the popup. Would you like to continue? The buttons below can be customised.',
                  radius=20, textSize=20)

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill((255, 255, 255))

        popup.listen(events)
        popup.draw()

        pygame.display.update()
