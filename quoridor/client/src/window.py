"""
Quoridor Online
Quentin Deschamps, 2020
"""
import pygame
from quoridor.client.src.colors import Colors
from quoridor.client.src.widgets import Text, Button
from quoridor.client.src.coord import Coords


def pos_in_rect(rect, pos):
    """Return True if pos is in the rectangle"""
    pos_x, pos_y = pos
    x, y, width, height = rect
    return (x <= pos_x <= x + width
            and y <= pos_y <= y + height)


class Window:
    """Create the window"""
    def __init__(self, width=1000, height=830, case_side=65, wall_width=15,
                 title="Quoridor Online", bgcolor=Colors.white):
        self.width = width
        self.height = height
        self.case_side = case_side
        self.wall_width = wall_width
        self.bgcolor = bgcolor
        self.top_left = (20, 20)
        self.side_board = 9*self.case_side + 10*self.wall_width
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.button_restart = Button("Restart", self.side_board + 60,
                                     self.side_board - 100, Colors.red,
                                     show=False)
        self.button_quit = Button("Quit", self.side_board + 60,
                                  self.side_board - 50, Colors.red)
        self.buttons = [self.button_restart, self.button_quit]
        self.title = Text("Quoridor", Colors.black, size=50)
        self.info = Text("Welcome to Quoridor Online!", Colors.black, size=45)
        self.coords = Coords(self)

    def update_info(self, text, color=None):
        """Update info text"""
        self.info.text = text
        if color is not None:
            self.info.color = color

    def draw_game_board(self, pos):
        """Draw the game board"""
        for c in self.coords.coords:
            rect = c.rect
            if pos_in_rect(rect, pos):
                color = Colors.grey_dark
            else:
                color = Colors.grey
                wall_east = c.wall_east
                wall_south = c.wall_south
                if wall_east and pos_in_rect(wall_east.rect_small, pos):
                    wall_east.draw(Colors.grey_dark)
                elif wall_south and pos_in_rect(wall_south.rect_small, pos):
                    wall_south.draw(Colors.grey_dark)
            c.draw(color)

    def draw_finish_lines(self, players):
        """Draw the finish lines with the player's color"""
        for p in players.players:
            if p.name != '':
                if p.orient == "north":
                    pygame.draw.line(
                        self.win, p.color,
                        (self.top_left[0], self.top_left[1] + self.side_board),
                        (self.top_left[0] + self.side_board,
                         self.top_left[1] + self.side_board),
                        self.wall_width)
                elif p.orient == "east":
                    pygame.draw.line(
                        self.win, p.color,
                        (self.top_left[0], self.top_left[1]),
                        (self.top_left[0], self.top_left[1] + self.side_board),
                        self.wall_width)
                elif p.orient == "south":
                    pygame.draw.line(
                        self.win, p.color,
                        (self.top_left[0], self.top_left[1]),
                        (self.top_left[0] + self.side_board, self.top_left[1]),
                        self.wall_width)
                elif p.orient == "west":
                    pygame.draw.line(
                        self.win, p.color,
                        (self.top_left[0] + self.side_board, self.top_left[1]),
                        (self.top_left[0] + self.side_board,
                         self.top_left[1] + self.side_board),
                        self.wall_width)

    def draw_right_panel(self, game, players):
        """Draw the right panel with player's informations"""
        x, y = self.side_board + 50, 20
        self.title.draw(self.win, (x + 10, y))
        for p in players.players:
            if p.name != '':
                text_p = Text(f"{p.name}: {p.walls_remain} walls", p.color)
                text_p.draw(self.win, (x, y + 100*p.num_player + 100))

    def draw_buttons(self):
        """Draw buttons"""
        for b in self.buttons:
            if b.show:
                b.draw(self.win)

    def redraw_window(self, game, players, walls, pos):
        """Redraw the full window"""
        self.win.fill(self.bgcolor)
        self.draw_game_board(pos)
        self.draw_finish_lines(players)
        self.draw_right_panel(game, players)
        self.draw_buttons()
        players.draw(self)
        walls.draw()
        self.info.draw(self.win, (self.top_left[0], self.height - 50))
        pygame.display.update()
