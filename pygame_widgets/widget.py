from abc import abstractmethod, ABC


class WidgetBase(ABC):
    def __init__(self, win, x, y, width, height):
        """ Base for all widgets

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
        """
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

    def get(self, attr):
        """Default setter for any attributes. Call super if overriding

        :param attr: Attribute to get
        :return: Value of the attribute
        """
        if attr == 'x':
            return self.x

        if attr == 'y':
            return self.y

        if attr == 'width':
            return self.width

        if attr == 'height':
            return self.height

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def set(self, attr, value):
        """Default setter for any attributes. Call super if overriding

        :param attr: Attribute to set
        :param value: Value to set
        """
        if attr == 'x':
            self.x = value

        if attr == 'y':
            self.y = value

        if attr == 'width':
            self.width = value

        if attr == 'height':
            self.height = value

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setWidth(self, width):
        self.width = width

    def setHeight(self, height):
        self.height = height
