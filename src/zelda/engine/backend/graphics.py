import pygame


class Surface(pygame.Surface):
    def __init__(self, (width, height), flags=0):
        surface_flags = {0: 0, 1: pygame.SRCALPHA, 2: pygame.HWSURFACE, 3: pygame.SRCALPHA | pygame.HWSURFACE}
        pygame.Surface.__init__(self, (width, height), flags=surface_flags[flags])
