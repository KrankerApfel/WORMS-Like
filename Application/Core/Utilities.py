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
    # Continue apres avoir presser une touche
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
                app.quit()
            if event.type == pg.KEYUP:
                waiting = False
