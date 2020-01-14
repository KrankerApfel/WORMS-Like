import pygame as pg
class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((1200, 600))
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = False

    def new(self): pass

    def run(self):
        # main loop
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.fixed_update()
            self.update()
            self.draw()

    def update(self):
        # update loop
        pass

    def fixed_update(self):
        # physic update loop
        pass

    def events(self):
        # Input events handler loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
        pass

    def draw(self):
        # display loop
        pg.display.flip()

    def show_splashscreen(self): pass

    def menu(self): pass

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def fadeout_img(self, image, x, y, delay, background):
        self.screen.fill(background)
        self.screen.blit(image, (x, y))
        pg.time.delay(delay)
        pg.display.flip()

    def quit(self):
        self.playing = False
        self.running = False
        pg.mixer.quit()
        pg.quit()
