import os

# Get the base resources folder
current_folder = os.path.dirname(__file__)
RESOURCE_DIR = os.path.join(current_folder, 'resources')

# Important game file subfolders
FONT_DIR = os.path.join(RESOURCE_DIR, 'font')
MUSIC_DIR = os.path.join(RESOURCE_DIR, 'music', 'wav')
SOUND_DIR = os.path.join(RESOURCE_DIR, 'sound')
SPRITE_DIR = os.path.join(RESOURCE_DIR, 'sprite')


__all__ = (
    'FONT_DIR',
    'MUSIC_DIR',
    'RESOURCE_DIR',
    'SOUND_DIR',
    'SPRITE_DIR',
)
