from Application.Core.Settings import *
from Application.Core.Menu import *
from Application.Core.Utilities import draw_text, fadeout_img, press_key
import pygame as pg


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.Settings = Settings(
            "WORMS Motherfuckers !",
            1200,
            600,
            "Graphics/icon.png",
            "WORMS Like - Groupe 2",
            60,
            "Graphics/Fonts/Godzilla.ttf",
            "Graphics/Fonts/Lemon-Juice.ttf"
        )
        self.screen = pg.display.set_mode((self.Settings.instance.SCREEN_WIDTH, self.Settings.instance.SCREEN_WIDTH))
        pg.display.set_icon(self.Settings.instance.ICON)
        self.clock = pg.time.Clock()
        self.running = True
        self.on_menu = True
        self.playing = False
        self.menu = Menu((163, 195, 208), self.Settings, self.screen, self)

    def new(self):
        self.run()
        pass

    def run(self):
        # main loop
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
        # Input events handler loop
        if self.on_menu:
            self.menu.events()
            self.on_menu = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    def draw(self):
        # display loop
        if self.on_menu:
            self.menu.draw()
        else:
            self.screen.fill((50, 255, 1))
        pg.display.flip()

    def show_splashscreen(self):
        pass

    def quit(self):
        self.on_menu = False
        self.playing = False
        self.running = False
        pg.mixer.quit()
        pg.quit()
