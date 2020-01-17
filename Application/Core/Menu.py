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
        self.credits = "(c) ESGI 2020  -  Developpers : Lior DILER, Tom RAKOTOMANAMPISON, Antoine PAVY | "\
                       "Graphic artist : Antoine PAVY  | " \
                       'Musics : Tom RAKOTOMANAMPISON  | '

    def draw(self):
        self.screen.fill(self.background_color)
        draw_text(self.Settings.instance.TITLE_GAME,
                  100,
                  (231,156,73),
                  self.Settings.instance.SCREEN_WIDTH / 2,
                  self.Settings.instance.SCREEN_HEIGHT / 4,
                  self.Settings.instance.FONT_TITLE,
                  self.screen
                  )

        draw_text("Press start",
                  50,
                  (231,156,73),
                  self.Settings.instance.SCREEN_WIDTH / 2,
                  self.Settings.instance.SCREEN_HEIGHT/2,
                  self.Settings.instance.FONT_TEXT,
                  self.screen
                  )

        draw_text(self.credits,
                  25,
                  (0, 0, 0),
                  self.Settings.instance.SCREEN_WIDTH / 2,
                  self.Settings.instance.SCREEN_HEIGHT /1.1,
                  self.Settings.instance.FONT_TEXT,
                  self.screen
                  )
        pg.display.flip()

    def events(self):
        press_key(self.app)




