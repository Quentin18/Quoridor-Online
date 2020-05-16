"""
Quoridor Online
Quentin Deschamps, 2020
"""
import pygame


class Sounds:
    """Manage sounds"""
    def __init__(self, path):
        pygame.mixer.init()
        self.start_sound = pygame.mixer.Sound(
            "".join([path, "/sounds/start_sound.wav"]))
        self.winning_sound = pygame.mixer.Sound(
            "".join([path, "/sounds/winning_sound.wav"]))
