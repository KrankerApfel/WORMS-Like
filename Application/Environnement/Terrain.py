import pygame as pg
from Application.Core.Utilities import path_asset


class Ground(pg.sprite.Sprite):
    """
    This class is a destructible ground representation.
    It displayed the image indicate by the path passed in arguments, but doesn't blit
    the black color. The collision mask correspond to the visible part, namely all colors
    that are not black.

    :param image_path: the path to the ground image.
    :type image_path: str
    """
    def __init__(self, image_path):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(path_asset(image_path))
        # an image can have only one color key, it's the rgb code of the not rendered color.
        self.image.set_colorkey((0, 0, 0))
        # set a rect may be  mandatory to check collision between pg.srite
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.mask = pg.mask.from_surface(self.image)

    def update_mask(self, hole_radius, hole_position):
        """
        This function update the collision and the rendering mask with a hole at the position
        the terrain is destroyed.
        :param hole_radius: the radius of the hole
        :param hole_position: the position of the hole
        """
        new_img = self.image.copy()
        pg.draw.circle(new_img, (0, 0, 0), hole_position, hole_radius)
        self.image = new_img
        self.mask = pg.mask.from_surface(self.image)

    def draw(self, screen):
        """
        This function display the ground on screen.
        :param screen: the screen that displayed the ground
        """
        screen.blit(self.image, (0, 0))

    def __repr__(self):
        return "Ground"
