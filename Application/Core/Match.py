from Application.Core.Utilities import path_asset
from Application.Environnement.Ground import *
import pygame as pg


class Match:
    """
    This class represent a game part, namely a match between players.
    """
    def __init__(self, player_number, timer_delay, level=None):
        self.level_data = dict(background='Graphics/Backgrounds/BKG_theme_1.png',
                               terrain='Graphics/Spritesheets/ground_lvl_1.bmp',
                               wind_velocity=(0, 0),
                               music='path/to/music.ogg',
                               ambiant='path/to/sonor_ambiant.wav')

        self.level = dict()
        self.level["background"] = pg.image.load(path_asset(self.level_data['background']))
        self.level["ground"] = Ground(self.level_data['terrain'])
        self.players = ['player' + str(i) for i in range(player_number)]
        self.turnTimer = timer_delay  # 3600
        self.turn = 0
        self.current_player = self.players.pop(0)
        self.players.append(self.current_player)

    def update(self):
        timeout = False
        if not timeout:  ## or self.current_player.pa <= 0 or self.current_player.passed_turn()

            print('Team ' + self.current_player + ' is playing')
            self.turnTimer -= 1
            print(self.turnTimer)
            if self.turnTimer < 0:
                print('Timeout !')
                #self.level["ground"].update_mask(200, (100, 200)) # destruction test
                self.current_player = self.players.pop(0)
                self.players.append(self.current_player)
                print('turn to ' + self.current_player + ' team !')
                self.turnTimer = 1200
                timeout = True

    def draw(self, screen):
        self.level["ground"].draw(screen)

    def check_loose(self):
        pass
