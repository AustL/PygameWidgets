from abc import abstractmethod, ABC


class WidgetBase(ABC):
    def __init__(self, win, x, y, width, height):
        self.win = win
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.hidden = False

    @abstractmethod
    def listen(self, events):
        pass

    @abstractmethod
    def draw(self):
        pass

    def contains(self, x, y):
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def moveX(self, x):
        self.x += x

    def moveY(self, y):
        self.y += y
