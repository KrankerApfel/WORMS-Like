import pygame as pg


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
