
from pygame_widgets.widget import WidgetBase
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown, DropdownChoice


class SearchBar(Dropdown):
    def __init__(
        self, win, x, y, width, height,
        choices,
        **kwargs
    ):
        """Initialize a customisable search bar for Pygame.

        The bar can be written on, and displays under it the results.

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
        :param max_results: The maximum number of results to display
        :type max_results: int
        :param kwargs: Optional parameters
        """
        WidgetBase.__init__(self, win, x, y, width, height)
        self._dropped = False

        self.choices = choices
        self.suggestions = choices  # Stores the current suggestions

        self.text_bar = TextBox(
            win, x, y, width, height,
            onTextChanged=self.update_search_results,
            **kwargs
        )
        self.__main = self.text_bar
        # Set the number of choices if not given
        self.max_results = kwargs.get('max_results', len(choices))

        self.create_drop_down_choices(x, y, width, height, **kwargs)

        self.getText = self.text_bar.getText

        # Function
        self.onSelected = kwargs.get('onSelected', lambda *args: None)
        self.onSelectedParams = kwargs.get('onSelectedParams', ())
        self.onStartSearch = kwargs.get('onStartSearch', lambda *args: None)
        self.onStartSearchParams = kwargs.get('onStartSearchParams', ())
        self.onStopSearch = kwargs.get('onStopSearch', lambda *args: None)
        self.onStopSearchParams = kwargs.get('onStopSearchParams', ())

    def create_drop_down_choices(self, x, y, width, height, **kwargs):
        """Create the widgets for the choices."""
        # We create the DropdownChoice(s)
        direction = kwargs.get('direction', 'down')
        self.__choice_widgets = []
        for i, text in enumerate(self.choices):
            if i == self.max_results:
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

            self.__choice_widgets.append(
                DropdownChoice(
                    self.win,
                    x,
                    y,
                    width,
                    height,
                    text=text,
                    drop=self,
                    value=i,
                    last=(i == self.max_results - 1),
                    **kwargs,
                )
            )

    def listen(self, events):
        """Wait for input.

        :param events: Use pygame.event.get()
        :type events: list of pygame.event.Event
        """
        if not self._hidden:
            # Keeps state of selected
            previously_selected = self.text_bar.selected
            self.text_bar.listen(events)
            # Whether the search is started or stopped
            if previously_selected and not self.text_bar.selected:
                self.onStopSearch(*self.onStopSearchParams)
            if not previously_selected and self.text_bar.selected:
                self.onStartSearch(*self.onStartSearchParams)

            for dropdown_choice in self.__choice_widgets:
                previously_clicked = dropdown_choice.clicked
                dropdown_choice.listen(events)
                if previously_clicked and not dropdown_choice.clicked:
                    # The choice was clicked by user
                    self.text_bar.setText(dropdown_choice.text)


    def draw(self):
        """Draw the widget."""
        if not self._hidden:
            self.text_bar.draw()
            if self.dropped:
                # Find how many choices should be shown
                n_to_show = min(len(self.suggestions), self.max_results)
                for i, dropdown_choice in enumerate(self.__choice_widgets):
                    # Define if the the drop down should be shown
                    if i < n_to_show:
                        dropdown_choice.show()
                        # Choose the text to show
                        dropdown_choice.text = self.suggestions[i]
                    else:
                        dropdown_choice.hide()
                    dropdown_choice.draw()

    def update_search_results(self):
        """Update the suggested results based on selected text.

        Uses a 'contains' research. Could be improved by other
        search algorithms.
        """

        text = self.text_bar.getText()

        # Finds all the texts that start with the same text
        self.suggestions = [
            choice for choice in self.choices
            if text in choice
        ]
        self.dropped = True




