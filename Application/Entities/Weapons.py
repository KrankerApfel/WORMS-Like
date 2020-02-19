import pygame as pg

from Application.Core.Utilities import path_asset
from math import cos, sin, pi

frag_image = pg.image.load(path_asset("Graphics\\Spritesheets\\Grenade.png"))
bazooka_image = pg.image.load(path_asset("Graphics\\Spritesheets\\Rocket_Launcher.png"))
target = pg.image.load(path_asset("Graphics\\Spritesheets\\Target.png"))


class Weapon(pg.sprite.Sprite):
    #gravity = 9.81
    gravity = 500

    def __init__(self, damage, image, position, drag, v0):
        pg.sprite.Sprite.__init__(self)
        self.image = image
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

    def shoot(self, initial_t, angle):
        # calculate angle and physic of weapon
        print("printing from weapon")

    def update(self):
        self.update_position()

    def update_position(self):
        return

    def draw(self, screen):
        screen.blit(self.image, self.rect.center)


class Frag(Weapon):

    def __init__(self, position, drag, v0):
        Weapon.__init__(self, 500, frag_image, position, drag, 500)

    def shoot(self, time_held, angle):
        self.t = 0
        self.initial_t = pg.time.get_ticks() / 1000 # initial_t
        self.angle = angle
        self.v0 = (time_held/2 * 500) # v0 = inital speed

    def update_position(self):
        # V0 = (t/tmax) * vmaxspeed

        if self.initial_t != 0:
            self.t = (pg.time.get_ticks() / 1000) - self.initial_t
            x = self.pos_initial[0] + self.v0 * cos(self.angle) * self.t
            y = self.pos_initial[1] + self.gravity * 0.5 * pow(self.t, 2) + self.v0 * sin(self.angle) * self.t
            self.rect.center = (x, y)


class Bazooka(Weapon):

    def __init__(self, damage, position, drag, v0, gravity):
        Weapon.__init__(self, damage, bazooka_image, position, drag, v0, gravity)

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
            if keys[pg.K_UP]:
                angle += 0.1
            if keys[pg.K_DOWN]:
                angle -= 0.1
            if keys[pg.K_a] and self._flip:
                self._flip = False
                self.swap_angle()
            if keys[pg.K_d] and not self._flip:
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
