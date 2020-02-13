from Application.Core.Menu import *
from Application.Core.Match import *
from Application.Core.Utilities import image_fade_in
import os
import random
import pygame as pg
from yaml import load, BaseLoader,SafeLoader


class Game:
    """
    The game class. It contains all the game logic and manage loops as physic update,
    events handling or screen rendering.
    """

    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.App_config = load(open(os.path.join("Application", "Data", "Configuration.yml"), 'r'), Loader=SafeLoader)[
            "Application"]
        self.screen = pg.display.set_mode((self.App_config["SCREEN_WIDTH"], self.App_config["SCREEN_HEIGHT"]))
        pg.display.set_icon(pg.image.load(path_asset(self.App_config["ICON"])))
        pg.display.set_caption(self.App_config["TITLE_GAME"])
        self.clock = pg.time.Clock()
        self.running = True
        self.on_menu = True
        self.on_game = False
        self.on_game_over = False
        self.playing = False
        self.menu = Menu((163, 195, 208),  self.App_config, self.screen, self)
        self.match = None

    def new(self):
        """
        Function to load game assets and init parameters before run it.
        :return: void
        """
        self.run()
        pass

    def run(self):
        """
        Application main loop.
        :return: void
        """
        self.playing = True
        while self.playing:
            self.clock.tick( self.App_config["FPS"])
            self.draw()
            self.fixed_update()
            self.update()
            self.events()

    def update(self):
        if self.on_game:
            self.match.update()
        pass

    def fixed_update(self):
        # physic update loop
        pass

    def events(self):
        """
        Event handling function.
        :return: void
        """
        if self.on_menu:
            self.menu.events()
            self.on_menu = False
            self.match = Match(self.menu.game_part_data['players_number'], self.menu.game_part_data['worms_number'], 10,
                               level_dict=random.choice(
                                   list(
                                       load(
                                           open(os.path.join("Application", "Data", "Levels.yml"), 'r'),
                                           Loader=BaseLoader
                                       ).values()
                                   )))
            self.on_game = True

        if self.on_game:
            self.match.events()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    def draw(self):
        """
        Screen rendering function
        :return: void
        """

        # Until we are on menu screen
        if self.on_menu:
            self.menu.draw()
        # if we are on game screen
        elif self.on_game:
            self.screen.blit(self.match.level["background"], (0, 0))
            self.match.draw(self.screen)
        pg.display.flip()

    def splash_screen(self):
        """
        Function to displayed a splash screen. According to Wikipedia :
        ''A splash screen is a graphical control element consisting of a window containing an image, a logo,
          and the current version of the software. A splash screen usually appears while a game or program is launching.''
        :return:
        """
        image_fade_in(pg.image.load(path_asset("Graphics\\splash.jpeg")),
                      0,
                      0,
                      300,
                      (0, 0, 0),
                      self.screen
                      )

    def quit(self):
        """
        A function to quit the application frost-free.
        :return: void
        """
        self.on_menu = False
        self.playing = False
        self.running = False
        pg.mixer.quit()
        pg.quit()
