"""
Quoridor Online
Quentin Deschamps, 2020
"""
import sys
import socket
from _thread import start_new_thread
import pickle
from quoridor.server.src.game import Games


def threaded_client(conn, nb_players, num_player, game_id, games):
    """Manage threads for clients"""
    first_data = ";".join([str(nb_players), str(num_player)])
    conn.send(str.encode(first_data))
    run = True
    while run:
        try:
            data = conn.recv(2048).decode()
            game = games.find_game(game_id)
            if game is not None:
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
                run = False
        except socket.error as e:
            print(e)

    games.remove_player(game_id, num_player)
    conn.close()


def server(host, port, nb_players):
    """Game server"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((host, port))
    except socket.error as e:
        str(e)

    s.listen(nb_players)
    print(f"Server for {nb_players} players games started!")
    print("Waiting for a connection...")

    games = Games(nb_players)

    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)
        game_id, num_player = games.accept_player()
        start_new_thread(threaded_client,
                         (conn, nb_players, num_player, game_id, games))
        games.launch_game()


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
