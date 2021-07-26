from pygame_widgets.mouse import Mouse
import pygame
import time

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
    print(Mouse.mouseState)

    pygame.display.update()
    time.sleep(0.1)
