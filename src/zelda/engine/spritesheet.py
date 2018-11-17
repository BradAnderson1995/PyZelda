import pygame


class Spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit(message)

    # Load image at location
    def image_at(self, rectangle, colorkey=None):
        """Loads image from x, y, x+offset, y+offset"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a list of images
    def images_at(self, rectangle_list, colorkey=None):
        return [self.image_at(rectangle, colorkey) for rectangle in rectangle_list]

    # Load a strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        rectangle_list = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.images_at(rectangle_list, colorkey)

    # Load a stip of images with offsets
    def load_strip_offsets(self, topleft, image_count, per_line, image_size, hor_offset=0, ver_offset=0, colorkey=None):
        rectangle_list = []
        lines = int(image_count / per_line)
        # even_lines = True
        # if image_count % per_line != 0:
        #     even_lines = False
        current_topleft = topleft
        for line in xrange(0, lines):
            for image in xrange(0, per_line):
                rectangle_list.append(pygame.Rect(current_topleft, (image_size[0], image_size[1])))
                current_topleft = (current_topleft[0] + image_size[0] + hor_offset, current_topleft[1])
            current_topleft = (topleft[0], current_topleft[1] + image_size[1] + ver_offset)
        return self.images_at(rectangle_list, colorkey)
