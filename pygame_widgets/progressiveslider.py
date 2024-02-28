import pygame
from pygame import gfxdraw

import pygame_widgets
from pygame_widgets.slider import Slider

class ProgressiveSlider(Slider):
    def __init__(self, win,x,y,width,height,**kwargs):
        super().__init__(win,x,y,width,height,**kwargs)
        self.progress = 0
        self.progressColour = kwargs.get('progressColour',(0,35,255))


    def draw(self):
        if not self._hidden:
            pygame.draw.rect(self.win, self.colour, (self._x, self._y, self._width, self._height))

            if self.vertical:
                if self.curved:
                    pygame.draw.circle(self.win, self.colour, (self._x + self._width // 2, self._y), self.radius)
                    pygame.draw.circle(self.win, self.colour, (self._x + self._width // 2, self._y + self._height),
                                       self.radius)
                circle = (self._x + self._width // 2,
                          int(self._y + (self.max - self.value) / (self.max - self.min) * self._height))
                
                pygame.draw.circle(self.win, self.progressColour, (self._x + self._width // 2, self._y + self._height),
                                   self.radius)
                pygame.draw.rect(self.win, self.progressColour,
                                (self._x, self._y + int(self._height * (1 - self.value/self.max)), self._width, int(self._height * self.value/self.max)))
            else:
                if self.curved:
                    pygame.draw.circle(self.win, self.colour, (self._x, self._y + self._height // 2), self.radius)
                    pygame.draw.circle(self.win, self.colour, (self._x + self._width, self._y + self._height // 2),
                                       self.radius)
                circle = (int(self._x + (self.value - self.min) / (self.max - self.min) * self._width),
                          self._y + self._height // 2)
                
                pygame.draw.circle(self.win, self.progressColour, (self._x, self._y + self._height // 2),
                                       self.radius)
                pygame.draw.rect(self.win, self.progressColour,
                             (self._x, self._y, int(self._width * self.value/self.max)-self.radius, self._height))

            gfxdraw.filled_circle(self.win, *circle, self.handleRadius, self.handleColour)
            gfxdraw.aacircle(self.win, *circle, self.handleRadius, self.handleColour)
        
        
            
        

if __name__ == '__main__':
    from pygame_widgets.textbox import TextBox

    pygame.init()
    win = pygame.display.set_mode((1000, 600))

    progslider = ProgressiveSlider(win, 100, 100, 800, 40, min=0, max=99, step=1)
    output = TextBox(win, 475, 200, 50, 50, fontSize=30)

    v_slider = ProgressiveSlider(win, 900, 200, 40, 300, min=0, max=99, step=1, vertical=True)
    v_output = TextBox(win, 800, 320, 50, 50, fontSize=30)

    output.disable()
    v_output.disable()

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                quit()

        win.fill((255, 255, 255))

        output.setText(progslider.getValue())
        v_output.setText(v_slider.getValue())

        pygame_widgets.update(events)
        pygame.display.update()
        