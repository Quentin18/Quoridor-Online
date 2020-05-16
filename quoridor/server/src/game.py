"""
Quoridor Online
Quentin Deschamps, 2020
"""


class Game:
    """Create a game"""
    def __init__(self, game_id, nb_players):
        self.game_id = game_id
        self.nb_players = nb_players
        self.connected = 0
        self.names = [''] * nb_players
        self.run = False
        self.current_player = -1
        self.last_play = ''
        self.winner = ''
        self.wanted_restart = []

    def add_player(self):
        """Add a player"""
        self.connected += 1
        print(f"Player added in game {self.game_id}")

    def players_missing(self):
        """Return the number of players missing to start"""
        return self.nb_players - self.connected

    def ready(self):
        """Return True if the game can start"""
        return self.connected == self.nb_players

    def start(self):
        """Start the game"""
        self.winner = ''
        self.current_player = 0
        self.run = True
        print(f"Game {self.game_id} starts!")

    def play(self, data):
        """Get a move"""
        print(f"Move in game {self.game_id}: {data}")
        self.last_play = data
        if data.split(';')[-1] == 'w':
            print(self.get_name_current(), "wins!")
            self.winner = self.get_name_current()
            self.current_player = -1
            self.run = False
            self.wanted_restart = []
        else:
            self.current_player = (self.current_player + 1) % self.nb_players

    def add_name(self, data):
        """Add a player's name"""
        num_player = int(data.split(';')[1])
        name = data.split(';')[2]
        self.names[num_player] = name
        print(f"{name} (player {num_player}) added in game {self.game_id}")

    def get_name_current(self):
        """Return the name of the current player"""
        return self.names[self.current_player]

    def restart(self, data):
        """Restart the game if there are enough players"""
        num_player = int(data.split(';')[1])
        self.wanted_restart.append(num_player)
        print(f"{self.names[num_player]} wants to restart")
        print(f"Restart: {len(self.wanted_restart)}/{self.nb_players}")
        if len(self.wanted_restart) == self.nb_players:
            self.start()


class Games:
    """Manage games"""
    def __init__(self, nb_players):
        self.games = {}
        self.nb_players = nb_players
        self.num_player = 0
        self.game_id = 0

    def add_game(self):
        """Create a new game"""
        if self.game_id not in self.games:
            self.num_player = 0
            self.games[self.game_id] = Game(self.game_id, self.nb_players)
            print("Game", self.game_id, "created")

    def del_game(self, game_id):
        """Delete a game"""
        if game_id in self.games:
            del self.games[game_id]
            print("Game", game_id, "closed")

    def accept_player(self):
        """Accept a player"""
        if self.game_id not in self.games:
            self.add_game()
        self.games[self.game_id].add_player()
        return self.game_id, self.num_player

    def launch_game(self):
        """Lauch a game"""
        if self.games[self.game_id].ready():
            self.games[self.game_id].start()
            self.game_id += 1
        else:
            self.num_player += 1

    def find_game(self, game_id):
        """Find a game"""
        if game_id in self.games:
            return self.games[game_id]
        return None
