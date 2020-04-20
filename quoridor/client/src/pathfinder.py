"""
Quoridor Online
Quentin Deschamps, 2020
"""
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class PathFinder:
    """Create the path finder to avoid blocked players"""
    def __init__(self):
        self.finder = AStarFinder()
        self.side = 17
        self.matrix = [[1]*self.side for _ in range(self.side)]
        self.make_walls()

    def make_walls(self):
        """Init the walls"""
        for i in range(self.side):
            if i % 2 == 1:
                for j in range(self.side):
                    if j % 2 == 1:
                        self.matrix[i][j] = 0

    def pos_player_in_grid(self, player):
        """Return the position of a player in the grid"""
        return (2*player.coord.y, 2*player.coord.x)

    def print_grid(self, grid=True, players=None):
        """Print the grid"""
        matrix = self.matrix.copy()
        if players is not None:
            for p in players.players:
                i, j = self.pos_player_in_grid(p)
                matrix[i][j] = -1
        grid = Grid(matrix=matrix)
        print(grid.grid_str())

    def add_wall(self, wall):
        """Add a wall"""
        if wall.orient == "e":
            y, x = 2*wall.coord1.x + 1, 2*wall.coord1.y
            for i in range(3):
                self.matrix[x + i][y] = 0
        elif wall.orient == "s":
            y, x = 2*wall.coord1.x, 2*wall.coord1.y + 1
            for i in range(3):
                self.matrix[x][y + i] = 0

    def remove_wall(self, wall):
        """Remove a wall"""
        if wall.orient == "e":
            y, x = 2*wall.coord1.x + 1, 2*wall.coord1.y
            for i in range(3):
                self.matrix[x + i][y] = 1
        elif wall.orient == "s":
            y, x = 2*wall.coord1.x, 2*wall.coord1.y + 1
            for i in range(3):
                self.matrix[x][y + i] = 1

    def find_path(self, player, show=False):
        """Return True if the player can finish"""
        x, y = self.pos_player_in_grid(player)
        grid = Grid(matrix=self.matrix)
        if player.orient == "north":
            x_end = self.side - 1
            for y_end in range(0, self.side, 2):
                start = grid.node(y, x)
                end = grid.node(y_end, x_end)
                path, runs = self.finder.find_path(start, end, grid)
                if path != []:
                    if show:
                        print(grid.grid_str(path=path, start=start, end=end))
                    return True
                grid.cleanup()

        elif player.orient == "east":
            y_end = 0
            for x_end in range(0, self.side, 2):
                start = grid.node(y, x)
                end = grid.node(y_end, x_end)
                path, runs = self.finder.find_path(start, end, grid)
                if path != []:
                    if show:
                        print(grid.grid_str(path=path, start=start, end=end))
                    return True
                grid.cleanup()

        elif player.orient == "south":
            x_end = 0
            for y_end in range(0, self.side, 2):
                start = grid.node(y, x)
                end = grid.node(y_end, x_end)
                path, runs = self.finder.find_path(start, end, grid)
                if path != []:
                    if show:
                        print(grid.grid_str(path=path, start=start, end=end))
                    return True
                grid.cleanup()

        elif player.orient == "west":
            y_end = self.side - 1
            for x_end in range(0, self.side, 2):
                start = grid.node(y, x)
                end = grid.node(y_end, x_end)
                path, runs = self.finder.find_path(start, end, grid)
                if path != []:
                    if show:
                        print(grid.grid_str(path=path, start=start, end=end))
                    return True
                grid.cleanup()

        return False

    def play_wall(self, wall, players):
        """Return True if the wall doesn't block players"""
        self.add_wall(wall)
        for p in players.players:
            if not self.find_path(p):
                self.remove_wall(wall)
                return False
        return True

    def reset(self):
        """Reset the matrix"""
        self.matrix.clear()
        self.matrix = [[1]*self.side for _ in range(self.side)]
        self.make_walls()
