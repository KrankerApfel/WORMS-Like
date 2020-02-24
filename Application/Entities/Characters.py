import pygame as pg
from yaml import load, SafeLoader
from Application.Core.Utilities import path_asset, Spritesheet, get_mask_collision_normal
from Application.Environnement.Terrain import Ground
from Application.Entities.Weapons import Frag, Bazooka, HandWithFrag
from random import randrange
import os

physic = load(open(os.path.join("Application", "Data", "Configuration.yml"), 'r'), Loader=SafeLoader)[
    "Physic"]
param = load(open(os.path.join("Application", "Data", "Configuration.yml"), 'r'), Loader=SafeLoader)[
    "Parameters"]
inputs = load(open(os.path.join("Application", "Data", "Configuration.yml"), 'r'), Loader=SafeLoader)[
    "Inputs"]
settings = load(open(os.path.join("Application", "Data", "Configuration.yml"), 'r'), Loader=SafeLoader)[
    "Application"]


class Player:

    # change current worm
    @property
    def current_worm(self):
        self._current_worms = self.worms.pop(0)
        self.worms.append(self._current_worms)
        return self._current_worms

    @property
    def worms(self):
        return self._worms

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    def __init__(self, name, nb_worms):
        self.name = name
        self.score = 0
        self._worms = [Worms(name + str(i)) for i in range(nb_worms)]
        self._current_worms = self.worms[0]
        self.weapon = None
        self.weapon_index = 0
        self.inventory = ["Frag", "Bazooka", None]
        self.can_move = False
        self.is_shooting = False
        self.end_shooting = True
        self.can_shoot = True
        self.start_shooting_time = 0
        self.shooting_time = 0
        self._target = None
        self.turn_end = False

    def events(self):
        keys = pg.key.get_pressed()
        if keys[inputs["MOVE_LEFT"]]:
            self._current_worms.set_direction(-1)
        if keys[inputs["MOVE_RIGHT"]]:
            self._current_worms.set_direction(1)
        if keys[inputs["JUMP"]]:
            self._current_worms.jump()

        self._current_worms._play_idling_animation = not (keys[inputs["MOVE_LEFT"]] or keys[inputs["MOVE_RIGHT"]])
        self._current_worms._play_walking_animation = keys[inputs["MOVE_LEFT"]] or keys[inputs["MOVE_RIGHT"]]

        if keys[inputs["CHANGE_WEAPONS"]]:
            self.weapon_index = (self.weapon_index+1)%len(self.inventory)
            if self.inventory[self.weapon_index].__eq__("Frag"):
                self.weapon = None
                self.weapon = HandWithFrag(self._current_worms.rect.center)
            elif self.inventory[self.weapon_index].__eq__("Bazooka"):
                self.weapon = None
                self.weapon = Bazooka(self._current_worms.rect.center, 0, 5)
            else:
                self.weapon = None

        self.shooting_logic(keys)
        if self.weapon:
            self.weapon.update_idle_position(self._current_worms.position, self.target.angle, self._current_worms.rect.center)
            if self.weapon.ballistic.exploded:
                self.turn_end = True

    def loose(self):
        return len(self.worms) == 0

    @property
    def current_worms(self):
        return self._current_worms

    def shooting_logic(self, keys):
        if self.can_shoot and self.weapon is not None:  # if in game state to shoot
            if keys[inputs["SHOOT"]] and self.end_shooting:  # if started pressing space
                self.is_shooting = True
                self.start_shooting_time = pg.time.get_ticks()
                self.end_shooting = False

            if not keys[inputs["SHOOT"]] and self.is_shooting:  # if the space key is not pressed and was pressed before
                self.weapon.ballistic.pos_initial = self._current_worms.rect.center
                self.shooting_time = pg.time.get_ticks()
                self.can_shoot = False
                self.weapon.shoot((pg.time.get_ticks() - self.start_shooting_time) / 1000, self.target.angle)
                self.start_shooting_time = 0
                self.end_shooting = True
                self.is_shooting = False

            if keys[inputs["SHOOT"]] and self.start_shooting_time != 0 and (
                    pg.time.get_ticks() - self.start_shooting_time) / 1000 > 2:  # if holding space and its been more than 2 seconds shoot
                if self.weapon is not None:
                    self.weapon.ballistic.pos_initial = self._current_worms.rect.center
                    self.shooting_time = pg.time.get_ticks()
                    self.can_shoot = False
                    self.weapon.shoot((pg.time.get_ticks() - self.start_shooting_time) / 1000, self.target.angle)
                    self.start_shooting_time = 0
                self.is_shooting = False
                self.end_shooting = True
        if (pg.time.get_ticks() - self.shooting_time) / 1000 > 5:  # if it has been 5 second, can start shooting again
            self.can_shoot = True


class Worms(pg.sprite.Sprite):
    def __init__(self, name):
        pg.sprite.Sprite.__init__(self)
        self.name = name
        self.life = param["WORMS_LIFE"]
        self._spritesheet_idle = Spritesheet(path_asset("Graphics\\Spritesheets\\Worms-Idle.png"),
                                             (0, 0, 16, 16), 2, 15)
        self._spritesheet_jump = Spritesheet(path_asset("Graphics\\Spritesheets\\Worms-Jump.png"),
                                             (0, 0, 16, 16), 3, 15, loop=False)
        self._spritesheet_walk = Spritesheet(path_asset("Graphics\\Spritesheets\\Worms-Walk.png"),
                                             (0, 0, 16, 16), 3, 10)
        self._spritesheet_dead = Spritesheet(path_asset("Graphics\\Spritesheets\\Worms-Dead.png"),
                                             (0, 0, 16, 16), 4, 15, loop=False)
        self.image = self._spritesheet_idle.frame_images[0]
        self.rect = self.image.get_rect()
        self.position = (randrange(1000), randrange(600))
        self.rect.center = self.position
        self.velocity = pg.math.Vector2(0, 0)
        self.acceleration = pg.math.Vector2(0, 0)
        self.drag = physic["WORMS_DRAG"]
        self.speed = physic["WORMS_SPEED"]
        self.gravity = physic["GRAVITY"]*physic["WORMS_MASS"]
        self.jump_force = physic["WORMS_JUMP_FORCE"]
        self.collided_objects = []
        self._play_jump_animation = False
        self._play_dying_animation = False
        self._play_idling_animation = True
        self._play_walking_animation = False
        self._is_jumping = False
        self.is_die = False
        self.die_timer = 100
        self._flip = False
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.move()
        self.acceleration = pg.math.Vector2(0, 0)
        self.update_animation()
        if self.rect.center[1] > settings['SCREEN_WIDTH']:
            self.die()

    def update_animation(self):
        if not self.is_die:
            if self._play_idling_animation:
                self.image = self._spritesheet_idle.animate()
            elif self._play_walking_animation:
                self.image = self._spritesheet_walk.animate()
            elif self._play_jump_animation:
                self.image = self._spritesheet_jump.animate()
        elif self._play_dying_animation:
            self.image = self._spritesheet_dead.animate()
            self.die_timer -= 1
            if self.die_timer <= 0:
                self.kill()

        self.image = pg.transform.flip(self.image, self._flip, False)

    def set_direction(self, x=None, y=None):
        if x:
            self.acceleration.x = self.speed * x
            if x > 0:
                self._flip = True
            elif x < 0:
                self._flip = False
        if y:
            self.acceleration.y = self.speed * y

    def move(self):

        if len(self.collided_objects) <= 1:
            self.acceleration.y = self.gravity
            self._play_idling_animation = False
            self._play_walking_animation = False
            self._play_jump_animation = True
            self._is_jumping = len(self.collided_objects) > 1

        elif not self._is_jumping:
            self.velocity.y = 0
            self._play_jump_animation = False
            for o in self.collided_objects:
                if not o == self:

                    p = get_mask_collision_normal(self, o)
                    if p[0]:
                        self.velocity.x = self.acceleration.x = 0

        self.acceleration.x += self.velocity.x * self.drag
        for o in self.collided_objects:
            if isinstance(o, Ground):

                p = get_mask_collision_normal(self, o)
                if p[1] < 0:
                    self.velocity.y = self.acceleration.y = 0
                    self.position = (self.position[0], self.position[1] - self.rect.height / 2)
                elif p[1] > 0:
                    self.velocity.y = self.acceleration.y = self.gravity
        # movement equations
        self.velocity += self.acceleration
        self.position += (self.velocity + 0.5 * self.acceleration)
        self.rect.center = self.position

    def jump(self):

        if len(self.collided_objects) > 1:
            self.velocity.y = -self.jump_force
            self._is_jumping = True

    def die(self):
        self._play_walking_animation = self._play_idling_animation = self._play_jump_animation = False
        self._play_dying_animation = True
        self.is_die = True

    def hurt(self, damage, direction):
        self.life -= damage
        # self.velocity += pg.math.Vector2(direction[0], direction[1])
        if self.life <= 0:
            self.die()
