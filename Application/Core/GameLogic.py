from Application.Core.Settings import *
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
        self.playing = False

    def new(self):
        self.run()
        pass

    def run(self):
        # main loop
        self.playing = True
        while self.playing:
            self.clock.tick(Settings.instance.FPS)
            self.events()
            self.fixed_update()
            self.update()
            self.draw()

    def update(self):
        # update loop
        pass

    def fixed_update(self):
        # physic update loop
        pass

    def events(self):
        # Input events handler loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
        pass

    def draw(self):
        # display loop
        self.screen.fill((50,255,1))
        pg.display.flip()

    def show_splashscreen(self):
        pass

    def menu(self):
        self.screen.fill((5,5,30))
        draw_text(self.Settings.instance.TITLE_GAME,
                       40,
                       (255,255,255),
                       self.Settings.instance.SCREEN_WIDTH / 2,
                       self.Settings.instance.SCREEN_WIDTH / 4,
                       self.Settings.instance.FONT_TITLE,
                       self.screen
                  )

        draw_text("Presse start",
                       18,
                       (255, 255, 255),
                       self.Settings.instance.SCREEN_WIDTH / 2,
                       self.Settings.instance.SCREEN_WIDTH / 2,
                       self.Settings.instance.FONT_TEXT,
                       self.screen
                  )

        pg.display.flip()
        press_key(self)
        self.new()



    def quit(self):
        self.playing = False
        self.running = False
        pg.mixer.quit()
        pg.quit()