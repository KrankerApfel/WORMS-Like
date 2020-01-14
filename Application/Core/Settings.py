import os
import pygame as pg


# --- OS compatibility function ---
def path_asset(path):
    return os.path.join('Assets', path)


class Settings:
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
            self.TITLE_GAME = title_game
            self.FONT_TEXT = path_asset(font_text_file_path)

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
