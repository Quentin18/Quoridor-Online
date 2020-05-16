"""
Quoridor Online
Quentin Deschamps, 2020
"""
import pygame
from quoridor.client.src.window import pos_in_rect
from quoridor.client.src.colors import Colors


class Player():
    """Create a player"""
    def __init__(self, num_player, walls_remain, orient, color, coord,
                 radius=20):
        self.num_player = num_player
        self.orient = orient
        self.color = color
        self.coord = coord
        self.radius = radius
        self.name = ''
        self.walls_remain = walls_remain

    def set_name(self, name):
        """Set the name of the player"""
        if name != '':
            self.name = name

    def get_num_player(self):
        """Get the num of the player"""
        return self.num_player

    def has_walls(self):
        """Return True if the player has walls"""
        return self.walls_remain > 0

    def can_play(self, game):
        """Return True if the player can play"""
        return game.run and game.current_player == self.num_player

    def can_play_wall(self, game):
        """Return True if the player can play a wall"""
        return self.can_play(game) and self.has_walls()

    def send_move(self, network, coord):
        """Send a move to the server"""
        if self.has_win(coord):
            win = "w"
        else:
            win = "c"
        data = ";".join(['P', str(self.num_player), str(0),
                        str(coord.x), str(coord.y), win])
        network.send(data)

    def play_move(self, walls, network):
        """Play a move if it is possible"""
        keys = pygame.key.get_pressed()
        coord = self.coord

        # Left
        if keys[pygame.K_LEFT]:
            c = coord.west
            if c is not None and walls.no_wall(coord, c):
                if c.is_occuped:
                    c2 = c.west
                    if (c2 is not None and not c2.is_occuped
                            and walls.no_wall(c, c2)):
                        self.send_move(network, c2)
                else:
                    self.send_move(network, c)

        # Right
        elif keys[pygame.K_RIGHT]:
            c = coord.east
            if c is not None and walls.no_wall(coord, c):
                if c.is_occuped:
                    c2 = c.east
                    if (c2 is not None and not c2.is_occuped
                            and walls.no_wall(c, c2)):
                        self.send_move(network, c2)
                else:
                    self.send_move(network, c)

        # Up
        elif keys[pygame.K_UP]:
            c = coord.north
            if c is not None and walls.no_wall(coord, c):
                if c.is_occuped:
                    c2 = c.north
                    if (c2 is not None and not c2.is_occuped
                            and walls.no_wall(c, c2)):
                        self.send_move(network, c2)
                else:
                    self.send_move(network, c)

        # Down
        elif keys[pygame.K_DOWN]:
            c = coord.south
            if c is not None and walls.no_wall(coord, c):
                if c.is_occuped:
                    c2 = c.south
                    if (c2 is not None and not c2.is_occuped
                            and walls.no_wall(c, c2)):
                        self.send_move(network, c2)
                else:
                    self.send_move(network, c)

    def send_wall(self, network, coord, orient):
        """Send a wall to the server"""
        data = ";".join(['P', str(self.num_player), str(1),
                        str(coord.x), str(coord.y), orient])
        network.send(data)

    def play_put_wall(self, pos, coords, walls, network,
                      path_finder, players):
        """Put a wall if it is possible"""
        for c in coords.coords:
            wall_east = c.wall_east
            wall_south = c.wall_south
            for w in [wall_east, wall_south]:
                if (w is not None and pos_in_rect(w.rect_small, pos)
                        and walls.can_add(w)):
                    if path_finder.play_wall(w, players):
                        self.send_wall(network, c, w.orient)
                        return ''
                    else:
                        return "You can't block players!"
        return ''

    def draw(self, win):
        """Draw player on the game board"""
        (x, y) = self.coord.middle
        pygame.draw.circle(win.win, self.color,
                           (x, y), self.radius)
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.name[0], 1, Colors.white)
        win.win.blit(text, (x - self.radius // 2, y - self.radius // 2))

    def has_win(self, coord):
        """Return True if the player wins in the coord"""
        if self.orient == "north" and coord.y == 8:
            return True
        if self.orient == "east" and coord.x == 0:
            return True
        if self.orient == "south" and coord.y == 0:
            return True
        if self.orient == "west" and coord.x == 8:
            return True
        return False


class Players:
    """Manage the players"""
    def __init__(self, nb_players, coords):
        self.nb_players = nb_players
        if nb_players == 4:
            self.players = [
                Player(0, 5, "north", Colors.red, coords.find_coord(4, 0)),
                Player(1, 5, "east", Colors.blue, coords.find_coord(8, 4)),
                Player(2, 5, "south", Colors.green, coords.find_coord(4, 8)),
                Player(3, 5, "west", Colors.yellow, coords.find_coord(0, 4))]
        elif self.nb_players == 2:
            self.players = [
                Player(0, 10, "north", Colors.red, coords.find_coord(4, 0)),
                Player(1, 10, "south", Colors.green, coords.find_coord(4, 8))]
        elif self.nb_players == 3:
            self.players = [
                Player(0, 7, "north", Colors.red, coords.find_coord(4, 0)),
                Player(1, 7, "east", Colors.blue, coords.find_coord(8, 4)),
                Player(2, 7, "south", Colors.green, coords.find_coord(4, 8))]

    def draw(self, win):
        """Draw all players on the game board"""
        for p in self.players:
            if p.name != '':
                p.draw(win)

    def get_player(self, num_player):
        """Get a player"""
        return self.players[num_player]

    def play(self, last_play, coords, walls, path_finder):
        """Make a player play"""
        data = last_play.split(";")
        player = self.get_player(int(data[1]))
        type_play = int(data[2])
        x, y = int(data[3]), int(data[4])
        if type_play == 0:   # Move
            player.coord.is_occuped = False
            player.coord = coords.find_coord(x, y)
            player.coord.is_occuped = True
            win = data[5]
            if win == "w":
                return False
            return True
        elif type_play == 1:    # Wall
            orient = data[5]
            coord_wall = coords.find_coord(x, y)
            if orient == "e":
                wall = coord_wall.wall_east
            elif orient == "s":
                wall = coord_wall.wall_south
            wall.set_color(player.color)
            walls.add_wall(wall)
            player.walls_remain -= 1
            path_finder.add_wall(wall)
        return True

    def set_names(self, names):
        """Set the names of players"""
        for player, name in zip(self.players, names):
            player.set_name(name)

    def reset(self, coords):
        """Reset the players"""
        if self.nb_players == 2:
            walls_remain = 10
        elif self.nb_players == 3:
            walls_remain = 7
        elif self.nb_players == 4:
            walls_remain = 5
        for p in self.players:
            if p.orient == "north":
                p.coord = coords.find_coord(4, 0)
            elif p.orient == "east":
                p.coord = coords.find_coord(8, 4)
            elif p.orient == "south":
                p.coord = coords.find_coord(4, 8)
            elif p.orient == "west":
                p.coord = coords.find_coord(0, 4)
            p.walls_remain = walls_remain
