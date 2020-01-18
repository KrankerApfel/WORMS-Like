from Application.Core.Utilities import path_asset
import pygame as pg


class Settings:
    """"
    A singleton to manage game settings. It contain only one instance that have to be called to used
    his fields.

    :Example:

    Settings = Settings(*param) # call the constructor
    screen_width = Settings.instance.SCREEN_WIDTH # use instance to access to settings fields.

    :param title_game: The game title
    :type title_game: str
    :param screen_width: The screen width
    :type screen_width: int
    :param screen_height: The screen height
    :type screen_height: int
    :param icon_file_path: The path to the window title bar icon file
    :type icon_file_path: str
    :param window_caption: The text caption displayed on window title bar
    :type window_caption: str
    :param fps: The game frame per second
    :type fps: int
    :param font_title_file_path: The path to the title font file
    :type font_title_file_path: str
    :param font_text_file_path: The path to the text font file
    :type font_text_file_path: str
    """
    class __SettingsSingleton:
        def __init__(self, title_game, screen_width, screen_height, icon_file_path, window_caption, fps,
                     font_title_file_path,
                     font_text_file_path):
            self.SCREEN_WIDTH = screen_width
            self.SCREEN_HEIGHT = screen_height
            self.ICON = pg.image.load(path_asset(icon_file_path))
            self.WINDOW_CAPTION = window_caption
            self.FPS = fps
            self.FONT_TITLE = path_asset(font_title_file_path)
            self.FONT_TEXT = path_asset(font_text_file_path)
            self.TITLE_GAME = title_game

        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self, title_game, screen_width, screen_height, icon_file_path, window_caption, fps,
                 font_title_file_path,
                 font_text_file_path):
        if not Settings.instance:
            Settings.instance = Settings.__SettingsSingleton(title_game, screen_width, screen_height, icon_file_path,
                                                             window_caption,
                                                             fps, font_title_file_path, font_text_file_path)
        else:
            Settings.instance.TITLE_GAME = title_game
            Settings.instance.SCREEN_WIDTH = screen_width
            Settings.instance.SCREEN_HEIGHT = screen_height
            Settings.instance.ICON = path_asset(icon_file_path)
            Settings.instance.WINDOW_CAPTION = window_caption
            Settings.instance.FPS = fps
            Settings.instance.FONT_TITLE = path_asset(font_title_file_path)
            Settings.instance.FONT_TEXT = path_asset(font_text_file_path)

    def __getattr__(self, name):
        return getattr(self.instance, name)
