import pygame as pg
from Application.Core.Utilities import path_asset, Spritesheet
from random import randrange


class Player:

    @property
    def current_worm(self):
        self._current_worms = self.worms.pop(0)
        self.worms.append(self._current_worms)
        return self._current_worms

    @property
    def worms(self):
        return self._worms

    def __init__(self, name, nb_worms):
        self.name = name
        self.score = 0
        self._worms = [Worms(name + str(i)) for i in range(nb_worms)]
        self._current_worms = self.current_worm

    def events(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self._current_worms.set_direction(-1)
        if keys[pg.K_RIGHT]:
            self._current_worms.set_direction(1)
        if keys[pg.K_UP]:
            self._current_worms.jump()

        self._current_worms.is_idling = not (keys[pg.K_LEFT] or keys[pg.K_RIGHT])
        self._current_worms.is_walking = keys[pg.K_LEFT] or keys[pg.K_RIGHT]

    def loose(self):
        return len(self.worms) == 0


class Worms(pg.sprite.Sprite):
    def __init__(self, name):
        pg.sprite.Sprite.__init__(self)
        self.name = name
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
        self.drag = -0.5
        self.speed = 1
        self.gravity = 0.8
        self.jump_force = 7
        self.is_ground_colliding = None
        self.is_jumping = False
        self.is_dying = False
        self.is_idling = True
        self.is_walking = False
        self._flip = False

    def update(self):
        self.move()
        self.acceleration = pg.math.Vector2(0, 0)
        self.update_animation()

    def update_animation(self):
        if self.is_idling:
            self.image = self._spritesheet_idle.animate()
        elif self.is_walking:
            self.image = self._spritesheet_walk.animate()
        elif self.is_jumping:
            self.image = self._spritesheet_jump.animate()
        elif self.is_dying:
            self.image = self._spritesheet_dead.animate()

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
        if not self.is_ground_colliding:
            self.acceleration.y = self.gravity
            self.is_idling = False
            self.is_walking = False
            self.is_jumping = True

        else:
            self.velocity.y = 0
            self.is_jumping = False

        self.acceleration.x += self.velocity.x * self.drag
        # movement equations
        self.velocity += self.acceleration
        self.position += (self.velocity + 0.5 * self.acceleration)
        self.rect.center = self.position

    def jump(self):

        if self.is_ground_colliding:
            self.is_ground_colliding = None
            self.velocity.y = -self.jump_force

    def die(self):
        self.is_walking = self.is_idling = self.is_jumping = False
        self.is_dying = True
