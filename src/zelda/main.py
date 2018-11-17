# Standard
import argparse
import logging
import os
import pkg_resources
import sys
from logging.config import dictConfig

# Third Party
import pygame
from pygame.locals import *
from log_color import ColorStripper, ColorFormatter

# Project
from zelda import (
    RESOURCE_DIR,
    SPRITE_DIR,
    MUSIC_DIR,
    FONT_DIR,
    engine,
    game,
)

LOG = logging.getLogger(__name__)

ZELDA_ASCII = """
              _______
         ..-'`       ````---.
       .'          ___ .'````.'SS'.
      /        ..-SS####'.  /SSHH##'.
     |       .'SSSHHHH##|/#/#HH#H####'.
    /      .'SSHHHHH####/||#/: \SHH#####\\
   /      /SSHHHHH#####/!||;`___|SSHH###\\
-..__    /SSSHHH######.         \SSSHH###\\
`.'-.''--._SHHH#####.'           '.SH####/
  '. ``'-  '/SH####`/_             `|H##/
  | '.     /SSHH###|`'==.       .=='/\H|
  |   `'-.|SHHHH##/\__\/        /\//|~|/
  |    |S#|/HHH##/             |``  |
  |    \H' |H#.'`              \    |
  |        ''`|               -     /
  |          /H\          .----    /
  |         |H#/'.           `    /
  |          \| | '..            /
  |    ^~DLF   /|    ''..______.'
   \          //\__    _..-. |
    \         ||   ````     \ |_
     \    _.-|               \| |_
     _\_.-'   `'''''-.        |   `--.
 ''``    \            `''-;    \ /
          \      .-'|     ````.' -
          |    .'  `--'''''-.. |/
          |  .'               \|
          |.'
"""


# Setup the version string globally
try:
    pkg_version = '%(prog)s {0}'.format(
        pkg_resources.get_distribution('zelda').version
    )
except pkg_resources.DistributionNotFound:
    pkg_version = '%(prog)s Development'
except Exception:
    pkg_version = '%(prog)s Unknown'


# Screen constants
COORDINATE_WIDTH = 160
COORDINATE_HEIGHT = 128
COORDINATE_SIZE = (COORDINATE_WIDTH, COORDINATE_HEIGHT)
SCREEN_MULTIPLIER = 4
SCREEN_WIDTH = COORDINATE_WIDTH*SCREEN_MULTIPLIER  # 640  # 480
SCREEN_HEIGHT = (COORDINATE_HEIGHT+16)*SCREEN_MULTIPLIER  # 576  # 432
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
# Clock constants
TICKS_PER_SECOND = 60.
MAX_FPS = 60  # 60
USE_WAIT = True
MAX_FRAME_SKIP = 0
UPDATE_CALLBACK = None
FRAME_CALLBACK = None
CLOCK_SETTINGS = (
    TICKS_PER_SECOND,
    MAX_FPS,
    USE_WAIT,
    MAX_FRAME_SKIP,
    UPDATE_CALLBACK,
    FRAME_CALLBACK
)
# lambda: time.time())
# lambda: pygame.time.get_ticks()/1000.)
# Mask and string constants
COLORKEY = (64, 64, 192)


EXTENSION = '.wav'
GUI_MASK = ['gui']
GAME_MASK = ['game']
# Game Constants
TRANSITION_SPEED = 2  # Roughly a 1.5


def main():
    parser = argparse.ArgumentParser(description='Legend of Zelda')
    parser.add_argument(
        '-l',
        '--log-level',
        default='INFO',
        choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
        help='Logging level for command output.'
    )
    parser.add_argument(
        '-L',
        '--logfile',
        dest='logfile',
        default=None,
        help='Location to place a log of the process output'
    )
    parser.add_argument(
        '-V',
        '--version',
        dest='version',
        action='version',
        version=pkg_version,
        help='Display the version number.'
    )

    parsed_args = parser.parse_args()

    # Get logging related arguments & the configure logging
    if parsed_args.logfile:
        logfile = os.path.abspath(parsed_args.logfile)
    else:
        logfile = None

    # Don't bother with a file handler if we're not logging to a file
    handlers = ['console', 'filehandler'] if logfile else ['console', ]

    # The base logging configuration
    BASE_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'ConsoleFormatter': {
                '()': ColorFormatter,
                'format': '%(levelname)s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'FileFormatter': {
                '()': ColorStripper,
                'format': ("%(levelname)-8s: %(asctime)s '%(message)s' "
                           '%(name)s:%(lineno)s'),
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'ConsoleFormatter',
            },
        },
        'loggers': {
            'zelda': {
                'handlers': handlers,
                'level': parsed_args.log_level,
            },
            'pygame': {
                'handlers': handlers,
                'level': parsed_args.log_level,
            },
            'pyaudio': {
                'handlers': handlers,
                'level': parsed_args.log_level,
            },
        }
    }

    # If we have a log file, modify the dict to add in the filehandler conf
    if logfile:
        BASE_CONFIG['handlers']['filehandler'] = {
            'level': log_level,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': logfile,
            'formatter': 'FileFormatter',
        }

    # Setup the loggers
    dictConfig(BASE_CONFIG)

    global screen, game_state, game_surface, gui_surface, resource_manager
    global clock, game_scene, current_width, current_state, pause_state
    global pause_scene, game_map, overworld_sheet, hud

    pygame.init()
    pygame.register_quit(has_quit)

    LOG.info('#g<%s>', ZELDA_ASCII)

    # Set up the window
    LOG.debug('Setting up pygame window')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    LOG.debug('Width: #y<%s> - Height: #y<%s>', SCREEN_WIDTH, SCREEN_HEIGHT)
    game_state = engine.State()
    pause_state = engine.State()
    game_surface = engine.CoordinateSurface(
        (
            SCREEN_WIDTH,
            (SCREEN_HEIGHT / COORDINATE_HEIGHT) * COORDINATE_HEIGHT
        ),
        (
            COORDINATE_WIDTH,
            COORDINATE_HEIGHT,
        )
    )
    pause_surface = engine.CoordinateSurface(
        pygame.Rect(
            (0, 0),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        ),
        (
            COORDINATE_WIDTH,
            COORDINATE_HEIGHT,
        )
    )

    LOG.debug('Initializing HUD')
    hud = game.gui.HUD((SCREEN_WIDTH, SCREEN_HEIGHT))

    game_scene = engine.Scene((2560, 2048))
    pause_scene = engine.Scene((COORDINATE_WIDTH, COORDINATE_HEIGHT))
    game_state.add_scene('game', game_scene)
    pause_state.add_scene('pause', pause_scene)
    current_state = game_state
    game_scene.insert_view(game_surface, 'game_view', (0, 0))
    pause_scene.insert_view(
        pause_surface,
        'pause_view',
        (0, 0),
        (0, 0),
        (0, 0, 0, 0)
    )
    current_width = 480

    # Set up the clock
    clock = engine.GameClock(*CLOCK_SETTINGS)

    # Load the resources
    overworld_sheet = engine.Spritesheet(os.path.join(SPRITE_DIR, 'OverworldSheet.png'))
    enemy_sheet = engine.Spritesheet(os.path.join(SPRITE_DIR, 'Enemies.png'))

    resource_manager = engine.ResourceManager()

    resource_manager.add_spritesheet_strip_offsets(
        'overworld_tiles',
        overworld_sheet,
        (1, 1),
        600,
        24,
        (16, 16),
        1,
        1,
    )

    # Load enemy sprites
    resource_manager.add_spritesheet_strip_offsets(
        'octorok',
        enemy_sheet,
        (0, 0),
        9,
        9,
        (16, 16),
        0,
        0,
        (64, 64, 192)
    )

    resource_manager.add_font(
        'gui_font_small',
        os.path.join(FONT_DIR, 'ReturnofGanon.ttf'),
        20
    )
    resource_manager.add_font(
        'gui_font_large',
        os.path.join(FONT_DIR, 'ReturnofGanon.ttf'),
        46
    )

    # Music
    resource_manager.add_music(
        'overworld',
        os.path.join(MUSIC_DIR, '10. Overworld.wav')
    )
    resource_manager.add_music(
        'mabe_village',
        os.path.join(MUSIC_DIR, '11. Mabe Village.wav')
    )
    resource_manager.add_music(
        'mysterious_forest',
        os.path.join(MUSIC_DIR, '16. Mysterious Forest.wav')
    )
    # resource_manager.play_music('mabe_village')

    # Sounds
    game_map = engine.Map(
        os.path.join(RESOURCE_DIR, 'worlds/grassworldtmx'),
        os.path.join(SPRITE_DIR, 'OverworldSheet.png'),
    )

    while True:
        if not run_game():
            LOG.info('Quitting game.')
            break


def run_game():
    global link, camera, camera_movement, \
        link_movement, room_movement, var, game_map, force_exit, textboxes
    var = {
        'game_ticks': 0,
        'can_move': True,
        'move_camera': False,
        'camera_increment': 0,
        'clear_previous': False,
        'current_frame': 0,
        'animation_frames': 0,
        'camera_position': (1, 11),
        'short_grass_drawn': False,
        'invert': True
    }

    force_exit = False
    textboxes = []
    link = game.link.Link()
    camera = engine.GameObject(
        collision_rect=(
            pygame.Rect(
                (0, 0),
                (COORDINATE_WIDTH, COORDINATE_HEIGHT)
            )
        ),
        handle_collisions=True,
        object_type='camera',
        persistent=True
    )
    camera.collision_rect.center = camera.rect.center
    link.set_animation('link_walk_down')

    camera_movement = {
        0: (TRANSITION_SPEED*(COORDINATE_WIDTH/32), 0),
        1: (0, -TRANSITION_SPEED*(COORDINATE_HEIGHT/32)),
        2: (-TRANSITION_SPEED*(COORDINATE_WIDTH/32), 0),
        3: (0, TRANSITION_SPEED*(COORDINATE_HEIGHT/32))
    }
    room_movement = {
        0: (TRANSITION_SPEED*.5, 0),
        1: (0, -TRANSITION_SPEED*.5),
        2: (-TRANSITION_SPEED*.5, 0),
        3: (0, TRANSITION_SPEED*.5)
    }

    game_scene.insert_object_centered(
        link,
        (
            112 + COORDINATE_WIDTH * var['camera_position'][0],
            80 + COORDINATE_HEIGHT * var['camera_position'][1]
        )
    )
    game_scene.insert_object_centered(
        camera,
        (
            80 + COORDINATE_WIDTH * var['camera_position'][0],
            64 + COORDINATE_HEIGHT * var['camera_position'][1]
        )
    )
    current_state.update_collisions()
    game_scene.center_view_on_object('game_view', camera)
    game_map.build_world(game_scene, game_scene.view_rects['game_view'])
    build_world()

    # Game loop
    while True:
        if force_exit:
            LOG.warning('Exit forced, ending run_game')
            return False
        clock.tick()
        if clock.update_ready:
            update_clock()
            update_logic()
            resource_manager.update_sound()

        if clock.frame_ready:
            # Draw functions
            draw_game()

            # Update display
            pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            handle_event(event)

        pygame.display.set_caption('FPS: ' + str(clock.fps))


def update_clock():
        """Update function for use with GameClock."""
        global var, clock

        var['game_ticks'] += 1
        if var['game_ticks'] >= clock.ticks_per_second:
            # set_caption()
            var['game_ticks'] = 0


def update_logic():
    global camera_movement, link_movement, room_movement, \
        var
    current_state.update_collisions()
    if current_state == game_state:
        game_scene.center_view_on_object('game_view', camera)
        link.update(0)

        if var['clear_previous']:
            var['clear_previous'] = False
            var['invert'] = True
            game_map.clear_tiles(game_scene, game_scene.view_rects['game_view'], kill_all=True)
            link.controllable = True
            game_scene.update_all = False
        if var['can_move']:
            update_room()
        if var['move_camera']:
            move_camera()


def draw_game():
    current_state.update(colorkey=COLORKEY)
    draw_gui()
    for scene_key in current_state.scenes.keys():  # Draws each scene in the current state to the screen
        if current_state.scenes[scene_key].active:
            for surface_key in current_state.scenes[scene_key].views.keys():
                surface = current_state.scenes[scene_key].views[surface_key]
                if surface.active:
                    screen.blit(surface.draw(), current_state.scenes[scene_key].view_draw_positions[surface_key])
    if current_state == pause_state:
        message = resource_manager.fonts['default'].render('PAUSE', True, (255, 255, 255, 255))
        screen.blit(message, (SCREEN_WIDTH/2-message.get_rect().width/2, SCREEN_HEIGHT/2-message.get_rect().height/2))
    screen.blit(hud, (0, SCREEN_HEIGHT-(SCREEN_HEIGHT/COORDINATE_HEIGHT)*16))
    return


def draw_gui():
    hud.fill((255, 255, 139, 255))
    text_b = resource_manager.fonts['gui_font_small'].render('B', False, (0, 0, 0, 255))
    text_a = resource_manager.fonts['gui_font_small'].render('A', False, (0, 0, 0, 255))
    text_brackets = resource_manager.fonts['gui_font_large'].render('[    ]', False, (0, 0, 0, 255))
    hud.blit(text_b, (3, 3))
    hud.blit(text_brackets, (19, 3))
    hud.blit(text_a, (120, 3))
    hud.blit(text_brackets, (136, 3))
    for textbox in textboxes:
        textbox.update_text()
        if game_surface.check_position(link)[1] > COORDINATE_HEIGHT/2:
            game_surface.blit(textbox, (8*SCREEN_MULTIPLIER, 8*SCREEN_MULTIPLIER))
        else:
            game_surface.blit(textbox, (8*SCREEN_MULTIPLIER, (COORDINATE_HEIGHT/2+16)*SCREEN_MULTIPLIER))


def handle_event(event):
    global current_state, screen, var, textboxes
    # Quit the game
    if event.type == KEYDOWN:
        key = event.key
        if link.controllable and var['can_move']:
            if key == K_SPACE:
                for game_object in game_scene.check_collision_rect_objects(link.interaction_rect):
                    if game_object.object_type == 'sign':
                        var['can_move'] = False
                        justify = 'center'
                        if 'justify' in game_object.properties:
                            justify = game_object.properties['justify']
                        textboxes.append(game.gui.TextBox(game_object.properties['text'], SCREEN_SIZE, COORDINATE_SIZE, justify))
            elif key == K_g:
                link.shield = not link.shield
                if link.shield:
                    link.set_animation(link.link_shield_walk[link.facing], 0)
                else:
                    link.set_animation(link.link_walk[link.facing], 0)
            elif key == K_n:
                link.no_clip = not link.no_clip
        if key == K_TAB:
            if current_state == game_state:
                current_state = pause_state
            else:
                current_state = game_state
        if key == K_SPACE:
            for textbox in textboxes:
                if textbox.waiting:
                    textbox.scrolling = True
                if textbox.finished:
                    textboxes.remove(textbox)
                    del textbox
                    game_scene.update_all = True
                    game_scene.update('game_view')
                    game_scene.update_all = False
                    var['can_move'] = True
        if key == K_ESCAPE:
            terminate()
        if key == K_r:
            game_scene.update_screen_coordinates('game_view', (640, 576))
            screen = pygame.display.set_mode((640, 576))
        if key == K_t:
            game_scene.update_screen_coordinates('game_view', (480, 432))
            screen = pygame.display.set_mode((480, 432))
        if key == K_f:
            pygame.display.toggle_fullscreen()
    if var['can_move']:
        link.handle_event(game_scene, event)
    return


def load_room():
    global var, game_scene, game_map
    link.controllable = False
    var['invert'] = False
    if link.direction == 0:
        new_rect = game_scene.view_rects['game_view'].copy()
        new_rect[0] += var['camera_increment']
        game_map.build_world(game_scene, new_rect, current_frame=var['current_frame'])
    if link.direction == 1:
        new_rect = game_scene.view_rects['game_view'].copy()
        new_rect[1] -= var['camera_increment']
        game_map.build_world(game_scene, new_rect, current_frame=var['current_frame'])
    if link.direction == 2:
        new_rect = game_scene.view_rects['game_view'].copy()
        new_rect[0] -= var['camera_increment']
        game_map.build_world(game_scene, new_rect, current_frame=var['current_frame'])
    if link.direction == 3:
        new_rect = game_scene.view_rects['game_view'].copy()
        new_rect[1] += var['camera_increment']
        game_map.build_world(game_scene, new_rect, current_frame=var['current_frame'])
    build_world()


def build_world():
    global game_map
    for game_object in game_scene.list_objects():
        for object_property in game_object.properties.keys():
            if object_property == 'type':
                object_type = game_object.properties[object_property]
                if object_type == 'octorok_spawn':
                    game_scene.remove_object(game_object)
                    game_scene.insert_object(game.octorok.Octorok(resource_manager), game_object.position)


def test_music_change():
    for game_object in game_scene.check_object_collision_objects(link):
        if game_object.object_type == 'music_zone':
            if resource_manager.current_key != game_object.properties['song']:
                resource_manager.play_music(game_object.properties['song'])


def update_room():
    update_player()
    update_animated_tiles()
    update_objects()


def update_player():
    global var, resource_manager

    if var['can_move']:
        link.handle_input(game_scene)
    link.update_state(game_scene)

    # Check for collision with edge of screen
    if camera.position[0] - link.position[0] > COORDINATE_WIDTH/2:
        link.direction = 2
        var['camera_increment'] = COORDINATE_WIDTH
        var['move_camera'] = True
        var['can_move'] = False
        load_room()
        return
    elif link.position[0]+link.body_rect.width - camera.position[0] > COORDINATE_WIDTH/2:
        link.direction = 0
        var['camera_increment'] = COORDINATE_WIDTH
        var['move_camera'] = True
        var['can_move'] = False
        load_room()
        return
    elif camera.position[1] - link.position[1] > COORDINATE_HEIGHT/2:
        link.direction = 1
        var['camera_increment'] = COORDINATE_HEIGHT
        var['move_camera'] = True
        var['can_move'] = False
        load_room()
        return
    elif link.position[1]+link.body_rect.height - camera.position[1] > COORDINATE_HEIGHT/2:
        link.direction = 3
        var['camera_increment'] = COORDINATE_HEIGHT
        var['move_camera'] = True
        var['can_move'] = False
        load_room()
        return


def update_animated_tiles():
    global game_scene, var

    for game_object in game_scene.list_objects():
        if game_object.animate:
            game_object.update()
            if var['current_frame'] != game_object.animation_frame and game_object.sync:
                var['current_frame'] = game_object.animation_frame


def update_objects():
    global game_scene, var, link

    for game_object in game_scene.list_objects():
        if game_object.object_type in link.big_grass or game_object.object_type in link.short_grass:
            if (link.state == 'SwordState' or link.state == 'SwordSpinState') and link._state.sword.handle_collisions:
                if game_object.get_global_rect().colliderect(link._state.sword.get_global_collision_rect()):
                    position = game_object.position
                    game_scene.remove_object(game_object)
                    game_scene.insert_object(game.specialtiles.GroundTile(resource_manager), position)
                    game_scene.insert_object_centered(game.effects.CutGrass(), (position[0]-8, position[1]-8))
                    if link.state == 'SwordState':
                        resource_manager.play_sound('grass_cut')
        if game_object._state is not None and game_object != link:
            game_object._state.update(game_object, game_scene)
        if game_object.call_special_update:
            game_object.special_update(game_scene)


def move_camera():
    if var['camera_increment'] > 0:
        game_scene.update_all = True
        camera.increment(camera_movement[link.direction])
        link.increment(room_movement[link.direction])
        if link.state == 'SwordChargeState':
            link._state.sword.increment(room_movement[link.direction])
        if link.direction == 1 or link.direction == 3:
            var['camera_increment'] -= abs(camera_movement[link.direction][1])
        else:
            var['camera_increment'] -= abs(camera_movement[link.direction][0])
    else:
        var['move_camera'] = False
        var['can_move'] = True
        var['clear_previous'] = True
        test_music_change()


def terminate():
    global force_exit
    force_exit = True


def has_quit():
    LOG.info('Pygame has quit')
    return


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        terminate()
        # Write a nice message to stderr
        sys.stderr.write(
            u"\n\033[91m\u2717 Operation canceled by user.\033[0m\n"
        )
        sys.exit(errno.EINTR)
    sys.exit()
