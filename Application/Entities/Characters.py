import pygame as pg
from Application.Core.Utilities import path_asset
from random import randrange

class Player:
    @property
    def current_worm(self):
        self._current_worms = self.worms.pop(0)
        self.worms.append(self._current_worms)
        return self._current_worms

    def __init__(self, name, nb_worms):
        self.name = name
        self.score = 0
        self.worms = [name + str(i) for i in range(nb_worms)]
        self._current_worms = self.current_worm

    def events(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
           # self._current_worms.set_direction(-1)
           print(self._current_worms + " go left !")
        if keys[pg.K_RIGHT]:
          #  self._current_worms.set_direction(1)
          print(self._current_worms + " go right !")
        if keys[pg.K_UP]:
          #  self._current_worms.jump()
          print(self._current_worms + " jump !")

    def loose(self):
        return len(self.worms) == 0



worm_image = pg.image.load(path_asset("Graphics\\Spritesheets\\worm.png"))


class Worms(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = worm_image
        self.rect = self.image.get_rect()
        self.position = (randrange(1000), randrange(600))
        self.rect.center = self.position
        self.velocity = pg.math.Vector2(0, 0)
        self.acceleration = pg.math.Vector2(0, 0)
        self.drag = -0.5
        self.speed = 5
        self.gravity = 3
        self.jump_force = 30
        self.is_ground_colliding = False

    def update(self):
        self.move()
        self.acceleration = pg.math.Vector2(0, 0)

    def set_direction(self, x=None, y=None):
        if x:
            self.acceleration.x = self.speed * x
            
        if y:
            self.acceleration.y = self.speed * y

    def move(self):
        if not self.is_ground_colliding:
            self.acceleration.y = self.gravity
        else:
            self.velocity.y = 0
        self.acceleration.x += self.velocity.x * self.drag
        # movement equations
        self.velocity += self.acceleration
        self.position += (self.velocity + 0.5 * self.acceleration)

        self.rect.center = self.position

    def jump(self):
        if self.is_ground_colliding:
            self.is_ground_colliding = False
            self.velocity.y = -self.jump_force
