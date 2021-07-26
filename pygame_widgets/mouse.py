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
    _refreshTime = 0.01

    # Redundant currently, may use for double click handling
    lastLeftClick = 0
    lastRightClick = 0
    leftClickElapsedTime = 0
    rightClickElapsedTime = 0

    _mouseState = MouseState.HOVER

    @staticmethod
    def listen():
        listening = True
        while listening:
            try:
                Mouse.updateMouseState()
            except pygame.error:
                listening = False
            time.sleep(Mouse._refreshTime)

    @staticmethod
    def updateMouseState():
        leftPressed = pygame.mouse.get_pressed()[0]
        rightPressed = pygame.mouse.get_pressed()[2]

        if leftPressed:
            if Mouse._mouseState == MouseState.CLICK or Mouse._mouseState == MouseState.DRAG:
                Mouse._mouseState = MouseState.DRAG
            else:
                Mouse._mouseState = MouseState.CLICK

        elif rightPressed:
            if Mouse._mouseState == MouseState.RIGHT_CLICK or Mouse._mouseState == MouseState.RIGHT_DRAG:
                Mouse._mouseState = MouseState.RIGHT_DRAG
            else:
                Mouse._mouseState = MouseState.RIGHT_CLICK
        else:
            # If previously was held down, call the release
            if Mouse._mouseState == MouseState.CLICK or Mouse._mouseState == MouseState.DRAG:
                Mouse._mouseState = MouseState.RELEASE

            elif Mouse._mouseState == MouseState.RIGHT_CLICK or Mouse._mouseState == MouseState.RIGHT_DRAG:
                Mouse._mouseState = MouseState.RIGHT_RELEASE

            else:
                Mouse._mouseState = MouseState.HOVER

    @staticmethod
    def updateElapsedTime():
        """Also redundant until double click functionality implemented"""
        if Mouse._mouseState == MouseState.CLICK or Mouse._mouseState == MouseState.DRAG:
            Mouse.leftClickElapsedTime = time.time() - Mouse.lastLeftClick
        elif Mouse._mouseState == MouseState.RIGHT_CLICK or Mouse._mouseState == MouseState.RIGHT_DRAG:
            Mouse.rightClickElapsedTime = time.time() - Mouse.lastRightClick

    @staticmethod
    def getMouseState() -> MouseState:
        return Mouse._mouseState

    @staticmethod
    def getMousePos() -> (int, int):
        return pygame.mouse.get_pos()

    @staticmethod
    def setRefreshRatePerSec(refreshRate):
        Mouse._refreshTime = 1 / refreshRate if refreshRate != 0 else 0


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
