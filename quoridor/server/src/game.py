"""
Quoridor Online
Quentin Deschamps, 2020
"""


class Game:
    """Create a game"""
    def __init__(self, game_id, nb_players):
        self.game_id = game_id
        self.nb_players = nb_players
        self.current_player = -1
        self.connected = 0
        self.last_play = ""
        self.names = []
        self.winner = ""

    def add_player(self):
        """Add a player"""
        self.connected += 1

    def players_missing(self):
        """Return the number of players missing to start"""
        return self.nb_players - self.connected

    def ready(self):
        """Return True if the game can start"""
        return self.connected == self.nb_players

    def start(self):
        """Start the game"""
        self.current_player = 0

    def play(self, data):
        """Get a move"""
        print(f"Move in game {self.game_id}: {data}")
        self.last_play = data
        if data.split(";")[-1] == "w":
            print(f"{self.names[self.current_player]} wins!")
        self.current_player = (self.current_player + 1) % self.nb_players

    def add_name(self, data):
        """Add a player's name"""
        name = data.split(":")[1]
        self.names.append(name)
        print(f"{name} added in game {self.game_id}")
