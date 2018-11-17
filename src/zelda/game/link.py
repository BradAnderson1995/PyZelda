import os
import pygame
import effects
import random
import linksword
import specialtiles
from zelda import engine, SPRITE_DIR, SOUND_DIR
from pygame.locals import *


class Link(engine.GameObject):
    def __init__(self, layer=50):
        self.resource_manager = engine.ResourceManager()
        link_path = os.path.join(SPRITE_DIR, 'Link.png')
        link_sheet = engine.Spritesheet(link_path)
        world_path = os.path.join(SPRITE_DIR, 'OverworldSheet.png')
        overworld_sheet = engine.Spritesheet(world_path)
        self.resource_manager.add_spritesheet_strip_offsets('overworld_tiles', overworld_sheet, (1, 1), 600, 24, (16, 16), 1, 1)

        # Load animations
        self.resource_manager.add_spritesheet_strip_offsets('link_walk_down', link_sheet, (32, 0), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_walk_up', link_sheet, (64, 0), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_walk_left', link_sheet, (0, 0), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_walk_right', link_sheet, (96, 0), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_push_down', link_sheet, (32, 16), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_push_up', link_sheet, (64, 16), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_push_left', link_sheet, (0, 16), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_push_right', link_sheet, (96, 16), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_shield_walk_down', link_sheet, (32, 32), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_shield_walk_up', link_sheet, (64, 32), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_shield_walk_left', link_sheet, (0, 32), 2, 2, (16, 16), 0, 0, (64, 64, 192))  # These two might be messed up
        self.resource_manager.add_spritesheet_strip_offsets('link_shield_walk_right', link_sheet, (96, 32), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_use_shield_down', link_sheet, (32, 48), 2, 2, (16, 16), 0, 0, (64, 64, 192))  # Needs to be fixed
        self.resource_manager.add_spritesheet_strip_offsets('link_use_shield_up', link_sheet, (64, 48), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_use_shield_left', link_sheet, (0, 48), 2, 2, (16, 16), 0, 0, (64, 64, 192))  # Take a look at black spot
        self.resource_manager.add_spritesheet_strip_offsets('link_use_shield_right', link_sheet, (96, 48), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_hop_down', link_sheet, (0, 64), 3, 3, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_fall', link_sheet, (0, 96), 3, 3, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_down', link_sheet, (32, 112), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_up', link_sheet, (64, 112), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_left', link_sheet, (0, 112), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_right', link_sheet, (96, 112), 2, 2, (16, 16), 0, 0, (64, 64, 192))
        engine.GameObject.__init__(self, self.resource_manager.get_images('link_walk_down'), layer,
                                   collision_rect=pygame.Rect((3, 4), (10, 11)),
                                   handle_collisions=True, object_type='player', persistent=True)

        # Add animations to Link
        self.add_animation('link_walk_up', self.resource_manager.get_images('link_walk_up'))
        self.add_animation('link_walk_down', self.resource_manager.get_images('link_walk_down'))
        self.add_animation('link_walk_right', self.resource_manager.get_images('link_walk_right'))
        self.add_animation('link_walk_left', self.resource_manager.get_images('link_walk_left'))
        self.add_animation('link_push_up', self.resource_manager.get_images('link_push_up'))
        self.add_animation('link_push_down', self.resource_manager.get_images('link_push_down'))
        self.add_animation('link_push_left', self.resource_manager.get_images('link_push_left'))
        self.add_animation('link_push_right', self.resource_manager.get_images('link_push_right'))
        self.add_animation('link_shield_walk_up', self.resource_manager.get_images('link_shield_walk_up'))
        self.add_animation('link_shield_walk_down', self.resource_manager.get_images('link_shield_walk_down'))
        self.add_animation('link_shield_walk_right', self.resource_manager.get_images('link_shield_walk_right'))
        self.add_animation('link_shield_walk_left', self.resource_manager.get_images('link_shield_walk_left'))
        self.add_animation('link_use_shield_up', self.resource_manager.get_images('link_use_shield_up'))
        self.add_animation('link_use_shield_down', self.resource_manager.get_images('link_use_shield_down'))
        self.add_animation('link_use_shield_left', self.resource_manager.get_images('link_use_shield_left'))
        self.add_animation('link_use_shield_right', self.resource_manager.get_images('link_use_shield_right'))
        self.add_animation('link_hop_down', self.resource_manager.get_images('link_hop_down'))
        self.add_animation('link_fall', self.resource_manager.get_images('link_fall'))
        self.add_animation('link_sword_up', self.resource_manager.get_images('link_sword_up'))
        self.add_animation('link_sword_down', self.resource_manager.get_images('link_sword_down'))
        self.add_animation('link_sword_right', self.resource_manager.get_images('link_sword_right'))
        self.add_animation('link_sword_left', self.resource_manager.get_images('link_sword_left'))

        # Group animations
        self.link_walk = ['link_walk_right', 'link_walk_up', 'link_walk_left', 'link_walk_down']
        self.link_push = ['link_push_right', 'link_push_up', 'link_push_left', 'link_push_down']
        self.link_shield_walk = ['link_shield_walk_right', 'link_shield_walk_up', 'link_shield_walk_left', 'link_shield_walk_down']
        self.link_use_shield = ['link_use_shield_right', 'link_use_shield_up', 'link_use_shield_left', 'link_use_shield_down']
        self.link_sword = ['link_sword_right', 'link_sword_up', 'link_sword_left', 'link_sword_down']

        # Add sounds to Link
        self.resource_manager.add_sound('link_hop', os.path.join(SOUND_DIR, 'LA_Link_Jump.wav'))
        self.resource_manager.add_sound('link_land', os.path.join(SOUND_DIR, 'LA_Link_Land.wav'))
        self.resource_manager.add_sound('link_shield', os.path.join(SOUND_DIR, 'LA_Shield.wav'))
        self.resource_manager.add_sound('link_fall', os.path.join(SOUND_DIR, 'LA_Link_Fall.wav'))
        self.resource_manager.add_sound('link_sword_1', os.path.join(SOUND_DIR, 'LA_Sword_Slash1.wav'))
        self.resource_manager.add_sound('link_sword_2', os.path.join(SOUND_DIR, 'LA_Sword_Slash2.wav'))
        self.resource_manager.add_sound('link_sword_3', os.path.join(SOUND_DIR, 'LA_Sword_Slash3.wav'))
        self.resource_manager.add_sound('link_sword_4', os.path.join(SOUND_DIR, 'LA_Sword_Slash4.wav'))
        self.resource_manager.add_sound('link_sword_charge', os.path.join(SOUND_DIR, 'LA_Sword_Charge.wav'))
        self.resource_manager.add_sound('link_sword_spin', os.path.join(SOUND_DIR, 'LA_Sword_Spin.wav'))
        self.resource_manager.add_sound('link_sword_tap', os.path.join(SOUND_DIR, 'LA_Sword_Tap.wav'))
        self.resource_manager.add_sound('grass_cut', os.path.join(SOUND_DIR, 'LA_Bush_Cut.wav'))

        self.sword_slashes = ['link_sword_1', 'link_sword_2', 'link_sword_3', 'link_sword_4']

        # Configure Link's properties
        self.speed = 1.25  # 1.25
        self.movement = {0: (self.speed, 0), 1: (0, -self.speed), 2: (-self.speed, 0), 3: (0, self.speed)}
        self.direction = 3
        self.facing = 3
        self.big_grass = ['big_grass', 'big_forest_grass']
        self.short_grass = ['short_grass', 'short_forest_grass']
        self.effect_short_grass = ['effect_short_grass', 'effect_short_forest_grass']
        self.in_grass = False
        self.shield = False
        self.left = None
        self.right = None
        self.controllable = True
        self.no_clip = False
        self.direction_held = False
        self.body_rect = self.rect
        self.interaction_rect = None  # self.collision_rect.copy()
        self.standard_animation_speed = 15
        self.solid = True

        # Link's States
        # self.walk = WalkingState()
        # self.collide = CollidingState()
        # self.shield = ShieldState()
        self._state = WalkingState(self)
        self.state = 'WalkingState'

    def update_interactions(self):
        if self.facing == 0:
            self.interaction_rect = pygame.Rect((self.position[0]+self.collision_rect.x+self.collision_rect.width,
                                                 self.position[1]+self.collision_rect.y),
                                                (1, self.collision_rect.height))
        elif self.facing == 1:
            self.interaction_rect = pygame.Rect((self.position[0]+self.collision_rect.x,
                                                 self.position[1]+self.collision_rect.y-1),
                                                (self.collision_rect.width, 1))
        elif self.facing == 2:
            self.interaction_rect = pygame.Rect((self.position[0]+self.collision_rect.x-1,
                                                 self.position[1]+self.collision_rect.y),
                                                (1, self.collision_rect.height))
        elif self.facing == 3:
            self.interaction_rect = pygame.Rect((self.position[0]+self.collision_rect.x,
                                                 self.position[1]+self.collision_rect.y+self.collision_rect.height),
                                                (self.collision_rect.width, 1))

    def update_state(self, game_scene):
        self._state.update(self, game_scene)
        in_grass = False
        grass_type = None

        # Short grass effect
        for game_object in game_scene.check_object_collision_objects(self):
            object_type = game_object.object_type
            if object_type in self.short_grass:
                in_grass = True
                grass_type = object_type
        if in_grass and not self.in_grass:
            if grass_type == self.short_grass[0]:
                game_scene.insert_object(effects.ShortGrass(), self.position)
            elif grass_type == self.short_grass[1]:
                game_scene.insert_object(effects.ShortForestGrass(), self.position)
            self.in_grass = True
        elif not in_grass and self.in_grass:
            for game_object in game_scene.list_objects():
                if game_object.object_type in self.effect_short_grass:
                    game_scene.remove_object(game_object)
            self.in_grass = False

    def play_sound(self, key):
        self.resource_manager.play_sound(key)

    def set_speed(self, speed):
        self.speed = speed
        self.movement = {0: (self.speed, 0), 1: (0, -self.speed), 2: (-self.speed, 0), 3: (0, self.speed)}

    def handle_input(self, game_scene):
        if self._state is not None:
            self._state.handle_input(self, game_scene)
            self.update_interactions()

    def handle_event(self, game_scene, event):
        if self._state is not None:
            self._state.handle_event(self, game_scene, event)
            self.update_interactions()


class WalkingState(engine.ObjectState):
    def __init__(self, link):
        link.state = 'WalkingState'
        engine.ObjectState.__init__(self)
        # Change animations
        if not link.shield:
            link.set_animation(link.link_walk[link.facing], 0)
        else:
            link.set_animation(link.link_shield_walk[link.facing], 0)
        link.controllable = True
        link.animation_speed = link.standard_animation_speed
        link.rect_offset = (0, 0)

    @staticmethod
    def handle_input(link, game_scene):
        key = pygame.key.get_pressed()
        moves = []
        moved = False
        # mouse = pygame.mouse.get_pressed()
        # if mouse[2]:
        #     link._state = ShieldState(link)

        # Gather movement directions
        if not key[K_a] and not key[K_d] and not key[K_w] and not key[K_s] and not key[K_b]:
            link.set_animation_frame(0)
        else:
            if key[K_a] and not key[K_d]:
                if not key[K_w] and not key[K_s] and link.facing != 2:
                    link.facing = 2
                    if not link.shield:
                        link.set_animation(link.link_walk[link.facing], 0)
                    else:
                        link.set_animation(link.link_shield_walk[link.facing], 0)
                link.direction = 2
                moves.append(2)
                moved = True
            elif key[K_d] and not key[K_a]:
                if not key[K_w] and not key[K_s] and link.facing != 0:
                    link.facing = 0
                    if not link.shield:
                        link.set_animation(link.link_walk[link.facing], 0)
                    else:
                        link.set_animation(link.link_shield_walk[link.facing], 0)
                link.direction = 0
                moves.append(0)
                moved = True
            if key[K_s] and not key[K_w]:
                if not key[K_d] and not key[K_a] and link.facing != 3:
                    link.facing = 3
                    if not link.shield:
                        link.set_animation(link.link_walk[link.facing], 0)
                    else:
                        link.set_animation(link.link_shield_walk[link.facing], 0)
                link.direction = 3
                moves.append(3)
                moved = True
            elif key[K_w] and not key[K_s]:
                if not key[K_d] and not key[K_a] and link.facing != 1:
                    link.facing = 1
                    if not link.shield:
                        link.set_animation(link.link_walk[link.facing], 0)
                    else:
                        link.set_animation(link.link_shield_walk[link.facing], 0)
                link.direction = 1
                moves.append(1)
                moved = True

        # Execute movements
        if moved:
            for move_direction in moves:
                previous_position = link.position
                link.increment(link.movement[move_direction])
                # Deal with collisions
                if not link.no_clip:
                    collisions = []
                    # Figure out what link is colliding with
                    for game_object in game_scene.check_object_collision_objects(link):
                        # Regular collisions, stop movement
                        if game_object.solid:
                            collisions.append('solid')
                        if 'slow' in game_object.properties:
                            collisions.append('slow')
                            link.set_speed(float(game_object.properties['slow']))
                        if game_object.object_type == 'hole':
                            collisions.append('hole')
                        if game_object.object_type == 'jump':
                            collisions.append('jump')
                        # if game_object.object_type == "octorok":
                        #     print("Octorok")
                    if 'solid' in collisions:
                        link.move(previous_position)
                        link._state = CollidingState(link)
                    elif 'jump' in collisions:
                        link._state = HoppingState(link)
                    elif 'hole' in collisions:
                        link._state = SlippingState(link)

                    #TODO: Fix this
                    if 'slow' not in collisions:
                        link.set_speed(float(1.25))

            # Update and move short grass effect
            if link.in_grass:
                for game_object in game_scene.list_objects():
                    if game_object.object_type in link.effect_short_grass:
                        game_object.move(link.position)
                        game_object.update()

            link.update()

    @staticmethod
    def handle_event(link, game_scene, event):
        if event.type == MOUSEBUTTONDOWN:
            button = event.button
            if button == 1:
                link._state = SwordState(link)
            if button == 3:
                if link.shield:
                    link._state = ShieldState(link)

    def update(self, link, game_scene):
        return


class CollidingState(engine.ObjectState):
    def __init__(self, link):
        link.state = 'CollidingState'
        engine.ObjectState.__init__(self)
        link.set_animation(link.link_push[link.facing], 0)
        link.controllable = True
        link.animation_speed = link.standard_animation_speed
        link.rect_offset = (0, 0)

    @staticmethod
    def handle_input(link, game_scene):
        key = pygame.key.get_pressed()
        moves = []
        moved = False

        if key[K_a] and not key[K_d]:
            if not key[K_w] and not key[K_s] and link.facing != 2:
                link.facing = 2
                link.set_animation(link.link_push[link.facing], 0)
            link.direction = 2
            moves.append(2)
            moved = True
        elif key[K_d] and not key[K_a]:
            if not key[K_w] and not key[K_s] and link.facing != 0:
                link.facing = 0
                link.set_animation(link.link_push[link.facing], 0)
            link.direction = 0
            moves.append(0)
            moved = True
        if key[K_s] and not key[K_w]:
            if not key[K_d] and not key[K_a] and link.facing != 3:
                link.facing = 3
                link.set_animation(link.link_push[link.facing], 0)
            link.direction = 3
            moves.append(3)
            moved = True
        elif key[K_w] and not key[K_s]:
            if not key[K_d] and not key[K_a] and link.facing != 1:
                link.facing = 1
                link.set_animation(link.link_push[link.facing], 0)
            link.direction = 1
            moves.append(1)
            moved = True

        not_colliding_any = True
        if moved:
            for move_direction in moves:
                not_colliding_direction = True
                previous_position = link.position
                link.increment(link.movement[move_direction])
                for game_object in game_scene.check_object_collision_objects(link):
                    # Regular collisions, stop movement
                    if game_object.solid and not link.no_clip:
                        not_colliding_direction = False
                        not_colliding_any = False

                    # Stairs
                    if 'slow' in game_object.properties:
                        link.set_speed(float(game_object.properties['slow']))
                    else:
                        link.set_speed(float(1.25))

                if not not_colliding_direction:
                    link.move(previous_position)

            # Update and move short grass effect
            if link.in_grass:
                for game_object in game_scene.list_objects():
                    if game_object.object_type in link.effect_short_grass:
                        game_object.move(link.position)
                        game_object.update()

            link.update()
        if not_colliding_any:
            link._state = WalkingState(link)

    @staticmethod
    def handle_event(link, game_scene, event):
        if event.type == MOUSEBUTTONDOWN:
            button = event.button
            if button == 1:
                link._state = SwordState(link)

    def update(self, link, game_scene):
        return


class HoppingState(engine.ObjectState):
    def __init__(self, link):
        link.state = 'HoppingState'
        engine.ObjectState.__init__(self)
        link.set_animation('link_hop_down', 0)
        link.controllable = False
        link.animation_counter = 0
        link.play_sound('link_hop')
        self.hop_frame = 0
        link.animation_speed = 15
        link.rect_offset = (0, 0)

    @staticmethod
    def handle_input(link, game_scene):
        return

    @staticmethod
    def handle_event(link, game_scene, event):
        pass

    def update(self, link, game_scene):
        moved = False
        for game_object in game_scene.check_object_collision_objects(link):
            if game_object.solid or game_object.object_type == 'jump':
                link.increment((0, 1))
                moved = True
            if self.hop_frame < 3:
                if link.animation_counter >= 7:
                    link.next_frame(1)
                    link.animation_counter = 0
                    self.hop_frame += 1
            else:
                link.set_animation('link_walk_down', 0)
        if not moved:
            link.play_sound('link_land')
            link._state = WalkingState(link)


# TODO: Slipping should not be a state, can be in other states while slipping. Perhaps hole should pull player in.
class SlippingState(engine.ObjectState):
    def __init__(self, link):
        engine.ObjectState.__init__(self)

    @staticmethod
    def handle_input(link, game_scene):
        return

    @staticmethod
    def handle_event(link, game_scene, event):
        pass

    def update(self, link, game_scene):
        return


class FallingState(engine.ObjectState):
    def __init__(self, link):
        engine.ObjectState.__init__(self)
        link._state = WalkingState(link)

    @staticmethod
    def handle_input(link, game_scene):
        return

    @staticmethod
    def handle_event(link, game_scene, event):
        pass

    def update(self, link, game_scene):
        return


class ShieldState(engine.ObjectState):
    def __init__(self, link):
        link.state = 'ShieldState'
        engine.ObjectState.__init__(self)
        link.controllable = False
        link.set_animation(link.link_use_shield[link.facing], 0)
        link.play_sound('link_shield')
        link.animation_speed = link.standard_animation_speed
        link.rect_offset = (0, 0)

    @staticmethod
    def handle_input(link, game_scene):
        key = pygame.key.get_pressed()
        moves = []
        moved = False
        mouse = pygame.mouse.get_pressed()
        LOG.debug('Mouse: %s', mouse)
        if not mouse[2]:
            link._state = WalkingState(link)
        # Gather movement directions
        if not key[K_a] and not key[K_d] and not key[K_w] and not key[K_s] and not key[K_b]:
            link.set_animation_frame(0)
        else:
            if key[K_a] and not key[K_d]:
                if not key[K_w] and not key[K_s] and link.facing != 2:
                    link.facing = 2
                    link.set_animation(link.link_use_shield[link.facing], 0)
                link.direction = 2
                moves.append(2)
                moved = True
            elif key[K_d] and not key[K_a]:
                if not key[K_w] and not key[K_s] and link.facing != 0:
                    link.facing = 0
                    link.set_animation(link.link_use_shield[link.facing], 0)
                link.direction = 0
                moves.append(0)
                moved = True
            if key[K_s] and not key[K_w]:
                if not key[K_d] and not key[K_a] and link.facing != 3:
                    link.facing = 3
                    link.set_animation(link.link_use_shield[link.facing], 0)
                link.direction = 3
                moves.append(3)
                moved = True
            elif key[K_w] and not key[K_s]:
                if not key[K_d] and not key[K_a] and link.facing != 1:
                    link.facing = 1
                    link.set_animation(link.link_use_shield[link.facing], 0)
                link.direction = 1
                moves.append(1)
                moved = True

        # Execute movements
        if moved:
            for move_direction in moves:
                previous_position = link.position
                link.increment(link.movement[move_direction])
                # Deal with collisions
                if not link.no_clip:
                    collisions = []
                    # Figure out what link is colliding with
                    for game_object in game_scene.check_object_collision_objects(link):
                        # Regular collisions, stop movement
                        if game_object.solid:
                            collisions.append('solid')
                        if 'slow' in game_object.properties:
                            collisions.append('slow')
                            link.set_speed(float(game_object.properties['slow']))
                        if game_object.object_type == 'hole':
                            collisions.append('hole')
                        if game_object.object_type == 'jump':
                            collisions.append('jump')
                    if 'solid' in collisions:
                        link.move(previous_position)
                        # link._state = CollidingState(link)
                    elif 'jump' in collisions:
                        link._state = HoppingState(link)
                    elif 'hole' in collisions:
                        link._state = SlippingState(link)

                    # TODO: Fix this
                    if 'slow' in collisions:
                        link.set_speed(float(1.25))

            # Update and move short grass effect
            if link.in_grass:
                for game_object in game_scene.list_objects():
                    if game_object.object_type in link.effect_short_grass:
                        game_object.move(link.position)
                        game_object.update()

            link.update()

    @staticmethod
    def handle_event(link, game_scene, event):
        if event.type == MOUSEBUTTONDOWN:
            button = event.button
            if button == 1:
                link._state = SwordState(link)

    def update(self, link, game_scene):
        return


class SwordState(engine.ObjectState):
    def __init__(self, link):
        link.state = 'SwordState'
        engine.ObjectState.__init__(self)
        link.set_animation(link.link_sword[link.facing], 0)
        link.animation_counter = 0
        self.holding = True
        self.incremented = False
        self.frame = -2
        link.animation_speed = 4
        link.rect_offset = (0, 0)

        # Play random slash sound
        link.play_sound(link.sword_slashes[random.randrange(0, 4, 1)])

        # Make the sword
        self.sword = linksword.LinkSword(link.facing, mode='slash')
        self.sword.animation_speed = link.animation_speed / 2
        self.inserted = False
        self.sword_positions = [[(0, -16), (12, -12), (16, 0)],
                                [(16, 0), (12, -12), (0, -16)],
                                [(0, -16), (-12, -12), (-16, 0)],
                                [(-16, 0), (-12, 12), (0, 16)]]
        self.link_movement = [(2, 0), (0, -2), (-2, 0), (0, 2)]

    def handle_input(self, link, game_scene):
        mouse = pygame.mouse.get_pressed()
        if not mouse[0]:
            self.holding = False

    def handle_event(self, link, game_scene, event):
        if event.type == MOUSEBUTTONDOWN:
            button = event.button
            if button == 1:
                if self.inserted:
                    game_scene.remove_object(self.sword)
                if self.incremented:
                    link.increment((-1*self.link_movement[link.facing][0], -1*self.link_movement[link.facing][1]))
                link._state = SwordState(link)

    def update(self, link, game_scene):
        if not self.inserted and self.frame == -1:
            game_scene.insert_object(self.sword, (link.position[0] + self.sword_positions[link.facing][0][0],
                                                  link.position[1] + self.sword_positions[link.facing][0][1]))
            self.sword.handle_collisions = False
            self.inserted = True
            self.frame = 0
        if self.frame == -2:
            self.frame = -1
        if self.sword.animation_frame < 2 and self.inserted:
            if self.sword.update():
                if self.sword.animation_frame == 1:
                    link.set_animation_frame(1)
                elif self.sword.animation_frame == 2:
                    link.increment(self.link_movement[link.facing])
                    self.incremented = True
                self.sword.move((link.position[0] + self.sword_positions[link.facing][self.frame][0],
                                 link.position[1] + self.sword_positions[link.facing][self.frame][1]))
                if self.sword.animation_frame == 2:
                    self.sword.handle_collisions = True
                    self.sword.update_collisions()

        if link.update(can_update=False):
            self.frame += 1
            if self.frame == 5:
                link.increment((-1*self.link_movement[link.facing][0], -1*self.link_movement[link.facing][1]))
                self.incremented = False
                if not self.holding:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[2]:
                        link._state = ShieldState(link)
                    else:
                        link._state = WalkingState(link)
                else:
                    link._state = SwordChargeState(link)
                game_scene.remove_object(self.sword)

        link.updated = True  # Don't know why these don't update normally here
        self.sword.updated = True

        for game_object in game_scene.list_objects():
            if game_object.object_type in link.big_grass or game_object.object_type in link.short_grass:
                if self.sword.handle_collisions:
                    if game_object.get_global_rect().colliderect(self.sword.get_global_collision_rect()):
                        position = game_object.position
                        game_scene.remove_object(game_object)
                        game_scene.insert_object(specialtiles.GroundTile(link.resource_manager), position)
                        game_scene.insert_object_centered(effects.CutGrass(), (position[0]-8, position[1]-8))
                        link.resource_manager.play_sound('grass_cut')


class SwordChargeState(engine.ObjectState):
    def __init__(self, link):
        link.state = 'SwordChargeState'
        engine.ObjectState.__init__(self)
        if link.shield:
            link.set_animation(link.link_shield_walk[link.facing], 0)
        else:
            link.set_animation(link.link_walk[link.facing], 0)
        link.animation_frame = 0
        self.holding = True
        self.charged = False
        self.spin = False
        self.frame = 0
        link.animation_speed = link.standard_animation_speed

        self.sword = linksword.LinkSword(link.facing, mode='charge')
        self.sword.set_animation_frame(2)
        self.sword_positions = [(12, 0), (0, -12), (-12, 0), (0, 12)]
        self.inserted = False

    def handle_input(self, link, game_scene):
        key = pygame.key.get_pressed()
        moves = []
        moved = False
        # Gather movement directions
        if not key[K_a] and not key[K_d] and not key[K_w] and not key[K_s] and not key[K_b]:
            link.set_animation_frame(0)
        else:
            if key[K_a] and not key[K_d]:
                link.direction = 2
                moves.append(2)
                moved = True
            elif key[K_d] and not key[K_a]:
                link.direction = 0
                moves.append(0)
                moved = True
            if key[K_s] and not key[K_w]:
                link.direction = 3
                moves.append(3)
                moved = True
            elif key[K_w] and not key[K_s]:
                link.direction = 1
                moves.append(1)
                moved = True

        # Execute movements
        if moved:
            stab = False
            for move_direction in moves:
                previous_position = link.position
                link.increment(link.movement[move_direction])
                # Deal with collisions
                if not link.no_clip:
                    collisions = []
                    # Figure out what link is colliding with
                    for game_object in game_scene.check_object_collision_objects(link):
                        # Regular collisions, stop movement
                        if game_object.solid:
                            collisions.append('solid')
                            if move_direction == link.facing:
                                if game_object.get_global_rect().colliderect(self.sword.get_global_collision_rect()):
                                    stab = True
                        if 'slow' in game_object.properties:
                            collisions.append('slow')
                            link.set_speed(float(game_object.properties['slow']))
                        if game_object.object_type == 'hole':
                            collisions.append('hole')
                        if game_object.object_type == 'jump':
                            collisions.append('jump')
                    if 'solid' in collisions:
                        link.move(previous_position)
                        # link._state = CollidingState(link)
                    elif 'jump' in collisions:
                        if self.inserted:
                            game_scene.remove_object(self.sword)
                        link._state = HoppingState(link)
                    elif 'hole' in collisions:
                        if self.inserted:
                            game_scene.remove_object(self.sword)
                        link._state = SlippingState(link)

                    #TODO: Fix this
                    if 'slow' in collisions:
                        link.set_speed(float(1.25))

            if stab and len(moves) == 1:
                if self.inserted:
                    game_scene.remove_object(self.sword)
                link._state = SwordStabState(link)

            # Update and move short grass effect
            if link.in_grass:
                for game_object in game_scene.list_objects():
                    if game_object.object_type in link.effect_short_grass:
                        game_object.move(link.position)
                        game_object.update()

            link.update()

    def handle_event(self, link, game_scene, event):
        if event.type == MOUSEBUTTONUP:
            button = event.button
            if button == 1:
                if self.charged:
                    if self.inserted:
                        game_scene.remove_object(self.sword)
                    link._state = SwordSpinState(link)
                else:
                    if self.inserted:
                        game_scene.remove_object(self.sword)
                    link._state = WalkingState(link)

    def update(self, link, game_scene):
        if not self.inserted:
            game_scene.insert_object(self.sword, (link.position[0] + self.sword_positions[link.facing][0],
                                                  link.position[1] + self.sword_positions[link.facing][1]))
            self.inserted = True
        else:
            self.sword.move((link.position[0] + self.sword_positions[link.facing][0],
                             link.position[1] + self.sword_positions[link.facing][1]))
        if self.charged:
            if self.sword.animation_frame == 2 and self.frame % 3 == 0:
                self.sword.set_animation_frame(3)
            elif self.frame % 3 == 0:
                self.sword.set_animation_frame(2)
        self.frame += 1
        if self.frame == 30:
            self.charged = True
            link.play_sound('link_sword_charge')


class SwordStabState(engine.ObjectState):
    def __init__(self, link):
        link.state = 'SwordStabState'
        engine.ObjectState.__init__(self)
        link.controllable = False
        link.animation_frame = 0
        link.animation_speed = 4
        link.animation_counter = 0
        self.frame = 0
        self.stabbed = False
        self.inserted = False

        link.set_animation(link.link_sword[link.facing], 1)
        self.sword = linksword.LinkSword(link.facing, mode='stab')
        self.sword_positions = [(12, 0), (0, -12), (-12, 0), (0, 12)]
        self.sword.animation_frame = 2
        self.sword.update_collisions()
        LOG.debug('Stabbing...')

    @staticmethod
    def handle_input(link, game_scene):
        return

    @staticmethod
    def handle_event(link, game_scene, event):
        return

    def update(self, link, game_scene):
        if not self.inserted:
            game_scene.insert_object(self.sword, (link.position[0] + self.sword_positions[link.facing][0],
                                                  link.position[1] + self.sword_positions[link.facing][1]))
            self.inserted = True
        if not self.stabbed:
            # Figure out what is being stabbed and act accordingly
            collisions = []
            # Figure out what link is colliding with
            for game_object in game_scene.list_objects():
                if game_object.object_type in link.big_grass:
                    if self.sword.handle_collisions:
                        if game_object.get_global_rect().colliderect(self.sword.get_global_collision_rect()):
                            position = game_object.position
                            game_scene.remove_object(game_object)
                            game_scene.insert_object(specialtiles.GroundTile(link.resource_manager), position)
                            game_scene.insert_object_centered(effects.CutGrass(), (position[0]-8, position[1]-8))
                            collisions.append('big_grass')
                elif game_object.solid:
                    collisions.append('solid')
            if 'big_grass' in collisions:
                link.resource_manager.play_sound('grass_cut')
            elif 'solid' in collisions:
                link.play_sound('link_sword_tap')
            self.stabbed = True

        if self.frame == 0:
            if link.update(can_update=False):
                self.frame = 1
                if link.facing == 0:
                    link.increment((2, 0))
                    self.sword.increment((2, 0))
                elif link.facing == 1:
                    link.increment((0, -2))
                    self.sword.increment((0, -2))
                elif link.facing == 2:
                    link.increment((-2, 0))
                    self.sword.increment((-2, 0))
                else:
                    link.increment((0, 2))
                    self.sword.increment((0, 2))
        elif self.frame == 2:
            if link.update(can_update=False):
                link.set_animation(link.link_walk[link.facing], 0)
                if link.facing == 0:
                    link.increment((-2, 0))
                    self.sword.increment((-2, 0))
                elif link.facing == 1:
                    link.increment((0, 2))
                    self.sword.increment((0, 2))
                elif link.facing == 2:
                    link.increment((2, 0))
                    self.sword.increment((2, 0))
                else:
                    link.increment((0, -2))
                    self.sword.increment((0, -2))
                self.frame += 1
        else:
            if link.update(can_update=False):
                self.frame += 1

        if self.frame == 6:
            if self.inserted:
                game_scene.remove_object(self.sword)
            mouse = pygame.mouse.get_pressed()
            if mouse[0]:
                link._state = SwordChargeState(link)
            else:
                link._state = WalkingState(link)


class SwordSpinState(engine.ObjectState):
    def __init__(self, link):
        link.state = 'SwordSpinState'
        engine.ObjectState.__init__(self)
        link.controllable = False
        link.animation_frame = 0
        link.play_sound('link_sword_spin')
        link.animation_speed = 4
        link.animation_counter = 0
        self.frame = 0

        self.positions = {'up': (0, -16), 'ur': (12, -12), 'right': (16, 0), 'dr': (12, 12),
                          'down': (0, 16), 'dl': (-12, 12), 'left': (-16, 0), 'ul': (-12, -12)}
        self.sword = linksword.LinkSword(link.facing, mode='spin')
        # self.sword.set_animation_frame(2)
        self.sword_positions = [[self.positions['dr'], self.positions['down'], self.positions['dl'], self.positions['left'],
                                 self.positions['ul'], self.positions['up'], self.positions['up'], self.positions['ur'],
                                 self.positions['right']],
                                [self.positions['ul'], self.positions['left'], self.positions['dl'], self.positions['down'],
                                 self.positions['dr'], self.positions['right'], self.positions['right'], self.positions['ur'],
                                 self.positions['up']],
                                [self.positions['dl'], self.positions['down'], self.positions['dr'], self.positions['right'],
                                 self.positions['ur'], self.positions['up'], self.positions['up'], self.positions['ul'],
                                 self.positions['left']],
                                [self.positions['dr'], self.positions['right'], self.positions['ur'], self.positions['up'],
                                 self.positions['ul'], self.positions['left'], self.positions['left'], self.positions['dl'],
                                 self.positions['down']]]
        self.link_sprite_indices = [['link_sword_right', 'link_sword_down', 'link_sword_left', 'link_sword_up', 'link_sword_right'],
                                    ['link_sword_up', 'link_sword_left', 'link_sword_down', 'link_sword_right', 'link_sword_up'],
                                    ['link_sword_left', 'link_sword_down', 'link_sword_right', 'link_sword_up', 'link_sword_left'],
                                    ['link_sword_down', 'link_sword_right', 'link_sword_up', 'link_sword_left', 'link_sword_down']]
        self.inserted = False
        link.set_animation(self.link_sprite_indices[link.facing][0], 1)
        if link.facing == 0:
            self.sword.set_animation('link_sword_spin_clockwise', 0)
        elif link.facing == 1:
            self.sword.set_animation('link_sword_spin_counter', 6)
        elif link.facing == 2:
            self.sword.set_animation('link_sword_spin_counter', 0)
        elif link.facing == 3:
            self.sword.set_animation('link_sword_spin_counter', 2)
        self.sword.update_collisions()

    @staticmethod
    def handle_input(link, game_scene):
        return

    @staticmethod
    def handle_event(link, game_scene, event):
        return

    def update(self, link, game_scene):
        if not self.inserted:
            game_scene.insert_object(self.sword, (link.position[0] + self.sword_positions[link.facing][0][0],
                                                  link.position[1] + self.sword_positions[link.facing][0][1]))
            self.inserted = True
        if link.update(can_update=False):
            if self.frame < 8:
                self.sword.move((link.position[0] + self.sword_positions[link.facing][self.frame+1][0],
                                 link.position[1] + self.sword_positions[link.facing][self.frame+1][1]))
                if self.frame == 1:
                    link.set_animation(self.link_sprite_indices[link.facing][1], 1)
                elif self.frame == 2:
                    link.set_animation(self.link_sprite_indices[link.facing][2], 1)
                elif self.frame == 5:
                    link.set_animation(self.link_sprite_indices[link.facing][3], 1)
                elif self.frame == 7:
                    link.set_animation(self.link_sprite_indices[link.facing][4], 1)
                if self.frame != 5:
                    self.sword.next_frame(1)
                self.sword.update_collisions()
            else:
                game_scene.remove_object(self.sword)
                link._state = WalkingState(link)
            self.frame += 1
            link.updated = True
            self.sword.updated = True

        for game_object in game_scene.list_objects():
            if game_object.object_type in link.big_grass or game_object.object_type in link.short_grass:
                if self.sword.handle_collisions:
                    if game_object.get_global_rect().colliderect(self.sword.get_global_collision_rect()):
                        position = game_object.position
                        game_scene.remove_object(game_object)
                        game_scene.insert_object(specialtiles.GroundTile(link.resource_manager), position)
                        game_scene.insert_object_centered(effects.CutGrass(), (position[0]-8, position[1]-8))
