import os
from pygame import Rect
from zelda import engine, SPRITE_DIR


class LinkSword(engine.GameObject):
    def __init__(self, facing, mode='slash'):
        self.resource_manager = engine.ResourceManager()
        link_sheet = engine.Spritesheet(os.path.join(SPRITE_DIR, 'Link.png'))

        # Load animations
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_right', link_sheet, (192, 128), 4, 4, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_up', link_sheet, (128, 128), 4, 4, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_down', link_sheet, (64, 128), 4, 4, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_left', link_sheet, (0, 128), 4, 4, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_spin_clockwise', link_sheet, (0, 144), 8, 8, (16, 16), 0, 0, (64, 64, 192))
        self.resource_manager.add_spritesheet_strip_offsets('link_sword_spin_counter', link_sheet, (0, 160), 8, 8, (16, 16), 0, 0, (64, 64, 192))
        self.directions = ['link_sword_right', 'link_sword_up', 'link_sword_left', 'link_sword_down']

        engine.GameObject.__init__(self, image=self.resource_manager.get_images(self.directions[facing]), layer=25,
                                   persistent=True)

        self.add_animation('link_sword_up', self.resource_manager.get_images('link_sword_up'))
        self.add_animation('link_sword_down', self.resource_manager.get_images('link_sword_down'))
        self.add_animation('link_sword_right', self.resource_manager.get_images('link_sword_right'))
        self.add_animation('link_sword_left', self.resource_manager.get_images('link_sword_left'))
        self.add_animation('link_sword_spin_clockwise', self.resource_manager.get_images('link_sword_spin_clockwise'))
        self.add_animation('link_sword_spin_counter', self.resource_manager.get_images('link_sword_spin_counter'))

        self.set_animation(self.directions[facing], 0)

        self.animation_speed = 30

        self.facing = facing
        self.handle_collisions = True
        frame_col = {'up': ((3, 10), (1, 6)),
                     'ur': ((0, 6), (10, 10)),
                     'right': ((0, 11), (6, 1)),
                     'dr': ((0, 0), (10, 10)),
                     'down': ((11, 0), (1, 6)),
                     'dl': ((6, 0), (10, 10)),
                     'left': ((10, 11), (6, 1)),
                     'ul': ((6, 6), (10, 10)),
                     'right_upper': ((0, 3), (6, 1))}
        hit_boxes = {'up': ((2, 4), (6, 12)),
                     'ur': ((0, 0), (16, 16)),
                     'right': ((0, 8), (12, 6)),
                     'dr': ((0, 0), (16, 16)),
                     'down': ((2, 0), (6, 12)),
                     'dl': ((0, 0), (16, 16)),
                     'left': ((4, 8), (12, 6)),
                     'ul': ((0, 0), (16, 16)),
                     'right_upper': ((0, 2), (12, 6))}
        self.collision_rects = {'link_sword_up': [Rect(frame_col['right_upper']), Rect(frame_col['ur']), Rect(frame_col['up'])],
                                'link_sword_down': [Rect(frame_col['left']), Rect(frame_col['dl']), Rect(frame_col['down'])],
                                'link_sword_right': [Rect(frame_col['up']), Rect(frame_col['ur']), Rect(frame_col['right'])],
                                'link_sword_left': [Rect(frame_col['up']), Rect(frame_col['ul']), Rect(frame_col['left'])],
                                'link_sword_spin_clockwise': [Rect(frame_col['dr']), Rect(frame_col['down']),
                                                              Rect(frame_col['dl']), Rect(frame_col['left']),
                                                              Rect(frame_col['ul']), Rect(frame_col['up']),
                                                              Rect(frame_col['ur']), Rect(frame_col['right'])],
                                'link_sword_spin_counter': [Rect(frame_col['dl']), Rect(frame_col['down']),
                                                            Rect(frame_col['dr']), Rect(frame_col['right']),
                                                            Rect(frame_col['ur']), Rect(frame_col['up']),
                                                            Rect(frame_col['ul']), Rect(frame_col['left'])]}
        self.hitbox_rects = {'link_sword_up': [Rect(hit_boxes['right_upper']), Rect(hit_boxes['ur']), Rect(hit_boxes['up'])],
                             'link_sword_down': [Rect(hit_boxes['left']), Rect(hit_boxes['dl']), Rect(hit_boxes['down'])],
                             'link_sword_right': [Rect(hit_boxes['up']), Rect(hit_boxes['ur']), Rect(hit_boxes['right'])],
                             'link_sword_left': [Rect(hit_boxes['up']), Rect(hit_boxes['ul']), Rect(hit_boxes['left'])],
                             'link_sword_spin_clockwise': [Rect(hit_boxes['dr']), Rect(hit_boxes['down']),
                                                           Rect(hit_boxes['dl']), Rect(hit_boxes['left']),
                                                           Rect(hit_boxes['ul']), Rect(hit_boxes['up']),
                                                           Rect(hit_boxes['ur']), Rect(hit_boxes['right'])],
                             'link_sword_spin_counter': [Rect(hit_boxes['dl']), Rect(hit_boxes['down']),
                                                         Rect(hit_boxes['dr']), Rect(hit_boxes['right']),
                                                         Rect(hit_boxes['ur']), Rect(hit_boxes['up']),
                                                         Rect(hit_boxes['ul']), Rect(hit_boxes['left'])]}
        self.call_special_update = True

    def update_collisions(self):
        self.collision_rect = self.collision_rects[self.current_key][self.animation_frame]
        self.hitbox = self.hitbox_rects[self.current_key][self.animation_frame]

    def special_update(self, game_scene):
        for game_object in game_scene.list_objects():
            if game_object.get_global_hitbox().colliderect(self.get_global_hitbox()):
                if game_object.object_type == 'octorok':
                    game_scene.remove_object(game_object)
