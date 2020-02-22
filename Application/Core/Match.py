from Application.Entities.Characters import Player
from Application.Environnement.Terrain import *
from Application.Entities.Characters import Worms
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
    getting_time = False
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

        if self.can_shoot:  #if in game state to shoot
            if keys[pg.K_SPACE] and self.end_shooting: #if started pressing space
                self.is_shooting = True
                self.getting_time = True
                self.end_shooting = False

                # wait for shoot to end and reset timer and change player
            if keys[pg.K_SPACE] and self.getting_time: #get the time once at the moment you start pressing spcae aka keydown
                self.start_shooting_time = pg.time.get_ticks()
                self.getting_time = False

            if not keys[pg.K_SPACE] and self.is_shooting: #if the space key is not pressed and was pressed before
                if self.weapon is not None:
                    self.shooting_time = pg.time.get_ticks()
                    self.can_shoot = False
                    self.weapon.shoot((pg.time.get_ticks() - self.start_shooting_time)/1000, self.target.angle)
                    self.start_shooting_time = 0

                self.end_shooting = True
                self.is_shooting = False

            if keys[pg.K_SPACE] and self.start_shooting_time != 0 and (pg.time.get_ticks() - self.start_shooting_time)/1000 > 2: #if holding space and its been more than 2 seconds shoot
                if self.weapon is not None:
                    self.shooting_time = pg.time.get_ticks()
                    self.can_shoot = False
                    self.weapon.shoot((pg.time.get_ticks() - self.start_shooting_time) / 1000, self.target.angle)
                    self.start_shooting_time = 0
                self.is_shooting = False
                self.end_shooting = True
        if (pg.time.get_ticks() - self.shooting_time) / 1000 > 5: #if it has been 5 second, can start shooting again 
            self.can_shoot = True
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

    @property
    def can_shoot(self):
        return self._can_shoot

    @can_shoot.setter
    def can_shoot(self, value):
        self._can_shoot = value
