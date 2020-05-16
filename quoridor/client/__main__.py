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
from quoridor.client.src.sounds import Sounds


def client(host, port):
    """Game client"""
    print("Welcome to Quoridor Online!")
    print("Host:", host)
    print("Port:", port)
    # Name input
    name = ''
    while name == '' or len(name) > 10:
        name = input("Enter your name: ").capitalize()
        if len(name) > 10:
            print("Too long")
    print("Waiting for the server...")

    # Connexion
    n = Network(host, port)
    try:
        n.connect()
        # Receive nb players, num player
        data = n.recv()
        nb_players, num_player = int(data[0]), int(data[1])
    except Exception:
        print("Unable to connect to the server")
        exit()

    # Send name
    try:
        n.send(';'.join(['N', str(num_player), name]))
    except Exception:
        print("Impossible to send data to the server")
        exit()

    print("Connexion established!")
    print(f"Hello {name}! You are player {num_player}!")

    # Init pygame
    pygame.init()
    clock = pygame.time.Clock()
    path = os.path.dirname(os.path.abspath(__file__))
    sounds = Sounds(path)

    # Init game
    win = Window()
    coords = win.coords
    players = Players(nb_players, coords)
    player = players.players[num_player]
    walls = Walls()
    pf = PathFinder()

    last_play = ''
    run = True
    ready = False
    start = False

    while run:
        clock.tick(40)
        n.send('get')
        try:
            game = n.get_game()
        except Exception:
            run = False
            print("Couldn't get game")
            break

        # Start a game
        if not start:
            if not ready:
                players.set_names(game.names)
                win.update_info(
                    f"Waiting for {game.players_missing()} players...")
                ready = game.ready()
            if game.run:
                current_p = players.players[game.current_player]
                win.update_info(f"Let's go! {current_p.name} plays!",
                                current_p.color)
                try:
                    sounds.start_sound.play()
                except Exception:
                    pass
                start = True
            elif game.wanted_restart != []:
                nb = len(game.wanted_restart)
                p = players.players[game.wanted_restart[-1]]
                win.update_info(
                    f"{p.name} wants to restart! ({nb}/{nb_players})",
                    p.color)

        # Continue a game
        else:
            get_play = game.last_play
            if get_play != '' and get_play != last_play:
                if get_play[0] == 'D':
                    current_p = players.players[game.current_player]
                    win.update_info(f"{current_p.name} plays!",
                                    current_p.color)
                elif get_play[0] == 'P':
                    if players.play(get_play, coords, walls, pf):
                        current_p = players.players[game.current_player]
                        win.update_info(f"{current_p.name} plays!",
                                        current_p.color)
                    else:
                        win.update_info(f"{game.winner} wins!")
                        try:
                            sounds.winning_sound.play()
                        except Exception:
                            pass
                        win.button_restart.show = True
                        start = False
                last_play = get_play

        pos = pygame.mouse.get_pos()
        win.redraw_window(game, players, walls, pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if win.button_quit.click(pos):
                    run = False
                    pygame.quit()
                elif (not game.run and win.button_restart.click(pos)
                        and win.button_restart.show):   # Restart
                    coords.reset()
                    players.reset(coords)
                    walls.reset()
                    pf.reset()
                    win.button_restart.show = False
                    n.send(';'.join(['R', str(num_player)]))
                elif player.can_play_wall(game):    # Put a wall
                    mes = player.play_put_wall(
                        pos, coords, walls, n, pf, players)
                    if mes != '':
                        win.update_info(mes)

            elif event.type == pygame.KEYDOWN:  # Move pawn
                if player.can_play(game):
                    player.play_move(walls, n)

    print("Good bye!")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Not enough arguments: [Host address] [Port number]")
    else:
        host = str(sys.argv[1])
        port = int(sys.argv[2])
        client(host, port)
