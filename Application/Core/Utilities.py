import pygame as pg
import os


# --- OS compatibility function ---
def path_asset(path):
    return os.path.join('Assets', path)


def draw_text(text, size, color, x, y, font_name, screen):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def fadeout_img(image, x, y, delay, background, screen):
    screen.fill(background)
    screen.blit(image, (x, y))
    pg.time.delay(delay)
    pg.display.flip()


def press_key(app):
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
                app.quit()
            if event.type == pg.KEYUP:
                waiting = False


def draw_button(button, screen):
    pg.draw.rect(screen, button['color'], button['rect'])
    screen.blit(button['text'], button['text rect'])


def create_button(x, y, w, h, text, callback, settings, color=(255, 255, 255)):
    font = pg.font.Font(settings.instance.FONT_TEXT, 20)
    text_surf = font.render(text, True, (255, 0, 0))
    button_rect = pg.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': color,
        'callback': callback,
    }
    return button
