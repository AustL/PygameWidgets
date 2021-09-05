import pygame_widgets
from pygame_widgets import Mouse
from pygame_widgets.widget import WidgetBase
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown, DropdownChoice


class ComboBox(Dropdown):
    def __init__(
            self, win, x, y, width, height,
            choices,
            textboxKwargs=None,
            **kwargs
    ):
        """Initialise a customisable combo box for Pygame. Acts like a searchable dropdown.

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
        :param textboxKwargs: Kwargs to be passed to the search box
        :type textboxKwargs: dict(str: Any)
        :param maxResults: The maximum number of results to display
        :type maxResults: int
        :param kwargs: Optional parameters
        """
        WidgetBase.__init__(self, win, x, y, width, height)

        if textboxKwargs is None:
            textboxKwargs = {}
        self._dropped = False

        self.choices = choices
        self.suggestions = choices  # Stores the current suggestions

        self._searchAlgo = kwargs.get('searchAlgo', self._defaultSearch)

        # Adds params that are not specified in text box
        for key, value in kwargs.items():
            if key not in textboxKwargs:
                textboxKwargs[key] = value

        self.textBar = TextBox(
            win, x, y, width, height, isSubWidget=True,
            onTextChanged=self.updateSearchResults,
            **textboxKwargs
        )
        self.__main = self.textBar
        # Set the number of choices if not given
        self.maxResults = kwargs.get('maxResults', len(choices))

        self.createDropdownChoices(x, y, width, height, **kwargs)

        self.getText = self.textBar.getText

        # Function
        self.onSelected = kwargs.get('onSelected', lambda *args: None)
        self.onSelectedParams = kwargs.get('onSelectedParams', ())
        self.onStartSearch = kwargs.get('onStartSearch', lambda *args: None)
        self.onStartSearchParams = kwargs.get('onStartSearchParams', ())
        self.onStopSearch = kwargs.get('onStopSearch', lambda *args: None)
        self.onStopSearchParams = kwargs.get('onStopSearchParams', ())

    def createDropdownChoices(self, x, y, width, height, **kwargs):
        """Create the widgets for the choices."""
        # We create the DropdownChoice(s)
        direction = kwargs.get('direction', 'down')
        self.__choices = []
        for i, text in enumerate(self.choices):
            if i == self.maxResults:
                return

            if direction == 'down':
                x = 0
                y = (i + 1) * height

            elif direction == 'up':
                x = 0
                y = -(i + 1) * height

            elif direction == 'right':
                x = (i + 1) * width
                y = 0

            elif direction == 'left':
                x = -(i + 1) * width
                y = 0

            self.__choices.append(
                DropdownChoice(
                    self.win, x, y, width, height,
                    text=text, dropdown=self, value=i,
                    last=(i == self.maxResults - 1),
                    **kwargs,
                )
            )

    def listen(self, events):
        """Wait for input.

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if not self._hidden and not self._disabled:
            # Keeps state of selected
            previouslySelected = self.textBar.selected
            self.textBar.listen(events)

            if self._dropped:
                for dropdownChoice in self.__choices:
                    dropdownChoice.listen(events)
                    if dropdownChoice.clicked:
                        # The choice was clicked by user
                        self.textBar.setText(dropdownChoice.text)
                        self.onSelected(*self.onSelectedParams)

            # Whether the search is started or stopped
            if previouslySelected and not self.textBar.selected:
                self.onStopSearch(*self.onStopSearchParams)
                self._dropped = False

            if not previouslySelected and self.textBar.selected:
                self.onStartSearch(*self.onStartSearchParams)
                self.updateSearchResults()

    def draw(self):
        """Draw the widget."""
        if not self._hidden:
            self.textBar.draw()
            if self._dropped:
                # Find how many choices should be shown
                numberVisible = min(len(self.suggestions), self.maxResults)
                for i, dropdownChoice in enumerate(self.__choices):
                    # Define if the the dropdown should be shown
                    if i < numberVisible:
                        dropdownChoice.show()
                        self.moveToTop()
                        # Choose the text to show
                        dropdownChoice.text = self.suggestions[i]
                    else:
                        dropdownChoice.hide()
                    dropdownChoice.draw()

    def contains(self, x, y):
        return super(Dropdown, self).contains(x, y) or \
               (any([c.contains(x, y) for c in self.__choices]) and self._dropped)

    def updateSearchResults(self):
        """Update the suggested results based on selected text.

        Uses a 'contains' research. Could be improved by other
        search algorithms.
        """
        text = self.textBar.getText()

        if text != '':
            # Finds all the texts that start with the same text
            self.suggestions = self._searchAlgo(text, self.choices)
            self._dropped = True
        else:
            self._dropped = False

    def _searchAlgo(self, text, choices):
        """Return the suggestions of text in choices."""
        raise NotImplementedError('A search method must override this.')

    @staticmethod
    def _defaultSearch(text, choices):
        """Return the suggestions of text in choices."""

        # First add the ones that perfectly match case
        suggestions = [
            choice for choice in choices
            if choice.startswith(text)
        ]
        # Then add the ones that include text
        suggestions += [
            choice for choice in choices
            if text in choice and choice not in suggestions
        ]
        return suggestions


if __name__ == '__main__':
    import pygame
    from pygame_widgets.button import Button

    pygame.init()
    win = pygame.display.set_mode((600, 600))

    comboBox = ComboBox(
        win, 120, 10, 250, 50, name='Select Colour',
        choices=pygame.colordict.THECOLORS.keys(),
        maxResults=4,
        font=pygame.font.SysFont('calibri', 30),
        borderRadius=3, colour=(0, 200, 50), direction='down',
        textHAlign='left'
    )


    def output():
        comboBox.textBar.colour = comboBox.getText()


    button = Button(
        win, 10, 10, 100, 50, text='Set Colour', fontSize=30,
        margin=15, inactiveColour=(200, 0, 100), pressedColour=(0, 255, 0),
        radius=5, onClick=output, font=pygame.font.SysFont('calibri', 18),
        textVAlign='bottom'
    )

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
