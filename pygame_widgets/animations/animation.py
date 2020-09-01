from threading import Thread
import time
import pygame

from pygame_widgets import Button


class AnimationBase:
    def __init__(self, widget, timeout, **kwargs):
        """Base for animations

        :param widget: The widget that the animation targets
        :param time: The time of the animation in seconds
        :param kwargs:
        """
        self.widget = widget
        self.timeout = timeout
        self.params = kwargs
        self.thread = Thread(target=self.loop)

    def start(self):
        self.thread.start()

    def loop(self):
        start = time.time()

        initialParams = {}
        for param, target in self.params.items():
            initialParams[param] = self.widget.get(param)

        # Animate
        while time.time() - start < self.timeout:
            step = (time.time() - start) / self.timeout
            for param, target in self.params.items():
                newValue = initialParams[param] + step * (target - initialParams[param])
                self.widget.set(param, newValue)

        # Ensure value is exactly correct at end
        for param, target in self.params.items():
            self.widget.set(param, target)


class Translate(AnimationBase):
    def __init__(self, widget, timeout, x, y):
        super().__init__(widget, timeout, x=x, y=y)


class Resize(AnimationBase):
    def __init__(self, widget, timeout, width, height):
        super().__init__(widget, timeout, width=width, height=height)


if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode((600, 600))

    button = Button(win, 100, 100, 300, 150)

    animation = Resize(button, 3, 200, 200)
    animation.start()

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill((255, 255, 255))

        button.listen(events)
        button.draw()

        pygame.display.update()
