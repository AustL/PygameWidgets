# Style Guide for Pygame Widgets

If you want to contribute to this project, it would be greatly appreciated
if you keep to the following code style guide as much as possible.

_Note: If ever in doubt, check the existing code._

## Naming
* Variables, functions and keyword arguments should be in lowerCamelCase ***NOT*** lower_snake_case
* Classes should be UpperCamelCase
* Constants should be UPPERCASE_WITH_UNDERSCORES
* Names should be concise but also descriptive
* The names of properties and methods should be consistent across all widgets
* Where possible, Australian English should be used
  * E.g. _colour_ instead of _color_
  * _Note: This is to ensure consistency across the project for users and does not matter as much for comments_

## Whitespace
* Two lines before and after class and function declarations
* A single line between separate blocks of logic
  * E.g. Between an _if_ and _elif_ statement
* A single space between operators
  * E.g. _n = (x + y) / 3 == (z ** 2)_
  * _Note: The only exception is if - is used for negatives_
* A single space after commas, not before
  * E.g. _[1, 2, 3, 4]_
* No space when setting keyword arguments
  * E.g. _function(param, x=1, y=2)_

## Other
* **SINGLE** quotes for 'strings'
* Double quotes for """docstrings""" only
* Extracting keyword arguments should be done with _kwargs.get('key', default)_
* Only use built-in exceptions if logical, otherwise create a custom exception in [exceptions.py](../pygame_widgets/exceptions/exceptions.py)

## Documentation
* Docstrings should include a short description of the function or class followed by parameter descriptions and types
* Single line comments should be placed whenever complex logic is used
* If unclear, type hints should be used to clarify functions