import os
from zelda import engine, SPRITE_DIR


class AbstractTile(engine.GameObject):
    def __init__(self):
        self.resource_manager = engine.ResourceManager()
        self.tile_sheet = engine.Spritesheet(os.path.join(
            SPRITE_DIR,
            'OverworldSheet.png'
        ))


class ShortGrass(AbstractTile):
    def __init__(self, resource_manager):
        AbstractTile.__init__(self)
        engine.GameObject.__init__(self, self.resource_manager.get_images('overworld_tiles')[229],
                                   layer=-500, handle_collisions=True, object_type='short_grass')


class BigBeachGrass(engine.GameObject):
    def __init__(self, resource_manager):
        engine.GameObject.__init__(self, resource_manager.get_images('overworld_tiles')[254],
                                   layer=-500, handle_collisions=True, object_type='big_beach_grass')


class Hole(engine.GameObject):
    def __init__(self, resource_manager):
        engine.GameObject.__init__(self, resource_manager.get_images('overworld_tiles')[232],
                                   layer=-500, handle_collisions=True, object_type='big_beach_grass', solid=True)


class GroundTile(AbstractTile):
    def __init__(self, resource_manager):
        engine.GameObject.__init__(self, resource_manager.get_images('overworld_tiles')[220],
                                   layer=-1000, handle_collisions=False)
