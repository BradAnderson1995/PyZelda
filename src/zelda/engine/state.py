

class State(object):

    def __init__(self):
        self.scenes = {}

    def add_scene(self, key, scene):
        self.scenes[key] = scene

    def remove_scene(self, key):
        del self.scenes[key]

    def clear(self):
        self.scenes = {}

    def update(self, invert=False, tint=(0, 0, 0), colorkey=None):
        for scene in self.scenes.keys():
            for key in self.scenes[scene].view_update_values.keys():
                self.scenes[scene].update(key, *self.scenes[scene].view_update_values[key], invert=invert, tint=tint,
                                          colorkey=colorkey)

    def update_collisions(self):
        for key in self.scenes.keys():
            self.scenes[key].update_collisions()
