from Application.Entities.Characters import Player
from Application.Environnement.Terrain import *
from Application.Entities.Characters import Worms
import pygame as pg


class Match:
    """
    This class represent a game part, namely a match between players.
    """

    def __init__(self, player_number, worms_number, timer_delay, level_dict):
        self.level_data = level_dict
        self.level = dict()
        self.level["background"] = pg.image.load(path_asset(self.level_data['background']))
        self.level["ground"] = Ground(self.level_data['terrain'])
        self.players = [Player("player" + str(i), worms_number) for i in range(player_number)]
        self.turnTimer = timer_delay  # 3600
        self.turn = 0
        self.current_player = self.players.pop(0)
        self.players.append(self.current_player)
        self.worms_group = pg.sprite.Group()
        self.all_sprites_group = pg.sprite.Group(self.level["ground"])
        for player in self.players:
            for worm in player.worms:
                self.worms_group.add(worm)
                self.all_sprites_group.add(worm)

    def update(self):
        self.events()
        self.worms_group.update()
        for w in self.worms_group:
            w.collided_objects = pg.sprite.spritecollide(w, self.all_sprites_group, False, pg.sprite.collide_mask)
        timeout = False
        if not timeout:  ## or self.current_player.pa <= 0 or self.current_player.passed_turn()

            self.turnTimer -= 1
            if self.turnTimer < 0:
                print('Timeout !')
                self.level["ground"].update_mask(200, (100, 200))  # destruction test TODO
                self.current_player = self.players.pop(0)
                self.players.append(self.current_player)
                print('turn to ' + self.current_player.name + ' team !')
                self.turnTimer = 1200
                timeout = True

    def events(self):
        self.current_player.events()


     

    def draw(self, screen):
        self.level["ground"].draw(screen)
        self.worms_group.draw(screen)

    def check_loose(self):
        for p in self.players:
            if p.loose():
                return False
        return True
