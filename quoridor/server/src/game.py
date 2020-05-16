"""
Quoridor Online
Quentin Deschamps, 2020
"""


class Game:
    """Create a game"""
    def __init__(self, game_id, nb_players):
        self.game_id = game_id
        self.nb_players = nb_players
        self.connected = [False] * nb_players
        self.names = [''] * nb_players
        self.run = False
        self.current_player = -1
        self.last_play = ''
        self.winner = ''
        self.wanted_restart = []

    def add_player(self, num_player):
        """Add a player"""
        self.connected[num_player] = True
        print(f"[Game {self.game_id}]: player {num_player} added")

    def add_name(self, data):
        """Add a player's name"""
        num_player = int(data.split(';')[1])
        name = data.split(';')[2]
        self.names[num_player] = name
        print(f"[Game {self.game_id}]: {name} added as player {num_player}")

    def remove_player(self, num_player):
        """Remove a player"""
        self.connected[num_player] = False
        self.names[num_player] = ''
        if self.nb_players_connected() == 1:
            self.run = False
            self.current_player == -1
        else:
            if num_player == self.current_player:
                self.current_player = self.next_player(self.current_player)
                self.last_play = ';'.join(['D', str(num_player)])
        print(f"[Game {self.game_id}]: player {num_player} removed")

    def nb_players_connected(self):
        """Return the number of players connected"""
        return self.connected.count(True)

    def players_missing(self):
        """Return the number of players missing to start"""
        return self.nb_players - self.nb_players_connected()

    def ready(self):
        """Return True if the game can start"""
        return self.nb_players_connected() == self.nb_players

    def next_player(self, current):
        """Return the new current player"""
        current = (current + 1) % self.nb_players
        while not self.connected[current]:
            current = (current + 1) % self.nb_players
        return current

    def get_name_current(self):
        """Return the name of the current player"""
        return self.names[self.current_player]

    def start(self):
        """Start the game"""
        self.winner = ''
        self.current_player = self.next_player(-1)
        self.run = True
        print(f"[Game {self.game_id}]: started")

    def play(self, data):
        """Get a move"""
        print(f"[Game {self.game_id}]: move {data}")
        self.last_play = data
        if data.split(';')[-1] == 'w':
            print(f"[Game {self.game_id}]: {self.get_name_current()} wins!")
            self.winner = self.get_name_current()
            self.current_player = -1
            self.run = False
            self.wanted_restart = []
        else:
            self.current_player = self.next_player(self.current_player)

    def restart(self, data):
        """Restart the game if there are enough players"""
        num_player = int(data.split(';')[1])
        self.wanted_restart.append(num_player)
        print(f"[Game {self.game_id}]: {self.names[num_player]} asked restart",
              end=' ')
        print(f"{len(self.wanted_restart)}/{self.nb_players}")
        if len(self.wanted_restart) == self.nb_players:
            self.start()


class Games:
    """Manage games"""
    def __init__(self, nb_players):
        self.games = {}
        self.nb_players = nb_players
        self.num_player = 0
        self.game_id = 0

    def find_game(self, game_id):
        """Find a game"""
        if game_id in self.games:
            return self.games[game_id]
        return None

    def add_game(self):
        """Create a new game"""
        if self.game_id not in self.games:
            self.num_player = 0
            self.games[self.game_id] = Game(self.game_id, self.nb_players)
            print(f"[Game {self.game_id}]: created")

    def del_game(self, game_id):
        """Delete a game"""
        if game_id in self.games:
            del self.games[game_id]
            print(f"[Game {game_id}]: closed")
            if game_id == self.game_id:
                self.num_player = 0

    def accept_player(self):
        """Accept a player"""
        if self.game_id not in self.games:
            self.add_game()
        self.games[self.game_id].add_player(self.num_player)
        return self.game_id, self.num_player

    def launch_game(self):
        """Lauch a game"""
        if self.games[self.game_id].ready():
            self.games[self.game_id].start()
            self.game_id += 1
        else:
            self.num_player += 1

    def remove_player(self, game_id, num_player):
        """Remove a player"""
        game = self.find_game(game_id)
        if game is not None:
            game.remove_player(num_player)
            if not game.run:
                self.del_game(game_id)
