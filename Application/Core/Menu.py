from Application.Core.Utilities import draw_text, create_button, draw_button
import pygame as pg


class Menu:
    """
    This is the title screen menu class.
    It manage menu display and handles button event.
    It also set data to the incoming game part.

    :param background_color: The background menu color RGB code.
    :type background_color: A tuple filled with RGB value as (r,g,b).
    :param settings: The singleton used to set games parameters
    :type settings: :class:`Application.Core.Settings`
    :param screen: The screen the menu belows
    :type screen: :class:`Pygame.Surface`
    :param app: The game the menu belows
    :type app: Application.Core.Game
    :param party_data: A dictionary containing data to the incoming game part as players number and worms per player.
    :type party_data: dict
    """
    @property
    def game_part_data(self):
        return self._game_part_data

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

        self._game_part_data = {'players_number': 2,
                            'worms_number': 1}
        self.credits = "(c) ESGI 2020  -  Developpers : Lior DILER, Tom RAKOTOMANAMPISON, Antoine PAVY | " \
                       "Graphic artist : Antoine PAVY  | " \
                       'Musics : Tom RAKOTOMANAMPISON  | '

    def draw(self):
        """
        Function to display menu
        :return: void
        """
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

        # call draw_button() for every buttons in self.buttons
        list(map(lambda btn: draw_button(btn, self.screen), self.buttons))

        draw_text("Players : " + str(self._game_part_data['players_number']),
                  25,
                  (0, 0, 0),
                  self.Settings.instance.SCREEN_WIDTH / 2.5,
                  self.Settings.instance.SCREEN_HEIGHT / 1.2,
                  self.Settings.instance.FONT_TEXT,
                  self.screen
                  )

        draw_text("Worms : " + str(self._game_part_data['worms_number']),
                  25,
                  (0, 0, 0),
                  self.Settings.instance.SCREEN_WIDTH / 2,
                  self.Settings.instance.SCREEN_HEIGHT / 1.2,
                  self.Settings.instance.FONT_TEXT,
                  self.screen
                  )

        pg.display.flip()

    def events(self):
        """
        Function to handle events
        :return: void
        """

        waiting = True
        while waiting:
            for event in pg.event.get():
                # check quit event, if you forget it, this loop will prevent quitting
                # even if something similar is already write in a loop that including this menu,
                # because of this 'waiting' loop !!
                if event.type == pg.QUIT:
                    waiting = False
                    self.app.quit()

                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    # check if players and worms numbers are valid
                    waiting = not (self._game_part_data['players_number'] > 1) or not (self._game_part_data['worms_number'] > 0)

                if event.type == pg.MOUSEBUTTONDOWN:
                    # buttons listener, it handle callback if the mouse position collide a button rect.
                    for btn in self.buttons:
                        if btn['rect'].collidepoint(event.pos):
                            btn['callback'](event.button)

    def add_player(self, event_button):
        """
        Function to add or remove a player into the incoming game part data according to the event.
        If it's a left click, it add a player. If it's a right click it will remove one.
        :param event_button: the button event value.
        :return: void
        """
        if event_button == 1:
            self._game_part_data['players_number'] += 1 if self._game_part_data['players_number'] < 4 else 0
        elif event_button == 3:
            self._game_part_data['players_number'] -= 1 if self._game_part_data['players_number'] > 2 else 0

        self.draw()

    def add_worms(self, event_button):
        """
        Function to increment or decrement worms by player for the incoming game part data according to the event.
        If it's a left click, it add a worms. If it's a right click it will remove one.
        :param event_button:  the button event value.
        :return: void
        """
        if event_button == 1:
            self._game_part_data['worms_number'] += 1 if self._game_part_data['worms_number'] < 4 else 0
        elif event_button == 3:
            self._game_part_data['worms_number'] -= 1 if self._game_part_data['worms_number'] > 1 else 0

        self.draw()
