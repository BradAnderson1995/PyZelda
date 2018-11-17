import pygame
import pyaudio
import backend
from ctypes import *
from contextlib import contextmanager

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)


class ResourceManager(object):
    def __init__(self, force_pygame=True, force_pyaudio=True, muted=False):
        pygame.font.init()
        # pygame.mixer.init()
        self.sprites = {}
        self.music = {}
        self.sounds = {}
        self.fonts = {}
        self.force_pygame = force_pygame
        self.force_pyaudio = force_pyaudio
        self.muted = muted
        self.current_key = None
        with noalsaerr():
            self.pya = pyaudio.PyAudio()
        self.sound_channels = 4
        self.current_sounds = [backend.Sound(self.pya) for x in xrange(self.sound_channels)]
        self.sound_queue_index = 0

    def add_image(self, key, image):
        self.sprites[key] = image

    def add_image_list(self, key, images):
        self.sprites[key] = images

    def add_image_file(self, key, filename):
        try:
            self.sprites[key] = pygame.image.load(filename).convert_alpha()
            return True
        except:
            return False

    def remove_image(self, key):
        del self.sprites[key]

    def add_image_file_list(self, key, filenames):
        self.sprites[key] = []
        for filename in filenames:
            try:
                self.sprites[key].append(pygame.image.load(filename).convert_alpha())
            except:
                pass

    def add_spritesheet_image(self, key, spritesheet, rectangle, colorkey=None):
        self.sprites[key] = spritesheet.image_at(rectangle, colorkey)

    def add_spritesheet_image_list(self, key, spritesheet, rectangle_list, colorkey=None):
        self.sprites[key] = spritesheet.images_at(rectangle_list, colorkey)

    def add_spritesheet_strip(self, key, spritesheet, rect, image_count, colorkey=None):
        self.sprites[key] = spritesheet.load_strip(rect, image_count, colorkey)

    def add_spritesheet_strip_offsets(self, key, spritesheet, topleft, image_count, per_line, image_size, hor_offset,
                                      ver_offset, colorkey=None):
        self.sprites[key] = spritesheet.load_strip_offsets(topleft, image_count, per_line, image_size, hor_offset,
                                                           ver_offset, colorkey)

    def get_images(self, key):
        return self.sprites[key]

    def add_font(self, key, filename, size):
        self.fonts[key] = pygame.font.Font(filename, size)

    def remove_font(self, key):
        del self.fonts[key]

    def add_music(self, key, filename):
        # if pyglet.media.have_avbin and not self.force_pygame:
        #     self.music[key] = pyglet.media.load(filename)
        if self.force_pyaudio:
            self.music[key] = backend.SoundStream(self.pya, filename)
        else:
            self.music[key] = filename

    def remove_music(self, key):
        del self.music[key]

    def play_music(self, key, start=0):
        if not self.muted:
            # if pyglet.media.have_avbin and not self.force_pygame:
            #     self.music[key].play()
            if self.force_pyaudio:
                if self.current_key is not None:
                    self.music[self.current_key].stop()
                self.music[key].play()
                self.current_key = key
            else:
                pygame.mixer.music.load(self.music[key])
                pygame.mixer.music.play(-1)
        # pygame.mixer.music.set_pos(start)
        # if pyglet.media.have_avbin and not self.force_pygame:
        #     self.music[key].play()

    def add_sound(self, key, filename):
        # if pyglet.media.have_avbin and not self.force_pygame:
        #     self.sounds[key] = pyglet.media.load(filename, streaming=False)
        if self.force_pyaudio:
            self.sounds[key] = backend.WaveFile(filename)
        else:
            self.sounds[key] = pygame.mixer.Sound(filename)
        # pass

    def remove_sound(self, key):
        del self.sounds[key]

    def play_sound(self, key):
        if not self.muted:
            if self.force_pyaudio:
                self.current_sounds[self.sound_queue_index].play(self.sounds[key])
                self.sound_queue_index += 1
                if self.sound_queue_index > self.sound_channels - 1:
                    self.sound_queue_index = 0
            else:
                self.sounds[key].play()
            # self.current_sounds.append(self.sounds[key])

    def update_sound(self):
        if self.current_key is not None:
            if self.force_pyaudio:
                if self.current_key is not None:
                    self.music[self.current_key].update()
