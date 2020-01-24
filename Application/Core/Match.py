from Application.Core.Utilities import path_asset
import pygame as pg


class Match:
    def __init__(self, player_number, timer_delay, screen, level=None):
        self.level = dict(background='Graphics/Backgrounds/BKG_theme_1.png',
                          terrain='path/to/terrain.bitmap',
                          wind_velocity=(0, 0),
                          music='path/to/music.ogg',
                          ambiant='path/to/sonor_ambiant.wav')

        self.players = ['player' + str(i) for i in range(player_number)]
        self.turnTimer = timer_delay  # 3600
        self.turn = 0
        self.current_player = self.players.pop(0)
        self.players.append(self.current_player)
        self.bkg = pg.image.load(path_asset(self.level['background']))
        self.screen = screen

    def update(self):
        timeout = False
        if not timeout:  ## or self.current_player.pa <= 0 or self.current_player.passed_turn()

            print('Team ' + self.current_player + ' is playing')
            self.turnTimer -= 1
            print(self.turnTimer)
            if self.turnTimer < 0:
                print('Timeout !')
                self.current_player = self.players.pop(0)
                self.players.append(self.current_player)
                print('turn to ' + self.current_player + ' team !')
                self.turnTimer = 1200
                timeout = True

    def draw(self):
        self.screen.blit(self.bkg, (0, 0))

    def check_loose(self):
        pass
