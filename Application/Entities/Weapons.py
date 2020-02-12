import pygame as pg
from Application.Core.Utilities import path_asset
from math import cos, sin

frag = pg.image.load(path_asset("Graphics\\Spritesheets\\Grenade.png"))
bazooka = pg.image.load(path_asset("Graphics\\Spritesheets\\Rocket_Launcher.png"))
target = pg.image.load(path_asset("Graphics\\Spritesheets\\Target.png"))


class Weapon(pg.sprite.Sprite):

    def __init__(self, damage, image, position, drag, speed, gravity):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.velocity = pg.math.Vector2(0, 0)
        self.acceleration = pg.math.Vector2(0, 0)
        self.drag = drag
        self.speed = speed
        self.gravity = gravity
        self.is_colliding = False
        self.damage = damage

    def shoot(self):
        # calculate angle and physic of weapon
        print("printing from weapon")

    def events(self):
        # equation de cercle pour que le visuer tourne autour du joeuur
        keys = pg.key.get_pressed()

    def update(self):
        self.events()


class Frag(Weapon):

    def __init__(self, damage, position, drag, speed, gravity):
        Weapon.__init__(self, damage, frag, position, drag, speed, gravity)

    def shoot(self):
        # calculate angle and physic of frag
        print("printing from frag")


class Bazooka(Weapon):

    def __init__(self, damage, position, drag, speed, gravity):
        Weapon.__init__(self, damage, bazooka, position, drag, speed, gravity)

    def shoot(self):
        # calculate angle and physic of bazooka and call specific sprite
        print("printing from frag")


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

    def events(self):
        if not self.is_active:
            keys = pg.key.get_pressed()
            if keys[pg.K_UP]:
                self.aim(self.angle + 0.1)
            if keys[pg.K_DOWN]:
                self.aim(self.angle - 0.1)
            if keys[pg.K_SPACE]:
                self.shoot()
        else:
            self.rect.center = (0, 0)

    def update(self):
        self.events()

    def aim(self, angle):
        self.angle = angle
        self.x = self.radius * cos(angle) + self.player_position[0]
        self.y = self.radius * sin(angle) + self.player_position[1]
        print(sin(angle))
        self.rect.center = (self.x, self.y)

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

    def draw(self, screen):
        screen.blit(self.image, self.rect.center)