from Application.Entities.Weapons import *
from Application.Core.Utilities import path_asset
background = pg.image.load(path_asset("Graphics\\Backgrounds\\BKG_theme_1.png"))

screen = pg.display.set_mode((1024, 600))
run = True
f = Frag(10, (600, 450), -0.5, 10, 10)

group = pg.sprite.Group(f)
group.add(Bazooka(10, (650, 300), -0.5, 10, 10))
group.add(f.target)
while run:
    group.update()
    screen.blit(background, (0, 0))
    group.draw(screen)
    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

