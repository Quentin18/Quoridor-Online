"""
Quoridor Online
Quentin Deschamps, 2020
"""
import sys
import socket
from _thread import start_new_thread
import pickle
from quoridor.server.src.game import Game


def threaded_client(conn, nb_players, num_player, game_id, games):
    first_data = ";".join([str(nb_players), str(num_player)])
    conn.send(str.encode(first_data))
    while True:
        try:
            data = conn.recv(2048).decode()
            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                elif data.split(';')[0] == 'N':
                    game.add_name(data)
                elif data.split(';')[0] == 'P':
                    game.play(data)
                elif data.split(';')[0] == 'R':
                    game.restart(data)
                conn.sendall(pickle.dumps(game))
            else:
                break
        except socket.error as e:
            print(e)

    print("Lost connection")
    try:
        del games[game_id]
        print("Closing game", game_id)
    except Exception:
        pass
    conn.close()


def server(host, port, nb_players):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((host, port))
    except socket.error as e:
        str(e)

    s.listen(nb_players)
    print("Server Started!\nWaiting for a connection...")

    games = {}
    num_player = 0
    game_id = 0

    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)
        if game_id not in games:
            num_player = 0
            games[game_id] = Game(game_id, nb_players)
        games[game_id].add_player()

        start_new_thread(threaded_client,
                         (conn, nb_players, num_player, game_id, games))
        if games[game_id].ready():
            games[game_id].start()
            game_id += 1
        else:
            num_player = num_player + 1


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Not enough arguments")
        print("[Host address] [Port number] [Number of players]")
    else:
        host = str(sys.argv[1])
        port = int(sys.argv[2])
        nb_players = int(sys.argv[3])
        if nb_players not in [2, 3, 4]:
            print("Only for 2, 3 or 4 players")
        else:
            server(host, port, nb_players)

# Get IP address on Linux: hostname -I
