import pygame


def drawText(win, text, colour, rect, font, align='centre'):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    fontHeight = font.size('Tg')[1]

    while text:
        i = 1

        if y + fontHeight > rect.bottom:
            break

        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        if i < len(text):
            i = text.rfind(' ', 0, i) + 1

        image: pygame.Surface = font.render(text[:i], 1, colour)

        imageRect: pygame.Rect = image.get_rect()

        imageRect.center = rect.center

        if align == 'left':
            imageRect.left = rect.left
        elif align == 'right':
            imageRect.right = rect.right

        win.blit(image, (imageRect.left, y))
        y += fontHeight + lineSpacing

        text = text[i:]

    return text
