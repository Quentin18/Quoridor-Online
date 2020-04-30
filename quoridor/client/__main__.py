"""
Quoridor Online
Quentin Deschamps, 2020
"""
import sys
import os
import pygame
from quoridor.client.src.network import Network
from quoridor.client.src.window import Window
from quoridor.client.src.player import Players
from quoridor.client.src.wall import Walls
from quoridor.client.src.pathfinder import PathFinder


def client(host, port):
    print("Welcome to Quoridor Online!")
    name = input("Enter your name: ").capitalize()
    run = True
    print("Host:", host)
    print("Port:", port)
    print("Waiting for the server...")
    try:
        n = Network(host, port)
        data = n.getP().split(";")
    except Exception:
        print("Unable to connect to the server")
        quit()
    nb_players, num_player = int(data[0]), int(data[1])

    pygame.init()
    clock = pygame.time.Clock()
    pygame.mixer.init()
    path = os.path.dirname(os.path.abspath(__file__))
    file = "".join([path, "/sounds/winning_sound.wav"])
    winning_sound = pygame.mixer.Sound(file)

    win = Window()
    coords = win.coords
    players = Players(nb_players, coords)
    player = players.players[num_player]
    player.set_name(name)
    walls = Walls()
    pf = PathFinder()
    print("Connexion established!")
    print(f"Hello {player.name}! You are player {num_player}!")
    last_play = ""

    n.send(f"name:{player.name}")
    finish_game = False
    set_names = False

    while run:
        clock.tick(40)
        try:
            game = n.send("get")
        except Exception:
            run = False
            print("Couldn't get game")
            break

        if not set_names and len(game.names) == nb_players:
            players.set_names(game)
            set_names = True

        if not finish_game:
            get_play = game.last_play
            if get_play != "" and get_play != last_play:
                if not players.play(get_play, coords, walls, pf):
                    print(f"{game.names[game.current_player - 1]} wins!")
                    winning_sound.play()
                    finish_game = True
                last_play = get_play
            if game.current_player == num_player:
                player.has_played = False

        pos = pygame.mouse.get_pos()
        win.redraw_window(finish_game, players, walls, game, pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if win.button_quit.click(pos):
                    run = False
                    pygame.quit()
                elif finish_game and win.button_restart.click(pos):
                    coords.reset()
                    players.reset(coords)
                    walls.reset()
                    pf.reset()
                    finish_game = False
                elif (not finish_game and not player.has_played
                        and player.has_walls()):
                    game = player.play_put_wall(
                        game, pos, coords, walls, n, pf, players)

        if not finish_game and not player.has_played:
            try:
                game = player.play_move(game, walls, n)
            except Exception:
                pass

    print("Good bye!")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Not enough arguments: [Host address] [Port number]")
    else:
        host = str(sys.argv[1])
        port = int(sys.argv[2])
        client(host, port)
