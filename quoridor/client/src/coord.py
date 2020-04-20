"""
Quoridor Online
Quentin Deschamps, 2020
"""
import pygame
from quoridor.client.src.wall import Wall


class Coord:
    """Create a coord"""
    def __init__(self, x, y, win, coords):
        self.win = win
        self.coords = coords

        self.x = x
        self.y = y
        self.tuple = (x, y)
        self.is_occuped = False

        # Window attributs
        self.top_left = self.make_top_left()
        self.middle = self.make_middle()
        self.rect = self.make_rect()

        # Links
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.wall_east = None
        self.wall_south = None

    def coord_north(self):
        """Return the coord on the north"""
        if self.y - 1 >= 0:
            return self.coords.find_coord(self.x, self.y - 1)
        return None

    def coord_east(self):
        """Return the coord on the east"""
        if self.x + 1 <= 8:
            return self.coords.find_coord(self.x + 1, self.y)
        return None

    def coord_south(self):
        """Return the coord on the south"""
        if self.y + 1 <= 8:
            return self.coords.find_coord(self.x, self.y + 1)
        return None

    def coord_west(self):
        """Return the coord on the west"""
        if self.x - 1 >= 0:
            return self.coords.find_coord(self.x - 1, self.y)
        return None

    def make_top_left(self):
        """Return the top left point of a coord on a window"""
        win = self.win
        x = ((win.wall_width + win.case_side)*self.x
             + win.wall_width + win.top_left[0])
        y = ((win.wall_width + win.case_side)*self.y
             + win.wall_width + win.top_left[1])
        return (x, y)

    def make_middle(self):
        """Return the middle point of a coord on a window"""
        win = self.win
        x = ((win.wall_width + win.case_side)*self.x
             + (win.wall_width + win.case_side // 2)
             + win.top_left[0])
        y = ((win.wall_width + win.case_side)*self.y
             + (win.wall_width + win.case_side // 2)
             + win.top_left[1])
        return (x, y)

    def make_rect(self):
        """Return the rectangle of the coord"""
        win = self.win
        x, y = self.top_left
        return (x, y, win.case_side, win.case_side)

    def make_wall_east(self):
        """Return the east wall of the coord"""
        if self.east is not None and self.y != 8:
            return Wall(self, self.east, self.win)
        return None

    def make_wall_south(self):
        """Return the south wall of the coord"""
        if self.south is not None and self.x != 8:
            return Wall(self, self.south, self.win)
        return None

    def link_coord(self):
        """Link the coords"""
        self.north = self.coord_north()
        self.east = self.coord_east()
        self.south = self.coord_south()
        self.west = self.coord_west()

    def make_walls(self):
        """Make the walls around the coord"""
        self.wall_east = self.make_wall_east()
        self.wall_south = self.make_wall_south()

    def make_cross_walls(self):
        """Make the cross walls of the walls of the coord"""
        if self.wall_east is not None:
            self.wall_east.make_cross_wall()
        if self.wall_south is not None:
            self.wall_south.make_cross_wall()

    def same_row(self, other):
        """Return True if the two coords are on the same row"""
        return self.y == other.y

    def same_column(self, other):
        """Return True if the two coords are on the same column"""
        return self.x == other.x

    def __str__(self):
        """String format of a coord"""
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        """Operator == between two coords"""
        return self.x == other.x and self.y == other.y

    def draw(self, color):
        """Draw the rectangle of a coord"""
        pygame.draw.rect(self.win.win, color, self.rect)


class Coords:
    """Manage the coords"""
    def __init__(self, win):
        self.win = win
        self.coords = self.make_coords()
        self.link_coords()
        self.make_walls()

    def make_coords(self):
        """Make coords"""
        coords = []
        for x in range(9):
            for y in range(9):
                coords.append(Coord(x, y, self.win, self))
        return coords

    def link_coords(self):
        """Link coords"""
        for c in self.coords:
            c.link_coord()

    def make_walls(self):
        """Make walls"""
        for c in self.coords:
            c.make_walls()
        for c in self.coords:
            c.make_cross_walls()

    def find_coord(self, x, y):
        """Find the coord corresponding to x and y"""
        return self.coords[x * 9 + y]

    def reset(self):
        """Reset coords"""
        for c in self.coords:
            c.is_occuped = False
