from enum import Enum
import pygame
import time


class MouseState(Enum):
    HOVER = 0
    CLICK = 1
    RIGHT_CLICK = 2
    DRAG = 3
    RIGHT_DRAG = 4  # Not sure when this is ever used but added anyway for completeness
    RELEASE = 5
    RIGHT_RELEASE = 6


class Mouse:
    # Redundant currently, may use for double click handling
    lastLeftClick = 0
    lastRightClick = 0
    leftClickElapsedTime = 0
    rightClickElapsedTime = 0

    mouseState = MouseState.HOVER

    @staticmethod
    def updateMouseState() -> MouseState:
        leftPressed = pygame.mouse.get_pressed()[0]
        rightPressed = pygame.mouse.get_pressed()[2]

        if leftPressed:
            if Mouse.mouseState == MouseState.CLICK or Mouse.mouseState == MouseState.DRAG:
                Mouse.mouseState = MouseState.DRAG
            else:
                Mouse.mouseState = MouseState.CLICK

        elif rightPressed:
            if Mouse.mouseState == MouseState.RIGHT_CLICK or Mouse.mouseState == MouseState.RIGHT_DRAG:
                Mouse.mouseState = MouseState.RIGHT_DRAG
            else:
                Mouse.mouseState = MouseState.RIGHT_CLICK
        else:
            # If previously was held down, call the release
            if Mouse.mouseState == MouseState.CLICK or Mouse.mouseState == MouseState.DRAG:
                Mouse.mouseState = MouseState.RELEASE

            elif Mouse.mouseState == MouseState.RIGHT_CLICK or Mouse.mouseState == MouseState.RIGHT_DRAG:
                Mouse.mouseState = MouseState.RIGHT_RELEASE

            else:
                Mouse.mouseState = MouseState.HOVER

        return Mouse.mouseState

    @staticmethod
    def updateElapsedTime():
        """Also redundant until double click functionality implemented"""
        if Mouse.mouseState == MouseState.CLICK or Mouse.mouseState == MouseState.DRAG:
            Mouse.leftClickElapsedTime = time.time() - Mouse.lastLeftClick
        elif Mouse.mouseState == MouseState.RIGHT_CLICK or Mouse.mouseState == MouseState.RIGHT_DRAG:
            Mouse.rightClickElapsedTime = time.time() - Mouse.lastRightClick

    @staticmethod
    def getMouseState() -> MouseState:
        return Mouse.mouseState

    @staticmethod
    def getMousePos() -> (int, int):
        return pygame.mouse.get_pos()


if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode((600, 600))

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill((255, 255, 255))

        Mouse.updateMouseState()

        pygame.display.update()
        time.sleep(0.1)
