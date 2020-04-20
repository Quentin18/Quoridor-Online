"""
Quoridor Online
Quentin Deschamps, 2020
"""
import pygame


class Wall:
    """Create a wall"""
    def __init__(self, coord1, coord2, win):
        self.coord1 = coord1
        self.coord2 = coord2
        if coord1.same_row(coord2):
            self.coord3 = coord1.south
            self.coord4 = coord2.south
            self.orient = "e"
        if coord1.same_column(coord2):
            self.coord3 = coord1.east
            self.coord4 = coord2.east
            self.orient = "s"

        self.cross_wall = None

        # Window attributs
        self.win = win
        self.rect = self.make_rect()
        self.rect_small = self.make_rect_small()
        self.color = None
        self.code = ";".join([str(coord1.x), str(coord1.y), self.orient])

    def __str__(self):
        return ", ".join([str(self.coord1), str(self.coord2),
                         str(self.coord3), str(self.coord4), self.orient])

    def set_color(self, color):
        """Set the wall's color"""
        self.color = color

    def make_cross_wall(self):
        """Return the cross wall"""
        if self.orient == "e":
            self.cross_wall = self.coord1.wall_south
        if self.orient == "s":
            self.cross_wall = self.coord1.wall_east

    def make_rect(self):
        """Return the rect corresponding to the wall on the window"""
        win = self.win
        (x, y) = self.coord1.top_left
        if self.orient == "e":
            return (x + win.case_side, y,
                    win.wall_width, 2*win.case_side + win.wall_width)
        elif self.orient == "s":
            return (x, y + win.case_side,
                    2*win.case_side + win.wall_width, win.wall_width)
        return None

    def make_rect_small(self):
        """Return the small rect corresponding to the wall on the window"""
        win = self.win
        (x, y) = self.coord1.top_left
        if self.orient == "e":
            return (x + win.case_side, y, win.wall_width, win.case_side)
        elif self.orient == "s":
            return (x, y + win.case_side, win.case_side, win.wall_width)
        return None

    def draw(self, color):
        """Draw the wall on the window"""
        pygame.draw.rect(self.win.win, color, self.rect)

    def __eq__(self, other):
        """Operator == for two walls"""
        return (self.coord1 == other.coord1
                and self.coord2 == other.coord2
                and self.coord3 == other.coord3
                and self.coord4 == other.coord4)


class Walls:
    """Manage all the walls played"""
    def __init__(self):
        self.walls = []
        self.blocked_coords = {}

    def add_wall(self, wall):
        """Add a wall"""
        self.walls.append(wall)
        d = self.blocked_coords
        if wall.coord1.tuple not in d:
            d[wall.coord1.tuple] = [wall.coord2.tuple]
        else:
            d[wall.coord1.tuple].append(wall.coord2.tuple)
        if wall.coord2.tuple not in d:
            d[wall.coord2.tuple] = [wall.coord1.tuple]
        else:
            d[wall.coord2.tuple].append(wall.coord1.tuple)
        if wall.coord3.tuple not in d:
            d[wall.coord3.tuple] = [wall.coord4.tuple]
        else:
            d[wall.coord3.tuple].append(wall.coord4.tuple)
        if wall.coord4.tuple not in d:
            d[wall.coord4.tuple] = [wall.coord3.tuple]
        else:
            d[wall.coord4.tuple].append(wall.coord3.tuple)

    def draw(self):
        """Draw the walls"""
        for w in self.walls:
            w.draw(w.color)

    def contains(self, wall):
        """Return True if wall can't be added"""
        d = self.blocked_coords
        if wall.coord1.tuple in d:
            if wall.coord2.tuple in d[wall.coord1.tuple]:
                return True
        if wall.coord3.tuple in d:
            if wall.coord4.tuple in d[wall.coord3.tuple]:
                return True
        return False

    def wall_in_walls(self, wall):
        """Return True if the wall is in walls"""
        for w in self.walls:
            if wall == w:
                return True
        return False

    def can_add(self, wall):
        """Return True if the wall can be added"""
        return (not self.contains(wall)
                and not self.wall_in_walls(wall.cross_wall))

    def no_wall(self, coord1, coord2):
        """Return True is there is no wall between two positions"""
        d = self.blocked_coords
        if coord1.tuple in d:
            return coord2.tuple not in d[coord1.tuple]
        return True

    def reset(self):
        """Reset the walls"""
        for w in self.walls:
            w.color = None
        self.walls.clear()
        self.blocked_coords.clear()
