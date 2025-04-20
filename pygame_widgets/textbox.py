import pygame
import pygame_widgets
import time
import pyperclip

from pygame_widgets.widget import WidgetBase
from typing import Literal
from pygame_widgets.mouse import Mouse, MouseState


class TextBox(WidgetBase):
    # Times in ms
    REPEAT_DELAY = 400
    REPEAT_INTERVAL = 70
    CURSOR_INTERVAL = 400

    def __init__(
            self,
            win: pygame.Surface,
            x: int,
            y: int,
            width: int,
            height: int,
            isSubWidget=False,
            **kwargs
    ) -> None:
        """ A customisable textbox for Pygame

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
        super().__init__(win, x, y, width, height, isSubWidget)
        self.selected = False
        self.showCursor = False
        self.cursorTime = 0
        self.cursorPosition = 0

        self.repeatTime = 0
        self.repeatKey = None
        self.firstRepeat = True
        self.keyDown = False

        self.text = [[]]
        self.highlightedText = [[]]

        # Highlight indexes
        self.highlightStartLine = 0
        self.highlightEndLine = 0
        self.highlightStartInline = 0
        self.highlightEndInline = 0

        self.escape = False

        # Border
        self.borderThickness = kwargs.get('borderThickness', 3)
        self.borderColour = kwargs.get('borderColour', (0, 0, 0))
        self.radius = kwargs.get('radius', 0)

        # Colour
        self.colour = kwargs.get('colour', (220, 220, 220))
        self.cursorColour = kwargs.get('cursorColour', (0, 0, 0))

        # Text
        self.placeholderText = kwargs.get('placeholderText', '')
        self.placeholderTextColour = kwargs.get('placeholderTextColour', (10, 10, 10))
        self.textColour = kwargs.get('textColour', (0, 0, 0))
        self.highlightColour = kwargs.get('highlightColour', (166, 210, 255))
        self.fontSize = kwargs.get('fontSize', 20)
        self.font = kwargs.get('font', pygame.font.SysFont('calibri', self.fontSize))
        self.tabSpaces = kwargs.get('tabSpaces', 4)

        self.textOffsetTop = self.fontSize // 3
        self.textOffsetLeft = self.fontSize // 3
        self.textOffsetRight = self.fontSize // 2
        self.cursorOffsetTop = self._height // 6

        # Index of the currently selected line
        self.selectedLine = 0

        self.firstVisibleLine = 0
        self.maxVisibleLines = (self._height - self.textOffsetTop - self.borderThickness * 2) // self.fontSize

        # Functions
        self.onSubmit = kwargs.get('onSubmit', lambda *args: None)
        self.onSubmitParams = kwargs.get('onSubmitParams', ())
        self.onTextChanged = kwargs.get('onTextChanged', lambda *args: None)
        self.onTextChangedParams = kwargs.get('onTextChangedParams', ())

        self.cursorWidth = kwargs.get('cursorWidth', 2)

        self._actual_width = (
                self._x
                + self._width
                - self.textOffsetRight
                - self.textOffsetLeft
                - self.borderThickness * 2
        )

    def listen(self, events: list[pygame.event.Event]) -> None:
        """ Wait for inputs

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if self._hidden or self._disabled:
            return
        if self.keyDown:
            self.updateRepeatKey()

        # Selection
        mouseState = Mouse.getMouseState()
        x, y = Mouse.getMousePos()

        if mouseState == MouseState.CLICK:
            if self.contains(x, y):
                self.selected = True
                self.showCursor = True
                self.cursorTime = time.time()
                self.updateCursorPosition(x, y)

                self.highlightStartLine = self.selectedLine
                self.highlightStartInline = self.cursorPosition
            else:
                self.selected = False
                self.showCursor = False
                self.cursorTime = time.time()
                self.resetHighlight()

        elif mouseState == MouseState.DRAG and self.contains(x, y):
            self.selected = True
            self.showCursor = True
            self.cursorTime = time.time()
            self.updateCursorPosition(x, y)

            self.highlightEndLine = self.selectedLine
            self.highlightEndInline = self.cursorPosition

        # Keyboard Input
        if self.selected:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    self.showCursor = True
                    self.keyDown = True
                    self.repeatKey = event
                    self.repeatTime = time.time()

                    if event.key == pygame.K_BACKSPACE:
                        self.handleBackspace()

                    elif event.key == pygame.K_DELETE:
                        self.handleDelete()

                    elif event.key == pygame.K_RETURN:
                        if event.mod & pygame.KMOD_SHIFT:
                            if not self.isEmptyText(self.highlightedText):
                                self.eraseHighlightedText()
                                self.shiftLines()
                            newlineText = self.text[self.selectedLine][self.cursorPosition:]
                            del self.text[self.selectedLine][self.cursorPosition:]
                            self.addText('\n' + ''.join(newlineText))
                            self.cursorPosition = 0
                        else:
                            self.onSubmit(*self.onSubmitParams)

                    elif event.key == pygame.K_UP:
                        self.resetHighlight()
                        self.selectedLine = max(0, self.selectedLine - 1)
                        self.cursorPosition = min(self.cursorPosition, len(self.text[self.selectedLine]))
                        while self.selectedLine < self.firstVisibleLine:
                            self.firstVisibleLine -= 1

                    elif event.key == pygame.K_DOWN:
                        self.resetHighlight()
                        self.selectedLine = min(len(self.text) - 1, self.selectedLine + 1)
                        self.cursorPosition = min(self.cursorPosition, len(self.text[self.selectedLine]))
                        while self.selectedLine >= self.firstVisibleLine + self.maxVisibleLines:
                            self.firstVisibleLine += 1

                    elif event.key == pygame.K_RIGHT:
                        self.resetHighlight()
                        self.cursorPosition = min(self.cursorPosition + 1, len(self.text[self.selectedLine]))

                    elif event.key == pygame.K_LEFT:
                        self.resetHighlight()
                        self.cursorPosition = max(self.cursorPosition - 1, 0)

                    elif event.key == pygame.K_HOME:
                        self.resetHighlight()
                        self.cursorPosition = 0

                    elif event.key == pygame.K_END:
                        self.resetHighlight()
                        self.cursorPosition = len(self.text[self.selectedLine])

                    elif event.key == pygame.K_TAB:
                        self.addText(' ' * self.tabSpaces)

                    elif event.key == pygame.K_INSERT:
                        # TODO add logic for insert
                        pass

                    elif event.key == pygame.K_a and event.mod & pygame.KMOD_CTRL:
                        self.highlightStartLine = 0
                        self.highlightEndLine = len(self.text) - 1
                        self.highlightStartInline = 0
                        self.highlightEndInline = len(self.text[-1])

                    elif (
                            event.key == pygame.K_c
                            and event.mod & pygame.KMOD_CTRL
                            and not self.isEmptyText(self.highlightedText)
                    ):
                        pyperclip.copy(self.getHighlightedText())

                    elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                        self.addText(pyperclip.paste())

                    elif (
                            event.key == pygame.K_x
                            and event.mod & pygame.KMOD_CTRL
                            and not self.isEmptyText(self.highlightedText)
                    ):
                        pyperclip.copy(self.getHighlightedText())
                        self.eraseHighlightedText()
                        self.shiftLines()
                        self.onTextChanged(*self.onTextChangedParams)

                    elif event.key == pygame.K_ESCAPE:
                        if not self.escape:
                            self.selected = False
                            self.showCursor = False
                            self.escape = True
                            self.repeatKey = None
                            self.keyDown = None
                            self.firstRepeat = True
                            self.resetHighlight()

                    self.addText(event.unicode)

                elif event.type == pygame.KEYUP:
                    self.repeatKey = None
                    self.keyDown = None
                    self.firstRepeat = True
                    self.escape = False

                elif event.type == pygame.MOUSEWHEEL:
                    self.scroll(event.y)

    def draw(self) -> None:
        """Display to surface"""
        if not self._hidden:
            if self.selected:
                self.updateCursor()
            self.drawBorder()
            self.drawBackground()
            self.drawHighlight()
            self.drawText()
            self.drawCursor()

    def handleBackspace(self) -> None:
        if not self.isEmptyText(self.highlightedText):
            self.eraseHighlightedText()
            self.cursorPosition += 1

        elif self.cursorPosition != 0:
            self.text[self.selectedLine].pop(self.cursorPosition - 1)

        elif self.cursorPosition == 0 and self.selectedLine == 0:
            if len(self.text[self.selectedLine]) - self.getCountSpecChars(self.selectedLine) == 0 and self.selectedLine + 1 < len(self.text) and self.text[self.selectedLine + 1]:
                self.text.pop(self.selectedLine)

            self.cursorPosition = len(self.text[self.selectedLine]) + 1

        elif self.cursorPosition == 0 and self.selectedLine != 0:
            if len(self.text[self.selectedLine]) - self.getCountSpecChars(self.selectedLine) == 0:
                self.text.pop(self.selectedLine)

            self.selectedLine = max(0, self.selectedLine - 1)
            self.cursorPosition = len(self.text[self.selectedLine])
            if self.text[self.selectedLine][-1] == '\n':
                self.text[self.selectedLine].pop(self.cursorPosition - 1)  # delete the \n
            else:
                self.text[self.selectedLine].pop(self.cursorPosition - 1)

        self.cursorPosition = max(self.cursorPosition - 1, 0)
        while self.selectedLine < self.firstVisibleLine:
            self.firstVisibleLine -= 1

        self.shiftLines()
        self.onTextChanged(*self.onTextChangedParams)

    def handleDelete(self) -> None:
        if not self.isEmptyText(self.highlightedText):
            self.eraseHighlightedText()

        elif self.cursorPosition < len(self.text[self.selectedLine]) - self.getCountSpecChars(self.selectedLine):
            self.text[self.selectedLine].pop(self.cursorPosition)

        elif self.cursorPosition == 0:
            if len(self.text[self.selectedLine]) - self.getCountSpecChars(self.selectedLine) == 0 and self.selectedLine + 1 < len(self.text) and self.text[self.selectedLine + 1]:
                self.text.pop(self.selectedLine)
                self.cursorPosition = 0

        elif self.cursorPosition == len(self.text[self.selectedLine]) - self.getCountSpecChars(self.selectedLine):
            try:
                if self.text[self.selectedLine + 1]:
                    if self.text[self.selectedLine][-1] == '\n':
                        self.text[self.selectedLine].pop()  # delete the \n
                    else:
                        self.text[self.selectedLine + 1].pop(0)
                else:
                    self.text.pop(self.selectedLine + 1)
            except IndexError:
                pass

        while self.selectedLine < self.firstVisibleLine:
            self.firstVisibleLine -= 1

        self.shiftLines()
        self.onTextChanged(*self.onTextChangedParams)

    def updateCursor(self) -> None:
        now = time.time()

        if now - self.cursorTime >= self.CURSOR_INTERVAL / 1000:
            self.showCursor = not self.showCursor
            self.cursorTime = now

    def drawBorder(self) -> None:
        borderRects = [
            (
                self._x + self.radius,
                self._y,
                self._width - self.radius * 2,
                self._height,
            ),
            (
                self._x,
                self._y + self.radius,
                self._width,
                self._height - self.radius * 2,
            ),
        ]

        borderCircles = [
            (self._x + self.radius, self._y + self.radius),
            (self._x + self.radius, self._y + self._height - self.radius),
            (self._x + self._width - self.radius, self._y + self.radius),
            (self._x + self._width - self.radius, self._y + self._height - self.radius),
        ]

        for rect in borderRects:
            pygame.draw.rect(self.win, self.borderColour, rect)

        for circle in borderCircles:
            pygame.draw.circle(self.win, self.borderColour, circle, self.radius)

    def drawBackground(self) -> None:
        backgroundRects = [
            (
                self._x + self.borderThickness + self.radius,
                self._y + self.borderThickness,
                self._width - 2 * (self.borderThickness + self.radius),
                self._height - 2 * self.borderThickness,
            ),
            (
                self._x + self.borderThickness,
                self._y + self.borderThickness + self.radius,
                self._width - 2 * self.borderThickness,
                self._height - 2 * (self.borderThickness + self.radius),
            ),
        ]

        backgroundCircles = [
            (
                self._x + self.radius + self.borderThickness,
                self._y + self.radius + self.borderThickness,
            ),
            (
                self._x + self.radius + self.borderThickness,
                self._y + self._height - self.radius - self.borderThickness,
            ),
            (
                self._x + self._width - self.radius - self.borderThickness,
                self._y + self.radius + self.borderThickness,
            ),
            (
                self._x + self._width - self.radius - self.borderThickness,
                self._y + self._height - self.radius - self.borderThickness,
            ),
        ]

        for rect in backgroundRects:
            pygame.draw.rect(self.win, self.colour, rect)

        for circle in backgroundCircles:
            pygame.draw.circle(self.win, self.colour, circle, self.radius)

    def drawText(self) -> None:
        if not self.isEmptyText(self.text):
            text = self.text[self.firstVisibleLine: self.firstVisibleLine + self.maxVisibleLines]
            colour = self.textColour
        else:
            text = [list(self.placeholderText)]
            colour = self.placeholderTextColour

        for lineIndex, line in enumerate(text):
            x = [self._x + self.textOffsetLeft]
            for char in line:
                if self.isSpecialChar(char):
                    continue
                charRender = self.font.render(
                    char,
                    True,
                    colour,
                )
                textRect = charRender.get_rect(
                    bottomleft=(
                        x[-1],
                        self._y + self.fontSize * (lineIndex + 1) + self.textOffsetTop,
                    )
                )

                self.win.blit(charRender, textRect)
                x.append(x[-1] + charRender.get_width())

    def drawCursor(self) -> None:
        if (
                self.selectedLine - self.firstVisibleLine >= self.maxVisibleLines
                or self.selectedLine < self.firstVisibleLine
        ):
            self.showCursor = False

        if self.showCursor:
            try:
                lineWidth = self.getLineWidth(self.selectedLine)
                pygame.draw.line(
                    self.win,
                    self.cursorColour,
                    (
                        lineWidth[self.cursorPosition],
                        self._y
                        + self.textOffsetTop
                        + self.fontSize * (self.selectedLine - self.firstVisibleLine),
                    ),
                    (
                        lineWidth[self.cursorPosition],
                        self._y
                        + self.fontSize * (self.selectedLine - self.firstVisibleLine + 1)
                        + self.textOffsetTop,
                    ),
                    width=self.cursorWidth,
                )
            except IndexError:
                self.cursorPosition -= 1

    def drawHighlight(self) -> None:
        def drawRect(line: int, start: int, end: int) -> None:
            shift = 0
            lineWidth = self.getLineWidth(line)
            for charIndex in range(start, end):
                char = self.text[line][charIndex]
                if self.isSpecialChar(char):
                    char = ' '
                    shift += 1
                charRender = self.font.render(char, True, self.highlightColour)
                rect = charRender.get_rect(
                    bottomleft=(
                        lineWidth[charIndex - shift],
                        self._y
                        + self.fontSize * (line - self.firstVisibleLine + 1)
                        + self.textOffsetTop,
                    )
                )
                pygame.draw.rect(self.win, self.highlightColour, rect)

        startLine = min(self.highlightStartLine, self.highlightEndLine)
        endLine = max(self.highlightStartLine, self.highlightEndLine)

        startInline = self.highlightStartInline
        endInline = self.highlightEndInline

        if self.highlightStartLine > self.highlightEndLine:
            startInline = self.highlightEndInline
            endInline = self.highlightStartInline

        if startLine == endLine:
            startInline = min(self.highlightStartInline, self.highlightEndInline)
            endInline = max(self.highlightStartInline, self.highlightEndInline)

            drawRect(startLine, startInline, endInline)
            self.highlightedText = [self.text[startLine][startInline:endInline]]

        else:
            if self.firstVisibleLine <= startLine < self.firstVisibleLine + self.maxVisibleLines:
                drawRect(startLine, startInline, len(self.text[startLine]))
            self.highlightedText = [self.text[startLine][startInline:]]

            for lineIndex in range(startLine + 1, endLine):
                if self.firstVisibleLine <= lineIndex < self.firstVisibleLine + self.maxVisibleLines:
                    drawRect(lineIndex, 0, len(self.text[lineIndex]))
                self.highlightedText += [self.text[lineIndex]]

            if self.firstVisibleLine <= endLine < self.firstVisibleLine + self.maxVisibleLines:
                drawRect(endLine, 0, endInline)
            self.highlightedText += [self.text[endLine][:endInline]]

    def updateRepeatKey(self):
        now = time.time()

        if self.firstRepeat:
            if now - self.repeatTime >= self.REPEAT_DELAY / 1000:
                self.firstRepeat = False
                self.repeatTime = now
                pygame.event.post(
                    pygame.event.Event(
                        pygame.KEYDOWN,
                        {
                            'key': self.repeatKey.key,
                            'unicode': self.repeatKey.unicode,
                            'mod': self.repeatKey.mod,
                        },
                    )
                )

        elif now - self.repeatTime >= self.REPEAT_INTERVAL / 1000:
            self.repeatTime = now
            pygame.event.post(
                pygame.event.Event(
                    pygame.KEYDOWN,
                    {
                        'key': self.repeatKey.key,
                        'unicode': self.repeatKey.unicode,
                        'mod': self.repeatKey.mod,
                    },
                )
            )

    def scroll(self, direction: Literal[1, -1]):
        if len(self.text) > self.maxVisibleLines:
            self.firstVisibleLine -= direction

            self.firstVisibleLine = max(0, self.firstVisibleLine)
            self.firstVisibleLine = min(len(self.text) - 1, self.firstVisibleLine)

    @staticmethod
    def isSpecialChar(char: str) -> bool:
        return ord(char) < 32 or ord(char) == 127

    @staticmethod
    def isEmptyText(text: list[list[str]]) -> bool:
        return all(len(line) == 0 for line in text)

    def eraseHighlightedText(self) -> None:
        startLine, endLine = sorted((self.highlightStartLine, self.highlightEndLine))
        startInline, endInline = sorted(
            (self.highlightStartInline, self.highlightEndInline)) if startLine == endLine else \
            (self.highlightStartInline, self.highlightEndInline) if self.highlightStartLine < self.highlightEndLine else \
            (self.highlightEndInline, self.highlightStartInline)

        if startLine == endLine:
            del self.text[startLine][startInline:endInline]
            if not self.text[startLine]:
                self.text.pop(startLine)
        else:
            del self.text[startLine][startInline:]
            del self.text[endLine][:endInline]
            del self.text[startLine + 1:endLine]

            if startLine < len(self.text) and not self.text[startLine]:
                self.text.pop(startLine)

            if endLine < len(self.text) and not self.text[endLine]:
                self.text.pop(endLine)

            for i in range(startLine, endLine):
                if i < len(self.text) and not self.text[i]:
                    self.text.pop(i)

        if not self.text:
            self.text = [[]]

        self.selectedLine = min(startLine, len(self.text) - 1)
        self.cursorPosition = startInline
        self.resetHighlight()

    def resetHighlight(self) -> None:
        self.highlightStartLine = self.highlightEndLine = 0
        self.highlightStartInline = self.highlightEndInline = 0
        self.highlightedText = [[]]

    def updateCursorPosition(self, x: float, y: float) -> None:
        lineY = self._y + self.borderThickness + self.textOffsetTop
        for lineIndex in range(len(self.text)):
            if lineY <= y < lineY + self.fontSize:
                self.selectedLine = lineIndex + self.firstVisibleLine
                break
            lineY += self.fontSize

        self.selectedLine = min(self.selectedLine, len(self.text) - 1)
        self.selectedLine = max(self.selectedLine, self.firstVisibleLine)

        lineWidth = self.getLineWidth(self.selectedLine)
        countSpecChars = self.getCountSpecChars(self.selectedLine)
        textLength = len(self.text[self.selectedLine]) - countSpecChars

        for charIndex in range(textLength):
            midX = (lineWidth[charIndex] + lineWidth[charIndex + 1]) / 2
            if midX >= x:
                self.cursorPosition = charIndex
                break
        else:
            self.cursorPosition = textLength

        if x <= lineWidth[0] / 2:
            self.cursorPosition = 0

    def addText(self, text: str) -> None:
        """
        Add text to the text box

        This method will insert the given text into the text box at the current cursor position.
        The text will be split into individual characters and inserted one by one.
        If a line is too long, the characters will be split onto the next line.
        If the cursor is at the end of the text box, a new line will be added.

        Args:
            text (str): The text to add to the text box
        """
        text = list(text.replace('\t', ' ' * self.tabSpaces))

        for char in text:
            if not char or self.isSpecialChar(char) and char != '\n':
                continue

            if not self.isEmptyText(self.highlightedText):
                self.eraseHighlightedText()
                self.shiftLines()

            if char == '\n':
                self.text[self.selectedLine].append('\n')
                self.text.insert(self.selectedLine + 1, [])
                self.selectedLine += 1
                self.cursorPosition = 0
            else:
                try:
                    self.text[self.selectedLine].insert(self.cursorPosition, char)
                except IndexError:
                    self.text.append([char])

            for lineIndex in range(self.selectedLine, len(self.text)):
                lineWidth = self.getLineWidth(lineIndex)

                for charIndex in range(len(self.text[lineIndex]) - self.getCountSpecChars(lineIndex)):
                    if lineWidth[charIndex] >= self._actual_width:
                        try:
                            self.text[lineIndex + 1].insert(0, self.text[lineIndex].pop())
                        except IndexError:
                            self.text.insert(lineIndex + 1, [self.text[lineIndex].pop()])

                        if self.cursorPosition >= len(self.text[lineIndex]):
                            self.selectedLine += 1
                            self.cursorPosition = 0

            self.cursorPosition += 1

        self.onTextChanged(*self.onTextChangedParams)
        self.firstVisibleLine = max(self.firstVisibleLine, len(self.text) - self.maxVisibleLines)
        while self.selectedLine < self.firstVisibleLine:
            self.firstVisibleLine -= 1

    def getLineWidth(self, line: int) -> list[float]:
        """
        Get the width of a line of text in the text box

        This method will return a list of the x-coordinates of the end of each character in the line.
        The x-coordinate is relative to the left edge of the text box.

        Args:
            line (int): The number of the line of text to get the width of

        Returns:
            list[float]: A list of the x-coordinates of the end of each character in the line
        """
        x = [self._x + self.textOffsetLeft]
        for char in self.text[line]:
            if self.isSpecialChar(char):
                continue
            charRender = self.font.render(char, True, self.textColour)
            x.append(x[-1] + charRender.get_width())
        return x

    def shiftLines(self) -> None:
        shift = 0

        for lineIndex in range(self.selectedLine, len(self.text) - 1):
            current_line = lineIndex - shift
            if not self.text[current_line] or self.text[current_line][-1] == '\n':
                continue

            while True:
                lineWidth = self.getLineWidth(current_line)
                if lineWidth[-1] >= self._actual_width:
                    break

                if not self.text[current_line + 1]:
                    break

                self.text[current_line].append(self.text[current_line + 1].pop(0))

                if not self.text[current_line + 1]:
                    self.text.pop(current_line + 1)
                    shift += 1
                    break

    def getCountSpecChars(self, line: int) -> int:
        return len([char for char in self.text[line] if self.isSpecialChar(char)])

    def setText(self, text: str) -> None:
        self.text = [[]]
        self.selectedLine = 0
        self.cursorPosition = 0
        self.addText(text)

    def getHighlightedText(self) -> str:
        return ''.join(''.join(line) for line in self.highlightedText)

    def getText(self) -> str:
        return ''.join(''.join(line) for line in self.text)


if __name__ == '__main__':

    def output():
        print(textbox.getText())
        print(len(textbox.getText()))
        textbox.setText('')


    pygame.init()
    window = pygame.display.set_mode((1000, 600))

    textbox = TextBox(
        window,
        100,
        100,
        800,
        400,
        fontSize=75,
        borderColour=(255, 0, 0),
        textColour=(0, 200, 0),
        onSubmit=output,
        radius=10,
        borderThickness=5,
        placeholderText='Enter something:',
    )

    run = True
    while run:
        outerEvents = pygame.event.get()
        for outerEvent in outerEvents:
            if outerEvent.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        window.fill((255, 255, 255))
        pygame_widgets.update(outerEvents)
        pygame.display.update()
