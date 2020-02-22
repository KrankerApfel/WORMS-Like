import pygame as pg
import os
from yaml import load, SafeLoader
from Application.Core.Utilities import path_asset, Spritesheet
from Application.Environnement.Terrain import Ground
from Application.Entities.Characters import Worms
from math import cos, sin, pi

target = pg.image.load(path_asset("Graphics\\Spritesheets\\Target.png"))
inputs = load(open(os.path.join("Application", "Data", "Configuration.yml"), 'r'), Loader=SafeLoader)[
    "Inputs"]


class Weapon(pg.sprite.Sprite):
    # gravity = 9.81
    gravity = 500

    def __init__(self, damage, spritesheet, position, drag, v0):
        pg.sprite.Sprite.__init__(self)
        self.image = spritesheet.frame_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos_initial = position
        self.velocity = pg.math.Vector2(0, 0)
        self.acceleration = pg.math.Vector2(0, 0)
        self.drag = drag
        self.v0 = v0
        self.angle = 0
        self.is_colliding = False
        self.damage = damage
        self.t = 0
        self.initial_t = 0
        self.idle = True
        self.mask = pg.mask.from_surface(self.image)
        self.collided_objects = []

    def shoot(self, initial_t, angle):
        # calculate angle and physic of weapon
        print("printing from weapon")

    def update(self):
        self.update_position()

    def update_position(self): return

    def update_idle_postion(self, position):
        if self.idle:
            self.rect.center = (position[0] + 10, position[1] - 10)

    def draw(self, screen):
        screen.blit(self.image, self.rect.center)


class Frag(Weapon):

    def __init__(self, position, drag, v0):
        Weapon.__init__(self, 500, Spritesheet(path_asset("Graphics\\Spritesheets\\Grenade.png"),
                                               (0, 0, 16, 16), 1, 15), position, drag, 500)
        self.rect.center = (self.pos_initial[0] + 10, self.pos_initial[1] - 10)

    def shoot(self, time_held, angle):
        self.idle = False

        self.t = 0
        self.initial_t = pg.time.get_ticks() / 1000  # initial_t
        self.angle = angle
        self.v0 = (time_held / 2 * 500)  # v0 = inital speed

    def update_position(self):
        # V0 = (t/tmax) * vmaxspeed

        if self.initial_t != 0:
            self.t = (pg.time.get_ticks() / 1000) - self.initial_t
            x = self.pos_initial[0] + self.v0 * cos(self.angle) * self.t
            y = self.pos_initial[1] + self.gravity * 0.5 * pow(self.t, 2) + self.v0 * sin(self.angle) * self.t
            self.rect.center = (x, y)
            self.explode()

    def explode(self):
        if len(self.collided_objects) > 1:
            for o in self.collided_objects:
                if isinstance(o, Ground):
                    o.update_mask(50, self.rect.center)
                elif isinstance(o, Worms) and not o.__eq__(self):
                    o.hurt(50, get_mask_collision_normal(o, self))


class Bazooka(Weapon):

    def __init__(self, position, drag, v0):
        Weapon.__init__(self, 50, Spritesheet(path_asset("Graphics\\Spritesheets\\Rocket_Launcher.png"),
                                              (0, 0, 16, 16), 1, 15), position, drag, v0, 500)

    def shoot(self, initial_t, angle):
        # calculate angle and physic of bazooka and call specific sprite
        print("printing from frag")

    def update_position(self):
        # TODO
        return


class Target(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = target
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.player_position = (0, 0)
        self.x = 600
        self.y = 400
        self.radius = 120
        self.angle = 0
        self.is_active = False
        self._flip = False

    def events(self):
        if not self.is_active:
            angle = self.angle
            keys = pg.key.get_pressed()
            if keys[inputs["AIM_UP"]]:
                angle += 0.1
            if keys[inputs["AIM_DOWN"]]:
                angle -= 0.1
            if keys[inputs["MOVE_LEFT"]] and self._flip:
                self._flip = False
                self.swap_angle()
            if keys[inputs["MOVE_RIGHT"]] and not self._flip:
                self._flip = True
                self.swap_angle()

            self.aim(angle)
        else:
            self.rect.center = (0, 0)

    def update(self):
        self.events()

    def aim(self, angle):
        if (self._flip and cos(angle) >= 0) or (not self._flip and cos(angle) <= 0):
            self.angle = angle
            self.x = self.radius * cos(angle) + self.player_position[0]
            self.y = self.radius * sin(angle) + self.player_position[1]
        self.rect.center = (self.x, self.y)

    def swap_angle(self):
        self.angle = pi - self.angle

    @property
    def player_position(self):
        return self._player_position

    @player_position.setter
    def player_position(self, value):
        self._player_position = value

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value

    @property
    def flip(self):
        return self._flip

    @flip.setter
    def flip(self, value):
        self._flip = value

    def draw(self, screen):
        screen.blit(self.image, self.rect.center)
