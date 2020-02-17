from Application.Entities.Characters import Player
from Application.Environnement.Terrain import *
from Application.Entities.Characters import Worms
from Application.Entities.Weapons import *
import pygame as pg


class Match:
    """
    This class represent a game part, namely a match between players.
    """
    gravity = 9.81
    windPower = 0
    windDirection = 0
    drag = 0
    count = 0
    is_shooting = False
    t = 0
    getting_time = False
    end_shooting = True

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
        self.weapon = None
        for player in self.players:
            # self.targets_group.add(player.target)
            for worm in player.worms:
                self.worms_group.add(worm)
                self.all_sprites_group.add(worm)

    def update(self):
        self.events()
        self.worms_group.update()
        self.target.update()
        if self.weapon is not None:
            self.weapon.update()
        # self.targets_group.update()
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
        keys = pg.key.get_pressed()
        if keys[pg.K_1]:
            self.weapon = Frag(self.current_player.current_worm.rect, 0, 5)
        if keys[pg.K_2]:
            self.weapon = Bazooka()
        if keys[pg.K_SPACE] and self.end_shooting:
            self.is_shooting = True
            self.getting_time = True
            self.end_shooting = False
            # wait for shoot to end and reset timer and change player
        if keys[pg.K_SPACE] and self.getting_time:
            self.t = pg.time.get_ticks()
            self.getting_time = False

        if not keys[pg.K_SPACE] and self.is_shooting:
            if self.weapon is not None:
                self.weapon.shoot((pg.time.get_ticks() - self.t)/1000, self.target.angle)
            self.end_shooting = True
            self.is_shooting = False


        # self.target._flip = self.current_player.current_worm.flip

    def draw(self, screen):
        self.level["ground"].draw(screen)
        self.worms_group.draw(screen)
        self.target.draw(screen)
        if self.weapon is not None:
            self.weapon.draw(screen)

    def check_loose(self):
        for p in self.players:
            if p.loose():
                return False
        return True
