from Application.Core.Utilities import draw_text, create_button, draw_button
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
        self.buttons = [
            create_button(
                self.Settings.instance.SCREEN_WIDTH / 3,
                self.Settings.instance.SCREEN_HEIGHT / 1.5,
                self.Settings.instance.SCREEN_WIDTH / 15,
                self.Settings.instance.SCREEN_HEIGHT / 12,
                "nb players : +/-",
                lambda e: self.add_player(e),
                self.Settings),

            create_button(
                self.Settings.instance.SCREEN_WIDTH / 1.8,
                self.Settings.instance.SCREEN_HEIGHT / 1.5,
                self.Settings.instance.SCREEN_WIDTH / 15,
                self.Settings.instance.SCREEN_HEIGHT / 12,
                "nb worms +/-",
                lambda e: self.add_worms(e),
                self.Settings)

        ]

        self._party_data = {'players_number': 2,
                            'worms_number': 1}
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

        list(map(lambda btn: draw_button(btn, self.screen), self.buttons))

        draw_text("Players : " + str(self._party_data['players_number']),
                  25,
                  (0, 0, 0),
                  self.Settings.instance.SCREEN_WIDTH / 2.5,
                  self.Settings.instance.SCREEN_HEIGHT / 1.2,
                  self.Settings.instance.FONT_TEXT,
                  self.screen
                  )

        draw_text("Worms : " + str(self._party_data['worms_number']),
                  25,
                  (0, 0, 0),
                  self.Settings.instance.SCREEN_WIDTH / 2,
                  self.Settings.instance.SCREEN_HEIGHT / 1.2,
                  self.Settings.instance.FONT_TEXT,
                  self.screen
                  )

        pg.display.flip()

    def events(self):

        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.app.quit()

                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    waiting = not (self._party_data['players_number'] > 1) or not (self._party_data['worms_number'] > 0)

                if event.type == pg.MOUSEBUTTONDOWN:
                    for btn in self.buttons:
                        if btn['rect'].collidepoint(event.pos):
                            btn['callback'](event.button)

    def add_player(self, event_button):
        if event_button == 1:
            self._party_data['players_number'] += 1 if self._party_data['players_number'] < 4 else 0
        elif event_button == 3:
            self._party_data['players_number'] -= 1 if self._party_data['players_number'] > 2 else 0

        self.draw()

    def add_worms(self, event_button):
        if event_button == 1:
            self._party_data['worms_number'] += 1 if self._party_data['worms_number'] < 4 else 0
        elif event_button == 3:
            self._party_data['worms_number'] -= 1 if self._party_data['worms_number'] > 1 else 0

        self.draw()
