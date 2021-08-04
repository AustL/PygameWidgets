from threading import Thread
import time
import pygame

import pygame_widgets
from pygame_widgets.exceptions import InvalidParameter, InvalidParameterType


class AnimationBase:
    def __init__(self, widget, timeout, allowMultiple=False, **kwargs):
        """Base for animations

        :param widget: The widget that the animation targets
        :param timeout: The time of the animation in seconds
        :param kwargs: The target of the animation, e.g. x=10 changes x position to 10
        """
        self.widget = widget
        self.timeout = timeout
        self.allowMultiple = allowMultiple
        self.params = kwargs
        self.thread = Thread()

        self.started = False
        self.runOnce = False

        self.checkValidParams()

    def checkValidParams(self):
        for param, target in self.params.items():
            value = self.widget.get(param)
            if value is None:
                raise InvalidParameter(
                    f'The parameter <{param}> is not a valid attribute of type {type(self.widget)}'
                )
            elif type(value) != type(target):
                raise InvalidParameterType(
                    f'Expected parameter <{param}> to be of type {type(value)} but found type {type(target)}'
                )

    def start(self):
        if not self.started and not (self.runOnce and not self.allowMultiple):
            self.thread = Thread(target=self.loop)
            self.thread.start()

    def loop(self):
        self.started = self.runOnce = True

        start = time.time()

        initialNumberParams = {}
        initialTupleParams = {}
        for param, target in self.params.items():
            initialValue = self.widget.get(param)
            if isinstance(initialValue, (int, float)):
                initialNumberParams[param] = initialValue
            elif isinstance(initialValue, (tuple, list)):
                initialTupleParams[param] = tuple(initialValue)

        # Animate
        while time.time() - start < self.timeout:
            step = (time.time() - start) / self.timeout

            # Numeric animation
            for param, initialValue in initialNumberParams.items():
                target = self.params[param]
                newValue = initialValue + step * (target - initialValue)
                self.widget.set(param, newValue)

            # Tuple animation
            for param, initialTuple in initialTupleParams.items():
                target = self.params[param]
                newValue = tuple(
                    initialTuple[i] + step * (target[i] - initialTuple[i]) for i in range(len(initialTuple)))
                self.widget.set(param, newValue)

        # Ensure value is exactly correct at end
        for param, target in self.params.items():
            self.widget.set(param, target)

        self.started = False


class Translate(AnimationBase):
    def __init__(self, widget, timeout, x, y):
        super().__init__(widget, timeout, x=x, y=y)


class Resize(AnimationBase):
    def __init__(self, widget, timeout, width, height):
        super().__init__(widget, timeout, width=width, height=height)


class Recolour(AnimationBase):
    def __init__(self, widget, timeout, colour):
        super().__init__(widget, timeout, colour=colour)


if __name__ == '__main__':
    from pygame_widgets.button import Button


    def animate():
        resize.start()
        translate.start()


    pygame.init()
    win = pygame.display.set_mode((600, 600))

    button = Button(win, 100, 100, 300, 150, text="Hello", inactiveColour=(0, 200, 0), hoverColour=(0, 200, 0))

    resize = Resize(button, 3, 200, 200)
    translate = Recolour(button, 5, (0, 100, 100))
    button.setOnClick(animate)

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
