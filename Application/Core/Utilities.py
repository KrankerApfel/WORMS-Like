import pygame as pg
import os


# --- OS compatibility function --
def path_asset(path):
    """A function to access assets folder without broke os compatibility.
       Indeed, os don't used the same path conventions."""
    return os.path.join('Assets', path)


# --- graphics manipulation ---
def draw_text(text, size, color, x, y, font_path, screen):
    """
    A function to simply draw text on a screen.
    :param text: the displaying text.
    :type text: str
    :param size: the font size.
    :type size: int
    :param color: the RGB code tuple for text color as (r,g,b).
    :type color: tuple.
    :param x: The text center  x position.
    :type x: int
    :param y: The text center y position.
    :type y: int
    :param font_path: the font file path
    :type font_path: str
    :param screen: the screen where the text is written
    :type screen: Pygame.Surface
    :return: void
    """
    font = pg.font.Font(font_path, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def image_fade_in(image, x, y, factor, background, screen):
    """
    A function to applied a fade in on an image.

    :param image: The image to fade in. It must be alpha convertible !
    :type image: Pygame.image
    :param x: The top left corner image x position.
    :type x: int
    :param y: The top left corner image y position.
    :type y: int
    :param factor: The number of iteration per framerate
    :type factor: int
    :param background: The RGB code tuple of the background color during the animation as (r,g,b)
    :type background: Tuple
    :param screen: the screen where the animation is displaying
    :type screen: Pygame.Surface
    :return:
    """
    i = 0
    # convert image to be able to set alpha canal
    image = image.convert()
    b = True
    while b:
        screen.fill(background)
        # change transparency with alpha canal
        image.set_alpha(i)
        # draw image on screen at (x,y) coordinates
        screen.blit(image, (x, y))
        # refresh screen
        pg.display.flip()
        # increment i according to the choose factor
        # 800 is the animation time duration in milliseconds
        i += factor / 800
        b = (i < 800)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()


# --- events utilities ---
def press_key(app):
    """
    A function to waiting for a key pressed action before continue
    :param app: the application it stop
    :return: void
    """
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
                app.quit()
            if event.type == pg.KEYUP:
                waiting = False


def draw_button(button, screen):
    """
    A function to draw a callable button on screen.

    :param button: The callable button
    :type button: dict
    :param screen: the screen where the button is drawn
    :type screen: Pygame.Surface
    :return: void
    """
    pg.draw.rect(screen, button['color'], button['rect'])
    screen.blit(button['text'], button['text rect'])


def create_button(x, y, w, h, text, callback, settings, btn_color=(255, 255, 255), text_color=(255, 0, 0),
                  font_size=20):
    """
    A function to create a callable button thanks to a dictionary structure.

    :param x: The button top left corner x position.
    :type x: int
    :param y: The button top left corner y position.
    :type y: int
    :param w: The button width
    :type w: int
    :param h: The button height
    :type h: int
    :param text: The text displayed on the button
    :type text: str
    :param callback: The function call when the button is clicking
    :param settings: The singleton that contains game parameters
    :type settings: Application.Core.Settings
    :param btn_color: The RGB code of the button color
    :type btn_color: tuple
    :param text_color: The RGB code of the text color
    :type text_color: tuple
    :param font_size: The text font size
    :type font_size: int
    :return: void
    """
    font = pg.font.Font(settings.instance.FONT_TEXT, font_size)
    text_surf = font.render(text, True, text_color)
    button_rect = pg.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': btn_color,
        'callback': callback,
    }
    return button
