from Application.Core.Utilities import draw_text, press_key
import pygame as pg


class Menu:

    @property
    def party_data(self):
        return self._party_data

    def __init__(self, background_color, settings, screen, app):
        self.background_color = background_color
        self.Settings = settings
        self.screen = screen
        self.app = app
        self._party_data = {'players_list': [],
                           'worms_number': 0}

    def draw(self):
        self.screen.fill(self.background_color)
        draw_text(self.Settings.instance.TITLE_GAME,
                  40,
                  (255, 255, 255),
                  self.Settings.instance.SCREEN_WIDTH / 2,
                  self.Settings.instance.SCREEN_WIDTH / 4,
                  self.Settings.instance.FONT_TITLE,
                  self.screen
                  )

        draw_text("Press start",
                  18,
                  (255, 255, 255),
                  self.Settings.instance.SCREEN_WIDTH / 2,
                  self.Settings.instance.SCREEN_WIDTH / 2,
                  self.Settings.instance.FONT_TEXT,
                  self.screen
                  )
        pg.display.flip()

    def events(self):
        press_key(self.app)




