import random
import pygame
from zelda import engine


class AbstractEnemy(engine.GameObject):
    def __init__(self):
        self.resource_manager = engine.ResourceManager()
        engine.GameObject.__init__(self, layer=0, handle_collisions=True, solid=True, object_type='enemy')


class Octorok(AbstractEnemy):
    def __init__(self, resource_manager):
        AbstractEnemy.__init__(self)
        self.resource_manager.add_image_list('octorok_walk_left', [resource_manager.get_images('octorok')[0],
                                                                   resource_manager.get_images('octorok')[1]])
        self.resource_manager.add_image_list('octorok_walk_down', [resource_manager.get_images('octorok')[2],
                                                                   resource_manager.get_images('octorok')[3]])
        self.resource_manager.add_image_list('octorok_walk_up', [resource_manager.get_images('octorok')[4],
                                                                 resource_manager.get_images('octorok')[5]])
        self.resource_manager.add_image_list('octorok_walk_right', [resource_manager.get_images('octorok')[6],
                                                                    resource_manager.get_images('octorok')[7]])
        self.resource_manager.add_image('octorok_missile', resource_manager.get_images('octorok')[8])

        self.add_animation('octorok_walk_up', self.resource_manager.get_images('octorok_walk_up'))
        self.add_animation('octorok_walk_down', self.resource_manager.get_images('octorok_walk_down'))
        self.add_animation('octorok_walk_left', self.resource_manager.get_images('octorok_walk_left'))
        self.add_animation('octorok_walk_right', self.resource_manager.get_images('octorok_walk_right'))
        self.animations = ['octorok_walk_right', 'octorok_walk_up', 'octorok_walk_left', 'octorok_walk_down']
        self.facing = random.randint(0, 3)
        self.solid = True
        self.hitbox = pygame.Rect((0, 0), (16, 16))

        self.object_type = 'octorok'
        self._state = WalkingState(self)
        self.speed = 1.0
        self.movement = {0: (self.speed, 0), 1: (0, -self.speed), 2: (-self.speed, 0), 3: (0, self.speed)}
        self.mouth = [(16, 2), (2, 0), (0, 2), (2, 16)]

    def turn(self):
        self.facing = random.randint(0, 3)
        self.set_animation(self.animations[self.facing], 0)


class WalkingState(engine.ObjectState):
    def __init__(self, octorok):
        octorok.state = 'WalkingState'
        engine.ObjectState.__init__(self)
        # Change animations
        octorok.set_animation(octorok.animations[octorok.facing], 0)
        octorok.collision_rect = octorok.images[octorok.current_key][0][0].get_rect()
        self.animation_speed = 15
        self.frame = 0
        self.shot_counter = 0
        self.walking = False
        self.missile = octorok.resource_manager.get_images('octorok_missile')

    def update(self, octorok, game_scene):
        if self.walking:
            previous_position = octorok.position
            octorok.increment(octorok.movement[octorok.facing])
            on_screen = False
            for game_object in game_scene.check_object_collision_objects(octorok):
                if game_object.solid:
                    octorok.position = previous_position
                    self.walking = False
                if game_object.object_type == 'camera':
                    if game_scene.check_contain_object(game_object, octorok):
                        on_screen = True
            if not on_screen:
                octorok.position = previous_position
                self.walking = False
            if octorok.update():
                self.frame += 1
                if self.shot_counter < 8:
                    self.shot_counter += 1
                if self.frame == 5:
                    self.frame = 0
                    self.walking = False
        else:
            if octorok.update(can_update=False):
                if self.frame < 2:
                    self.frame += 1
                    if self.shot_counter < 8:
                        self.shot_counter += 1
                else:
                    self.frame = 0
                    self.walking = True
                    octorok.turn()
        # if self.shot_counter == 8 and self.walking == False:
        #     missile = Missile(self.missile, octorok.facing)
        #     game_scene.insert_object(missile, (octorok.position[0] + octorok.mouth[octorok.facing][0],
        #                                        octorok.position[1] + octorok.mouth[octorok.facing][1]))
        #     self.shot_counter = 0


class Missile(engine.GameObject):
    def __init__(self, missile_sprite, direction):
        engine.GameObject.__init__(self, missile_sprite, handle_collisions=True)
        self.speed = 4
        self.movement = {0: (self.speed, 0), 1: (0, -self.speed), 2: (-self.speed, 0), 3: (0, self.speed)}
        self.direction = direction
        self.call_special_update = True

    def special_update(self, game_scene):
        self.increment(self.movement[self.direction])
        on_screen = False
        for game_object in game_scene.check_object_collision_objects(self):
            if game_object.solid and game_object.object_type != 'octorok':
                self.remove = True
                game_scene.remove_object(self)
            if game_object.object_type == 'camera':
                if game_scene.check_contain_object(game_object, self):
                    on_screen = True
                    game_scene.remove_object(self)
        if not on_screen:
            self.remove = True
