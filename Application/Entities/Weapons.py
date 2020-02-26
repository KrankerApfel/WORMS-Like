import pygame as pg
import os
from yaml import load, SafeLoader, Loader
from Application.Core.Utilities import path_asset, Spritesheet, get_mask_collision_normal
from Application.Environnement.Terrain import Ground
from math import cos, sin, pi

target = pg.image.load(path_asset("Graphics\\Spritesheets\\Target.png"))
inputs = load(open(os.path.join("Application", "Data", "Configuration.yml"), 'r'), Loader=SafeLoader)[
    "Inputs"]
physic = load(open(os.path.join("Application", "Data", "Configuration.yml"), 'r'), Loader=SafeLoader)[
    "Physic"]
wind = load(open(os.path.join("Application", "Data", "Levels.yml"), 'r'), Loader=Loader)[
     "Level_1"]["wind_velocity"]


class Ballistic(pg.sprite.Sprite):

    def __init__(self, damage, spritesheet, position, drag, v0, mass):
        pg.sprite.Sprite.__init__(self)
        self.image = spritesheet.frame_images[0]
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = (0, 0)
        self.pos_initial = position
        self.collided_objects = []
        self.velocity = pg.math.Vector2(0, 0)
        self.acceleration = pg.math.Vector2(0, 0)
        self.drag = drag
        self.v0 = v0
        self.angle = 0
        self.is_colliding = False
        self.damage = damage
        self.gravity = physic['GRAVITY'] * mass
        self.t = 0
        self.initial_t = 0
        self.blast_radius = 50
        self.idle = True
        self.mask = pg.mask.from_surface(self.image)
        self.collided_objects = []
        self.exploded = False
        self.rect.center = (self.pos_initial[0], self.pos_initial[1])
        self.timer = 50
        self.max_time_held = 2
        self.max_speed = 500

    def shoot(self, time_held, angle):
        print("print from balistic shoot")
        return

    def draw(self, screen):
        if not self.exploded:
            screen.blit(self.image, self.rect.center)

    def update(self):
        self.update_position()

    def update_position(self):
        return
        # V0 = (t/tmax) * vmaxspeed

    def explode(self):
        if self.collided_objects:
            for o in self.collided_objects:
                if isinstance(o, Ground) and not self.exploded:
                    o.update_mask(self.blast_radius, self.rect.center)
                elif not o.__eq__(self) or not isinstance(o, Ground):
                    o.hurt(1000, get_mask_collision_normal(o, self))
            self.exploded = True


class Weapon(pg.sprite.Sprite):
    @property
    def ballistic(self):
        return self._ballistic

    @ballistic.setter
    def ballistic(self, value):
        self._ballistic = value

    def __init__(self, spritesheet, position):
        pg.sprite.Sprite.__init__(self)
        self.image = spritesheet.frame_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.idle = True
        self.mask = pg.mask.from_surface(self.image)
        self._ballistic = None

    def shoot(self, time_held, angle):
        self._ballistic.shoot(time_held, angle)
        self.idle = False

    def draw(self, screen):
        if self.idle:
            screen.blit(self.image, self.rect.center)
        else:
            self._ballistic.draw(screen)

    def update(self):
        if not self.idle:
            self._ballistic.update_position()

    def update_idle_position(self, position, angle, player_position):
        if self.idle:
            self.rect.center = (position[0], position[1])
            x = 5 * cos(angle) + player_position[0]
            y = 5 * sin(angle) + player_position[1]
            self.rect.center = (x, y)


class HandWithFrag(Weapon):
    def __init__(self, position):
        Weapon.__init__(self, Spritesheet(path_asset("Graphics\\Spritesheets\\FragInHand.png"),
                                          (0, 0, 16, 16), 1, 15), position)
        self._ballistic = Frag(position, 0, 5)


class Frag(Ballistic):

    def __init__(self, position, drag, v0):
        Ballistic.__init__(self, 500, Spritesheet(path_asset("Graphics\\Spritesheets\\Grenade.png"),
                                                  (0, 0, 16, 16), 1, 15), position, drag, 500, physic["FRAG_MASS"])
        self.rect.center = (self.pos_initial[0], self.pos_initial[1])
        self.timer = 50

    def shoot(self, time_held, angle):
        self.idle = False
        self.t = 0
        self.initial_t = pg.time.get_ticks() / 1000  # initial_t
        self.angle = angle
        self.v0 = (time_held / self.max_time_held * self.max_speed)  # v0 = inital speed

    def update_position(self):
        # V0 = (t/tmax) * vmaxspeed
        if self.initial_t != 0:
            self.t = (pg.time.get_ticks() / 1000) - self.initial_t
            x = self.pos_initial[0] + self.v0 * cos(self.angle) * self.t
            y = self.pos_initial[1] + self.gravity * 0.5 * pow(self.t, 2) + self.v0 * sin(self.angle) * self.t
            self.rect.center = (x, y)
            self.timer -= 1
            if self.timer <= 0:
                self.explode()


class Rocket(Ballistic):

    def __init__(self, position, drag, v0):
        Ballistic.__init__(self, 500, Spritesheet(path_asset("Graphics\\Spritesheets\\Bomb.png"),
                                                  (0, 0, 16, 16), 4, 15), position, drag, 500, physic["ROCKET_MASS"])
        self.rect.center = (self.pos_initial[0], self.pos_initial[1])
        self.max_speed = 450

    def shoot(self, time_held, angle):
        self.idle = False
        self.t = 0
        self.initial_t = pg.time.get_ticks() / 1000  # initial_t
        self.angle = angle
        self.v0 = (time_held / self.max_time_held * self.max_speed)  # v0 = inital speed
        return

    def update_position(self):
        if self.initial_t != 0:
            self.t = (pg.time.get_ticks() / 1000) - self.initial_t
            x = self.pos_initial[0] + self.v0 * cos(self.angle) * self.t + (wind[0] * self.t)
            y = self.pos_initial[1] + self.gravity * 0.5 * pow(self.t, 2) + self.v0 * sin(self.angle) * self.t + (wind[1] * self.t)
            if self.v0 > 0:
                self.v0 = self.v0 - 0.02 * self.v0*self.t   
            self.rect.center = (x, y)
            self.timer -= 1
            if self.timer <= 0:
                self.explode()


class Bazooka(Weapon):

    def __init__(self, position, drag, v0):
        Weapon.__init__(self, Spritesheet(path_asset("Graphics\\Spritesheets\\Rocket_Launcher.png"),
                                          (0, 0, 16, 16), 1, 15), position)
        self._ballistic = Rocket(position, 0, 5)


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
