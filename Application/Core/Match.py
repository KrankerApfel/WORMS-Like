from Application.Entities.Characters import Player
from Application.Environnement.Terrain import *
from Application.Core.Utilities import draw_text
from Application.Entities.Weapons import *
import pygame as pg


class Match:
    """
    This class represent a game part, namely a match between plaoyers.
    """
    gravity = 9.81
    windPower = 0
    windDirection = 0
    drag = 0
    count = 0
    is_shooting = False
    start_shooting_time = 0
    end_shooting = True
    _can_shoot = True
    _can_move = True
    shooting_time = 0

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
        self.target = Target()
        self.targetPosition = (0, 0)
        for player in self.players:
            for worm in player.worms:
                self.worms_group.add(worm)
                self.all_sprites_group.add(worm)

    def update(self):
        self.events()
        self.worms_group.update()
        self.target.update()
        if self.current_player.weapon is not None:
            if self.current_player.weapon.ballistic is not None:
                if self.current_player.weapon.ballistic.exploded:
                    self.current_player.can_move = True
        if self.current_player.weapon:
            self.current_player.weapon.update()
            if self.current_player.weapon.ballistic:
                self.current_player.weapon.ballistic.collided_objects = \
                    pg.sprite.spritecollide(self.current_player.weapon.ballistic,
                                            self.all_sprites_group, False, pg.sprite.collide_mask)
        for w in self.worms_group:
            w.collided_objects = pg.sprite.spritecollide(w, self.all_sprites_group, False, pg.sprite.collide_mask)

        timeout = False
        if not timeout:  # or self.current_player.pa <= 0 or self.current_player.passed_turn()

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
        self.target.player_position = self.current_player.current_worm.rect
        self.current_player.target = self.target

    def draw(self, screen):
        self.level["ground"].draw(screen)
        self.worms_group.draw(screen)
        self.target.draw(screen)
        if self.current_player.weapon:
            self.current_player.weapon.draw(screen)

    def check_loose(self):
        for p in self.players:
            if p.loose():
                return False
        return True

    @property
    def can_shoot(self):
        return self._can_shoot

    @can_shoot.setter
    def can_shoot(self, value):
        self._can_shoot = value
