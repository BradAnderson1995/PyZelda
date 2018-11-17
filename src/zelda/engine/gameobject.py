import logging
import pygame
import random

LOG = logging.getLogger(__name__)


class ObjectState(object):
    def __init__(self):
        pass

    def update(self, game_object, game_scene):
        pass


class GameObject(pygame.sprite.Sprite, object):
    def __init__(self, image=None, layer=0, masks=None, collision_rect=None, angle=0, position=(0, 0),
                 handle_collisions=False, object_type=None, properties=None, visible=True, persistent=False,
                 tile_id=None, animate=False, animation_speed=15, current_frame=0, sync=False, solid=False,
                 hitbox=None, call_special_update=False):
        pygame.sprite.Sprite.__init__(self)
        self.images = {}
        self.images['image'] = {}
        self.images['image'][0] = []
        if image is None:
            self.images['image'][0].append(pygame.Surface((0, 0)))
        else:
            try:
                len(image)
                self.images['image'][0] = image
            except TypeError:
                self.images['image'][0] = [image]
        self.flipped_hor = False
        self.flipped_ver = False
        self.tinted = None
        self.inverted = False
        self.visible = visible
        self.current_animation = 'image'
        self.animate = animate
        self.animation_frame = current_frame
        self.animation_speed = animation_speed  # How many frames to wait between frames
        self.animation_counter = 0
        self.sync = sync
        self.frame_ready = False
        self.current_image = self.images['image']
        self.current_key = 'image'
        if collision_rect is None:
            self.collision_rect = self.images['image'][0][0].get_rect()
        else:
            self.collision_rect = collision_rect
        if hitbox is None:
            self.hitbox = self.collision_rect
        else:
            self.hitbox = hitbox
        self.rect = self.images['image'][0][0].get_rect()
        self._rect_offset = (0, 0)
        self.rect_offset = (0, 0)
        # self.rect_scaled = self.rect.copy()
        # self.rect_draw = self.images['image'].get_rect()
        self.layer = layer
        self.masks = []
        # self.images['image'] = self.image
        self.angle = angle
        self.scene_position = None
        self.position = position
        self.states = {}
        self._state = None
        self.handle_collisions = handle_collisions
        self.object_type = object_type
        self.persistent = persistent
        self.updated = True
        self.updated_sprite = False
        self.solid = solid
        self.remove = False
        self.call_special_update = call_special_update
        if properties is None:
            self.properties = {}
        else:
            self.properties = properties
            for object_property in properties.keys():
                if object_property == 'solid':
                    # if properties[property] == "True":
                    self.solid = True
                    self.handle_collisions = True
                if object_property == 'handle_collisions':
                    self.handle_collisions = True
                if object_property == 'object_type':
                    self.object_type = properties[object_property]
                if object_property == 'collision_rect':
                    crect_list = map(int, self.properties[object_property].split(','))
                    self.collision_rect = pygame.Rect(crect_list)
                if object_property == 'hitbox':
                    crect_list = map(int, self.properties[object_property].split(','))
                    self.hitbox = pygame.Rect(crect_list)
        self.tile_id = tile_id
        # self.rotate(0)
        if masks is not None:
            for mask in masks:
                self.add_mask(mask)

    def get_global_rect(self):
        return pygame.Rect(self.rect[0] + self.position[0], self.rect[1] + self.position[1], self.rect[2], self.rect[3])

    def get_global_collision_rect(self):
        return pygame.Rect(self.collision_rect[0] + self.position[0], self.collision_rect[1] + self.position[1],
                           self.collision_rect[2], self.collision_rect[3])

    def get_global_hitbox(self):
        return pygame.Rect(self.hitbox[0] + self.position[0], self.hitbox[1] + self.position[1],
                           self.hitbox[2], self.hitbox[3])

    def add_mask(self, mask):
        self.masks.append(mask)

    def remove_mask(self, mask):
        if self.masks.count(mask) != 0:
            while self.masks.remove(mask):
                pass

    def add_image(self, key, surface):
        self.images[key] = {}
        self.images[key][0] = []
        self.images[key][0].append(surface)

    def set_image(self, key):
        self.updated = True
        self.updated_sprite = True
        # self.image = self.images[key]
        self.current_image = self.images[key]
        self.current_key = key
        self.animation_frame = 0
        self.rect = self.images[self.current_key][self.animation_frame][0].get_rect()
        # self.rect = self.current_image[0][0].get_rect()
        # self.rotate(0)

    def remove_image(self, key):
        if key in self.images:
            del self.images[key]

    def add_animation(self, key, image_list):
        self.images[key] = {}
        self.images[key][0] = image_list

    def set_animation_frame(self, frame):
        self.updated = True
        self.updated_sprite = True
        # self.image = self.images[key][frame]
        self.animation_frame = frame
        # self.current_image = self.images[key][frame]
        # self.rotate(0)

    def set_animation(self, key, starting_frame=0):
        self.updated = True
        self.updated_sprite = True
        # self.image = self.images[key][starting_frame]
        self.animation_frame = starting_frame
        self.current_animation = key
        # self.current_image = self.images[key][starting_frame]
        self.current_key = key
        # self.rotate(0)

    def next_frame(self, direction=1):
        self.updated = True
        self.updated_sprite = True
        if direction == -1:
            self.animation_frame -= 1
            if self.animation_frame < 0:
                # self.animation_frame = self.images[self.current_animation].__len__()-1
                self.animation_frame = len(self.images[self.current_animation][0])-1
        else:
            self.animation_frame += 1
            if self.animation_frame > len(self.images[self.current_animation][0])-1:
                self.animation_frame = 0
        if self.animation_frame < len(self.images[self.current_animation][0]):
            # self.image = self.images[self.current_animation][self.animation_frame]
            # self.current_image = self.images[self.current_animation][self.animation_frame]
            # self.rotate(0)
            return True
        else:
            return False

    def move(self, coordinate):
        self.updated = True
        if coordinate is not None:
            self.position = coordinate
            return True
        else:
            return False

    def increment(self, increment):
        return self.move((self.position[0] + increment[0], self.position[1] + increment[1]))

    def destroy(self):
        del self
        return True

    def width(self):
        return self.rect.width

    def height(self):
        return self.rect.height

    def draw(self, surface, (x, y), invert=False, tint=(0, 0, 0), colorkey=None):   # , x_scale, y_scale, x, y):
        # TODO: May need to change image to current_image. Also go through and make sure using right image consistently
        key = (surface.x_scale, surface.y_scale)
        try:
            if (invert and not self.inverted) or (not invert and self.inverted):
                for image in self.images.keys():
                    for size in self.images[image].keys():
                        for frame in xrange(0, len(self.images[image][size])):
                            self.images[image][size][frame] = self.invert_colors(self.images[image][size][frame],
                                                                                 colorkey=colorkey)
                self.inverted = not self.inverted
            # TODO: Make this non destructive
            # if tint is not None and self.tinted != tint:
            #     for image in self.images.keys():
            #         for size in self.images[image].keys():
            #             for frame in xrange(0, len(self.images[image][size])):
            #                 self.images[image][size][frame] = self.tint(self.images[image][size][frame], tint)
            surface.blit(self.tint(self.images[self.current_key][key][self.animation_frame], tint=tint, colorkey=colorkey),
                         (x, y, self.images[self.current_key][key][self.animation_frame].get_width(),
                          self.images[self.current_key][key][self.animation_frame].get_height()))
            # surface.blit(self.images[self.current_key][key][self.animation_frame],
            #          (x, y, self.images[self.current_key][key][self.animation_frame].get_width(),
            #           self.images[self.current_key][key][self.animation_frame].get_height()))
            # if tint != (0, 0, 0, 0):
            #     tint_surface = pygame.Surface(self.images[self.current_key][key][self.animation_frame].get_size())
            #     tint_surface.fill(tint)
            #     surface.blit(tint_surface, (x, y))
        except IndexError:
            LOG.error(
                'Draw error: %s %s',
                self.animation_frame,
                len(self.images[self.current_key][key])
            )
        self.updated = False
        self.updated_sprite = False

    def scale_to_view(self, scaling):
        LOG.debug('Scaling...')
        for image_list in self.images.keys():
            self.images[image_list][scaling] = []
            for image in xrange(0, len(self.images[image_list][0])):
                self.images[image_list][scaling].append(pygame.transform.scale(self.images[image_list][0][image],
                    (int(self.images[image_list][0][image].get_width()*scaling[0]),
                     int(self.images[image_list][0][image].get_height()*scaling[1]))))

    def rotate(self, angle):
        self.angle += angle
        rect = self.rect
        flipped_image = pygame.transform.flip(self.current_image, self.flipped_hor, self.flipped_ver)
        # flipped_image = self.image
        self.image = pygame.transform.rotate(flipped_image, self.angle)
        # self.image = pygame.transform.flip(self.image, self.flipped_hor, self.flipped_ver)
        rect.center = self.image.get_rect().center
        self.rect = rect

    # Rotates about center, clipping to original width and height
    # Don't use this, doesn't work
    def rotate_clip(self, angle):
        """rotate an image while keeping its center and size"""
        self.angle += angle
        rect = self.rect
        self.image = pygame.transform.rotate(self.current_image, self.angle)
        rect.center = self.image.get_rect().center
        self.image = self.image.subsurface(rect).copy()

    def flip(self, flip_hor, flip_ver):
        if flip_hor:
            self.flipped_hor = not self.flipped_hor
        if flip_ver:
            self.flipped_ver = not self.flipped_ver
        self.rotate(0)

    @staticmethod
    def tint(input_surface, tint, colorkey=None):
        if tint == (0, 0, 0) or tint == (0, 0, 0, 0):
            return input_surface
        else:
            surface = input_surface.copy()
            tint_surface = pygame.Surface((surface.get_width(), surface.get_height()))
            tint_surface.fill(tint)
            surface.blit(tint_surface, (0, 0))
        # else:
        #     surface = input_surface.copy()
        #     surface.lock()
        #     for x in range(0, surface.get_width()):
        #         for y in range(0, surface.get_height()):
        #             pixel = surface.get_at((x, y))
        #             if pixel != colorkey:
        #                 new_r = pixel.r + tint[0]
        #                 if new_r > 255:
        #                     new_r = 255
        #                 elif new_r < 0:
        #                     new_r = 0
        #                 new_g = pixel.g + tint[1]
        #                 if new_g > 255:
        #                     new_g = 255
        #                 elif new_g < 0:
        #                     new_g = 0
        #                 new_b = pixel.b + tint[2]
        #                 if new_b > 255:
        #                     new_b = 255
        #                 elif new_b < 0:
        #                     new_b = 0
        #                 new_a = pixel.a
        #                 if len(tint) == 4:
        #                     new_a = pixel.a + tint[3]
        #                     if new_a > 255:
        #                         new_a = 255
        #                     elif new_a < 0:
        #                         new_a = 0
        #                 surface.set_at((x, y), (new_r, new_g, new_b, new_a))
        #     surface.unlock()
            return surface

    @staticmethod
    def invert_colors(input_surface, colorkey=(0, 0, 0)):
        surface = input_surface.copy()
        surface.lock()
        for x in range(0, surface.get_width()):
            for y in range(0, surface.get_height()):
                pixel = surface.get_at((x, y))
                if pixel != colorkey:
                    new_r = 255 - pixel.r
                    new_g = 255 - pixel.g
                    new_b = 255 - pixel.b
                    a = pixel.a
                    surface.set_at((x, y), (new_r, new_g, new_b, a))
        surface.unlock()
        return surface

    @staticmethod
    def bloom(input_surface, colorkey=(0, 0, 0)):
        surface = input_surface.copy()
        surface.lock()
        for x in range(0, surface.get_width()):
            for y in range(0, surface.get_height()):
                pixel = surface.get_at((x, y))
                if pixel != colorkey:
                    new_r = 2*pixel.r
                    new_g = 2*pixel.g
                    new_b = 2*pixel.b
                    if new_r > 255:
                        new_r = 255
                    if new_g > 255:
                        new_g = 255
                    if new_b > 255:
                        new_b = 255
                    a = pixel.a
                    surface.set_at((x, y), (new_r, new_g, new_b, a))
        surface.unlock()
        return surface

    @staticmethod
    def gauss(input_surface, colorkey):
        surface = input_surface.copy()
        surface.lock()
        for x in range(0, surface.get_width()):
            for y in range(0, surface.get_height()):
                pixel = surface.get_at((x, y))
                if pixel != colorkey:
                    arg1 = 30
                    arg2 = 150
                    # new_r = pixel.r + random.randrange(-pixel.r, 255 - pixel.r, 1)
                    # new_g = pixel.g + random.randrange(-pixel.g, 255 - pixel.g, 1)
                    # new_b = pixel.b + random.randrange(-pixel.b, 255 - pixel.b, 1)
                    new_r = pixel.r + random.gauss(arg1, arg2)
                    new_g = pixel.g + random.gauss(arg1, arg2)
                    new_b = pixel.b + random.gauss(arg1, arg2)
                    if new_r > 255:
                        new_r = 255
                    elif new_r < 0:
                        new_r = 0
                    if new_g > 255:
                        new_g = 255
                    elif new_g < 0:
                        new_g = 0
                    if new_b > 255:
                        new_b = 255
                    elif new_b < 0:
                        new_b = 0
                    a = pixel.a
                    surface.set_at((x, y), (new_r, new_g, new_b, a))
        surface.unlock()
        return surface

    def update(self, can_update=True, rewind=False, direction=1):
        if self._state is not None:
            # self._state.update(self)
            pass
        if self.animation_speed > 0:
            if not rewind:
                self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.frame_ready = True
            if self.frame_ready and can_update:
                if not rewind:
                    self.next_frame(direction)
                    self.animation_counter = 0
            if self.frame_ready:
                self.animation_counter = 0
                self.frame_ready = False
                return True
            else:
                return False
