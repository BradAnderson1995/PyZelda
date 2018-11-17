import logging
import pygame
from resourceman import ResourceManager
from spritesheet import Spritesheet
from gameobject import GameObject
import xml.etree.ElementTree as ET

LOG = logging.getLogger(__name__)


class Map(object):
    def __init__(self, filename, tile_set):
        """Takes an XML world file and a tile set and creates a map from it"""
        # Load the tile set
        self.resource_manager = ResourceManager()
        self.object_tiles = {}
        self.object_properties = {}
        self.tile_set = Spritesheet(tile_set)  # Could eventually allow for multiple tile sets by making a list
        # TODO: Make spritesheet size independent of class
        self.resource_manager.add_spritesheet_strip_offsets('tile_set', self.tile_set, (1, 1), 600, 24, (16, 16), 1, 1)

        # Read the XML file
        tree = ET.parse(filename)
        root = tree.getroot()
        self.width = int(root.get('width'))
        self.height = int(root.get('height'))
        self.tile_width = int(root.get('tilewidth'))
        self.tile_height = int(root.get('tileheight'))

        # Read in the special tiles
        self.special_tiles = {}
        for tileset in root.findall('tileset'):
            for tile in tileset.findall('tile'):
                tile_properties = {}
                for tile_property in tile.find('properties').findall('property'):
                    tile_properties[tile_property.get('name')] = tile_property.get('value')
                self.special_tiles[int(tile.get('id'))] = tile_properties

        # Read in the layers
        self.layers = {}

        for layer in root.findall('layer'):
            LOG.debug('Layer: %s', layer.get('name'))
            tile_list = []
            for tile in layer.find('data').findall('tile'):
                LOG.debug('Tile: %s', tile.get('gid'))
                tile_list.append(int(tile.get('gid')))
            self.layers[layer.get('name')] = tile_list

        # Read in the collision boxes
        self.object_layers = {}

        for layer in root.findall('objectgroup'):
            rect_list = []
            rect_index = ''
            for object_rect in layer.findall('object'):
                try:
                    current_rect = pygame.Rect(int(object_rect.get('x')),  # /self.tile_width,
                                               int(object_rect.get('y')),  # /self.tile_height,
                                               int(object_rect.get('width')),  # /self.tile_width,
                                               int(object_rect.get('height')))  # /self.tile_height))
                    rect_list.append(current_rect)
                    rect_index = str(current_rect[0]) + ' ' + str(current_rect[1]) + ' ' + str(current_rect[2]) + ' ' + str(current_rect[3])
                except TypeError:
                    LOG.exception(
                        'Problem loading object at %s, %s',
                        str(int(object_rect.get('x'))/self.tile_width),
                        str(int(object_rect.get('y'))/self.tile_height),
                    )
                current_properties = {}
                if object_rect.get('type') is not None:
                    current_properties['type'] = object_rect.get('type')
                if object_rect.find('properties') is not None:
                    for object_property in object_rect.find('properties').findall('property'):
                        current_properties[object_property.get('name')] = object_property.get('value')
                if 'layer' not in current_properties.keys():
                    current_properties['layer'] = 0
                self.object_properties[rect_index] = current_properties
            self.object_layers[layer.get('name')] = rect_list
            for layer_property in layer.findall('property'):
                if layer_property.get('name') == 'tile':
                    self.object_tiles[layer.get('name')] = int(layer_property.get('value'))

    def get_tile_index(self, layer_name, x_tile, y_tile):
        index = self.width*y_tile+x_tile
        try:
            return self.layers[layer_name][index]-1
        except IndexError:
            return 0

    def build_world(self, scene, view_rect=None, current_frame=0):
        LOG.debug('Building world...')
        objects = 0
        tiles = 0
        if view_rect is None:
            row = 0
            for layer_name in self.layers.keys():
                while row < self.height:
                    for tile in xrange(0, self.width):
                        current_tile = self.get_tile_index(layer_name, tile, row)
                        if current_tile != -1:
                            is_special_tile = False
                            for special_tile in self.special_tiles.keys():
                                if current_tile == special_tile:
                                    is_special_tile = True
                            if is_special_tile:
                                scene.insert_object(GameObject(self.resource_manager.get_images('tile_set')
                                                               [current_tile], -1000, object_type=layer_name,
                                                               properties=self.special_tiles[current_tile],
                                                               tile_id=current_tile, sync=True),
                                                    (16*tile, 16*row))
                            else:
                                scene.insert_object(GameObject(self.resource_manager.get_images('tile_set')
                                                               [current_tile], -1000, object_type=layer_name,
                                                               tile_id=current_tile),
                                                    (16*tile, 16*row))
                        LOG.debug('Row: #y<%s> - Tile: #y<%s>', row, tile)
                    row += 1
        else:
            tile_rect = (view_rect.x/self.tile_width, view_rect.y/self.tile_height,
                         view_rect.width/self.tile_width, view_rect.height/self.tile_height)

            LOG.debug('Rectangle: #y<%s %s %s %s>',
                      view_rect[0], view_rect[1], view_rect[2], view_rect[3])

            # Build the map tiles
            for layer_name in self.layers.keys():
                row = 0
                while row < tile_rect[3]:
                    for tile in xrange(0, tile_rect[2]):
                        current_tile = self.get_tile_index(layer_name, tile_rect[0]+tile, tile_rect[1]+row)
                        if current_tile != -1:
                            is_special_tile = False
                            for special_tile in self.special_tiles.keys():
                                if current_tile == special_tile:
                                    is_special_tile = True
                            if is_special_tile:
                                animated = False
                                frames = 0
                                # for object_property in self.special_tiles[current_tile].keys():
                                #     if object_property == "animate":
                                #         animated = True
                                #         frames = int(self.special_tiles[current_tile][object_property])
                                if 'animate' in self.special_tiles[current_tile]:
                                    animated = True
                                    frames = int(self.special_tiles[current_tile]['animate'])
                                if animated:
                                    images = []
                                    for x in xrange(current_tile, current_tile + frames):
                                        images.append(self.resource_manager.get_images('tile_set')[x])
                                    scene.insert_object(GameObject(images, -1000, object_type=layer_name,
                                                                   properties=self.special_tiles[current_tile],
                                                                   tile_id=current_tile, animate=True,
                                                                   current_frame=current_frame, sync=True),
                                                        (16*(tile_rect[0]+tile), 16*(tile_rect[1]+row)))
                                else:
                                    scene.insert_object(GameObject(self.resource_manager.get_images('tile_set')
                                                                   [current_tile], -1000, object_type=layer_name,
                                                                   properties=self.special_tiles[current_tile],
                                                                   tile_id=current_tile),
                                                        (16*(tile_rect[0]+tile), 16*(tile_rect[1]+row)))
                            else:
                                # Allow it to determine whether objects already exist and just make them visible if they do
                                scene.insert_object(GameObject(self.resource_manager.get_images('tile_set')
                                                               [current_tile], -1000, object_type=layer_name,
                                                               tile_id=current_tile),
                                                    (16*(tile_rect[0]+tile), 16*(tile_rect[1]+row)))
                            tiles += 1
                        LOG.debug('Row: #y<%s> - Tile: #y<%s>', row, tile)
                    row += 1

            # Build the object layers
            for layer_name in self.object_layers.keys():
                for object_rect in self.object_layers[layer_name]:
                    if object_rect.colliderect(view_rect):  # tile_rect):
                        rect_index = str(object_rect[0]) + ' ' + str(object_rect[1]) + ' ' + str(object_rect[2]) + ' ' + str(object_rect[3])
                        scene.insert_object(GameObject(collision_rect=pygame.Rect(0, 0, object_rect[2], object_rect[3]),
                                                       handle_collisions=True, object_type=layer_name, visible=False,
                                                       properties=self.object_properties[rect_index],
                                                       layer=self.object_properties[rect_index]['layer']),
                                            (object_rect[0], object_rect[1]))
                        objects += 1
        LOG.debug('Added tiles: #g<%s>', tiles)
        LOG.debug('Added objects: #g<%s>', objects)
        LOG.debug('Ending build.')

    def clear_tiles(self, scene, view_rect, kill_all=False):
        LOG.debug('Starting to clear tiles...')
        self.clear_objects(scene, view_rect)
        objects = 0
        for coordinate in scene.coordinate_array.keys():
            for game_object in scene.coordinate_array[coordinate]:
                if game_object.object_type == 'Map Tiles':
                    object_rect = pygame.Rect(scene.check_position(game_object), (game_object.rect.width,
                                                                                  game_object.rect.height))
                    if not object_rect.colliderect(view_rect):
                        if kill_all:
                            scene.remove_object(game_object)
                        else:
                            game_object.visible = False
                    objects += 1
        LOG.debug('Tiles Cleared: #y<%s>', objects)

    @staticmethod
    def clear_objects(scene, view_rect):
        for coordinate in scene.coordinate_array.keys():
            for game_object in scene.coordinate_array[coordinate]:
                if not game_object.persistent and game_object.object_type != 'Map Tiles':
                    object_rect = pygame.Rect(scene.check_position(game_object), (game_object.rect.width,
                                                                                  game_object.rect.height))
                    if not object_rect.colliderect(view_rect):
                        scene.remove_object(game_object)
