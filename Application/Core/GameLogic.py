from Application.Core.Settings import *
from Application.Core.Menu import *
from Application.Core.Utilities import image_fade_in
import pygame as pg


class Game:
    """
    The game class. It contains all the game logic and manage loops as physic update,
    events handling or screen rendering.
    """
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.Settings = Settings(
            "WORMS Motherfuckers !",
            1200,
            600,
            "Graphics\\icon.png",
            "WORMS Like - Groupe 2",
            60,
            "Graphics\\Fonts\\Godzilla.ttf",
            "Graphics\\Fonts\\Lemon-Juice.ttf"
        )
        self.screen = pg.display.set_mode((self.Settings.instance.SCREEN_WIDTH, self.Settings.instance.SCREEN_WIDTH))
        pg.display.set_icon(self.Settings.instance.ICON)
        self.clock = pg.time.Clock()
        self.running = True
        self.on_menu = True
        self.on_game = False
        self.on_game_over = False
        self.playing = False
        self.menu = Menu((163, 195, 208), self.Settings, self.screen, self)

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
            self.clock.tick(Settings.instance.FPS)
            self.draw()
            self.fixed_update()
            self.update()
            self.events()

    def update(self):
        # update loop
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
        else:
            self.screen.fill((50, 255, 1))
        pg.display.flip()

    def splash_screen(self):
        """
        Function to displayed a splash screen. According to Wikipedia :
        ''A splash screen is a graphical control element consisting of a window containing an image, a logo,
          and the current version of the software. A splash screen usually appears while a game or program is launching.''
        :return:
        """
        image_fade_in(pg.image.load(path_asset("Graphics\\splash.jpeg")),
                      self.Settings.instance.SCREEN_WIDTH / 3.5,
                      self.Settings.instance.SCREEN_HEIGHT / 2,
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
