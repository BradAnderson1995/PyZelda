import os
import random
from zelda import engine
from zelda import SPRITE_DIR


class AbstractEffect(engine.GameObject):
    def __init__(self, object_type):
        self.resource_manager = engine.ResourceManager()
        effect_path = os.path.join(SPRITE_DIR, 'Effects.png')
        self.effect_sheet = engine.Spritesheet(effect_path)
        engine.GameObject.__init__(self, layer=100, object_type=object_type)
        self.animation_speed = 15


class AbstractShortGrass(AbstractEffect):
    def __init__(self, object_type):
        AbstractEffect.__init__(self, object_type)
        self.direction = 1

    def update(self, can_update=True, rewind=False, direction=1):
        previous_frame = self.animation_frame
        engine.GameObject.update(self, direction=self.direction)
        if self.animation_frame != previous_frame:
            self.direction = random.choice([1, -1])


class ShortGrass(AbstractShortGrass):
    def __init__(self):
        AbstractShortGrass.__init__(self, 'effect_short_grass')
        self.resource_manager.add_spritesheet_strip_offsets('effect_short_grass', self.effect_sheet,
                                                            (0, 0), 3, 3, (16, 16), 0, 0, (64, 64, 192))
        self.add_animation('image', self.resource_manager.get_images('effect_short_grass'))
        self.set_animation('image', 0)


class ShortForestGrass(AbstractShortGrass):
    def __init__(self):
        AbstractShortGrass.__init__(self, 'effect_short_forest_grass')
        self.resource_manager.add_spritesheet_strip_offsets('effect_short_forest_grass', self.effect_sheet,
                                                            (0, 16), 3, 3, (16, 16), 0, 0, (64, 64, 192))
        self.add_animation('image', self.resource_manager.get_images('effect_short_forest_grass'))
        self.set_animation('image', 0)


class CutGrass(AbstractEffect):
    def __init__(self):
        AbstractEffect.__init__(self, 'effect_cut_grass')
        self.resource_manager.add_spritesheet_strip_offsets('effect_cut_grass', self.effect_sheet,
                                                            (0, 32), 8, 8, (32, 32), 0, 0, (64, 64, 192))
        self.add_animation('image', self.resource_manager.get_images('effect_cut_grass'))
        self.set_animation('image', 0)
        self.animation_speed = 2
        self.animate = True

    def update(self, can_update=True, rewind=False, direction=1):
        if self.animation_frame == 7:
            self.remove = True
        else:
            engine.GameObject.update(self)
