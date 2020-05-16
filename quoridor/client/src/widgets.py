"""
Quoridor Online
Quentin Deschamps, 2020
"""
import pygame
from quoridor.client.src.colors import Colors


class Text:
    """Create a text box"""
    def __init__(self, text, color, size=30, font="comicsans"):
        self.text = text
        self.color = color
        self.size = size
        self.font = font

    def draw(self, win, pos):
        """Draw the text on the window"""
        font = pygame.font.SysFont(self.font, self.size)
        text = font.render(self.text, 1, self.color, True)
        win.blit(text, pos)


class Button:
    """Create a button"""
    def __init__(self, text, x, y, color, width=150, height=40, show=True):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.show = show

    def draw(self, win):
        """Draw the button on the window"""
        pygame.draw.rect(win, self.color,
                         (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, Colors.black)
        win.blit(text,
                 (self.x + round(self.width/2) - round(text.get_width()/2),
                  self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        """Return True if pos is in the button rectangle"""
        pos_x, pos_y = pos
        return (self.x <= pos_x <= self.x + self.width
                and self.y <= pos_y <= self.y + self.height)
