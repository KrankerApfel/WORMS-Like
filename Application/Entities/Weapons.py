import pygame as pg
from Application.Core.Utilities import path_asset
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
        self.target = Target((650, 350))

    def shoot(self):
        #calculate angle and physic of weapon
        print("printing from weapon")

    def events(self):
        # equation de cercle pour que le visuer tourne autour du joeuur
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.target.aim(0, -5)
        if keys[pg.K_DOWN]:
            self.target.aim(0, 5)

    def update(self):
        self.events()

class Frag(Weapon):

    def __init__(self, damage, position, drag, speed, gravity):
        Weapon.__init__(self, damage, frag,position,drag,speed,gravity)

    def shoot(self):
        #calculate angle and physic of frag
        print("printing from frag")


class Bazooka(Weapon):

    def __init__(self, damage, position, drag, speed, gravity):
        Weapon.__init__(self, damage, bazooka,position,drag,speed,gravity)

    def shoot(self):
        #calculate angle and physic of bazooka and call specific sprite
        print("printing from frag")


class Target(pg.sprite.Sprite):

    def __init__(self, position):
        pg.sprite.Sprite.__init__(self)
        self.image = target
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.x = 0
        self.y = 0

    def aim(self, x, y):
        self.x += x
        self.y += y
        self.rect.center = (self.x, self.y)
