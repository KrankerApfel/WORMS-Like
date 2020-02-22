import pygame as pg
from yaml import load, SafeLoader
from Application.Core.Utilities import path_asset, Spritesheet, get_mask_collision_normal
from Application.Environnement.Terrain import Ground
from random import randrange
import os
from Application.Entities.Weapons import Frag, Bazooka

physic = load(open(os.path.join("Application", "Data", "Configuration.yml"), 'r'), Loader=SafeLoader)[
    "Physic"]
param = load(open(os.path.join("Application", "Data", "Configuration.yml"), 'r'), Loader=SafeLoader)[
    "Parameters"]


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
        self._current_worms = self.worms[0]

    def events(self):
        # self.target.rect.center = self._current_worms.position
        # self.target.update()
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self._current_worms.set_direction(-1)
        if keys[pg.K_d]:
            self._current_worms.set_direction(1)
        if keys[pg.K_w]:
            self._current_worms.jump()

        self._current_worms._play_idling_animation = not (keys[pg.K_LEFT] or keys[pg.K_RIGHT])
        self._current_worms._play_walking_animation = keys[pg.K_LEFT] or keys[pg.K_RIGHT]

    def loose(self):
        return len(self.worms) == 0

    @property
    def current_worms(self):
        return self._current_worms


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
        self.gravity = physic["GRAVITY"]
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
        self.velocity += pg.math.Vector2(direction[0], direction[1])
        if self.life <= 0:
            self.die()
