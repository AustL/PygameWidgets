import weakref

from collections.abc import MutableSet
from collections import OrderedDict

from abc import abstractmethod, ABC

from pygame.event import Event

from pygame_widgets.mouse import Mouse


# Implementation of an insertion-ordered set. Necessary to keep track of the order in which widgets are added.
class OrderedSet(MutableSet):
    def __init__(self, values=()):
        self._od = OrderedDict().fromkeys(values)

    def __len__(self):
        return len(self._od)

    def __iter__(self):
        return iter(self._od)

    def __contains__(self, value):
        return value in self._od

    def add(self, value):
        self._od[value] = None

    def discard(self, value):
        self._od.pop(value, None)

    def move_to_end(self, value):
        self._od.move_to_end(value)

    def move_to_start(self, value):
        self._od.move_to_end(value, last=False)



class OrderedWeakset(weakref.WeakSet):
    _remove = ...  # Getting defined after the super().__init__() call

    def __init__(self, values=()):
        super(OrderedWeakset, self).__init__()

        self.data = OrderedSet()
        for elem in values:
            self.add(elem)

    def move_to_end(self, item):
        self.data.move_to_end(weakref.ref(item, self._remove))

    def move_to_start(self, item):
        self.data.move_to_start(weakref.ref(item, self._remove))



class WidgetBase(ABC):
    def __init__(self, win, x, y, width, height, isSubWidget=False):
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
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._isSubWidget = isSubWidget

        self._hidden = False
        self._disabled = False

        if not isSubWidget:
            WidgetHandler.addWidget(self)

    @abstractmethod
    def listen(self, events):
        pass

    @abstractmethod
    def draw(self):
        pass

    def __repr__(self):
        return f'{type(self).__name__}(x = {self._x}, y = {self._y}, width = {self._width}, height = {self._height})'

    def contains(self, x, y):
        return (self._x < x - self.win.get_abs_offset()[0] < self._x + self._width) and \
               (self._y < y - self.win.get_abs_offset()[1] < self._y + self._height)

    def hide(self):
        self._hidden = True
        if not self._isSubWidget:
            WidgetHandler.moveToBottom(self)

    def show(self):
        self._hidden = False
        if not self._isSubWidget:
            WidgetHandler.moveToTop(self)

    def disable(self):
        self._disabled = True

    def enable(self):
        self._disabled = False

    def isSubWidget(self):
        return self._isSubWidget

    def moveToTop(self):
        WidgetHandler.moveToTop(self)

    def moveToBottom(self):
        WidgetHandler.moveToBottom(self)

    def moveX(self, x):
        self._x += x

    def moveY(self, y):
        self._y += y

    def get(self, attr):
        """Default setter for any attributes. Call super if overriding

        :param attr: Attribute to get
        :return: Value of the attribute
        """
        if attr == 'x':
            return self._x

        if attr == 'y':
            return self._y

        if attr == 'width':
            return self._width

        if attr == 'height':
            return self._height

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def isVisible(self):
        return not self._hidden

    def isEnabled(self):
        return not self._disabled

    def set(self, attr, value):
        """Default setter for any attributes. Call super if overriding

        :param attr: Attribute to set
        :param value: Value to set
        """
        if attr == 'x':
            self._x = value

        if attr == 'y':
            self._y = value

        if attr == 'width':
            self._width = value

        if attr == 'height':
            self._height = value

    def setX(self, x):
        self._x = x

    def setY(self, y):
        self._y = y

    def setWidth(self, width):
        self._width = width

    def setHeight(self, height):
        self._height = height

    def setIsSubWidget(self, isSubWidget):
        self._isSubWidget = isSubWidget
        if isSubWidget:
            WidgetHandler.removeWidget(self)
        else:
            WidgetHandler.addWidget(self)


class WidgetHandler:
    _widgets: OrderedWeakset[weakref.ref] = OrderedWeakset()

    @staticmethod
    def main(events: [Event]) -> None:
        blocked = False

        # Conversion is used to prevent errors when widgets are added/removed during iteration a.k.a safe iteration
        widgets = list(WidgetHandler._widgets)

        for widget in widgets[::-1]:
            if not blocked or not widget.contains(*Mouse.getMousePos()):
                widget.listen(events)

            # Ensure widgets covered by others are not affected (widgets created later)
            if widget.contains(*Mouse.getMousePos()):  # TODO: Unless 'transparent'
                blocked = True

        for widget in widgets:
            widget.draw()

    @staticmethod
    def addWidget(widget: WidgetBase) -> None:
        if widget not in WidgetHandler._widgets:
            WidgetHandler._widgets.add(widget)
            WidgetHandler.moveToTop(widget)

    @staticmethod
    def removeWidget(widget: WidgetBase) -> None:
        try:
            WidgetHandler._widgets.remove(widget)
        except ValueError:
            print(f'Error: Tried to remove {widget} when {widget} not in WidgetHandler.')

    @staticmethod
    def moveToTop(widget: WidgetBase):
        try:
            WidgetHandler._widgets.move_to_end(widget)
        except KeyError:
            print(f'Error: Tried to move {widget} to top when {widget} not in WidgetHandler.')

    @staticmethod
    def moveToBottom(widget: WidgetBase):
        try:
            WidgetHandler._widgets.move_to_start(widget)
        except KeyError:
            print(f'Error: Tried to move {widget} to bottom when {widget} not in WidgetHandler.')

    @staticmethod
    def getWidgets() -> [WidgetBase]:
        return WidgetHandler._widgets
