from Application.Core.Utilities import draw_text, press_key, create_button, draw_button
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
        self.button_increment_players = create_button(
            self.Settings.instance.SCREEN_WIDTH / 4,
            self.Settings.instance.SCREEN_HEIGHT / 1.5,
            self.Settings.instance.SCREEN_WIDTH / 15,
            self.Settings.instance.SCREEN_HEIGHT / 12,
            "+/-",
            lambda nb : self.add_player(nb),
            self.Settings)

        self._party_data = {'players_list': [],
                            'worms_number': 0}
        self.credits = "(c) ESGI 2020  -  Developpers : Lior DILER, Tom RAKOTOMANAMPISON, Antoine PAVY | " \
                       "Graphic artist : Antoine PAVY  | " \
                       'Musics : Tom RAKOTOMANAMPISON  | '

    def draw(self):
        self.screen.fill(self.background_color)
        draw_text(self.Settings.instance.TITLE_GAME,
                  100,
                  (231, 156, 73),
                  self.Settings.instance.SCREEN_WIDTH / 2,
                  self.Settings.instance.SCREEN_HEIGHT / 4,
                  self.Settings.instance.FONT_TITLE,
                  self.screen
                  )

        draw_text("Press start",
                  50,
                  (231, 156, 73),
                  self.Settings.instance.SCREEN_WIDTH / 2,
                  self.Settings.instance.SCREEN_HEIGHT / 2,
                  self.Settings.instance.FONT_TEXT,
                  self.screen
                  )

        draw_text(self.credits,
                  25,
                  (0, 0, 0),
                  self.Settings.instance.SCREEN_WIDTH / 2,
                  self.Settings.instance.SCREEN_WIDTH / 2,
                  self.Settings.instance.FONT_TEXT,
                  self.screen
                  )

        draw_button(self.button_increment_players, self.screen)
        pg.display.flip()

    def events(self):

        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.app.quit()
                if event.type == pg.K_RETURN :
                    waiting = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    # 1 is the left mouse button, 2 is middle, 3 is right.
                    if event.button == 1:
                        if self.button_increment_players['rect'].collidepoint(event.pos):
                            self.button_increment_players['callback'](1)
                    if event.button == 3:
                        if self.button_increment_players['rect'].collidepoint(event.pos):
                            self.button_increment_players['callback'](-1)


    def add_player(self, nb):
        print("add something " + str(nb))