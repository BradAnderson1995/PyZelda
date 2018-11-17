from setuptools import setup, find_packages


setup(
    name='py-zelda',
    version='1.0.0',
    description='The Legend of Zelda: Link\'s Awakening Remake in python',
    url='https://github.com/branderson/PyZelda',
    author='Bradley Anderson',
    author_email='brad@branderson.io',
    keywords='game zelda engine pygame',
    packages=find_packages('src'),
    package_dir={"": "src"},
    install_requires=[
        'log-color',
        'pyaudio',
        'pygame',
    ],
    entry_points={
        'console_scripts': ['zelda = zelda.main:main']
    },
    package_data={
        'zelda': [
            'resources/*.*',
            'resources/fixtures/*.json',
            'resources/font/*.tty',
            'resources/music/*.*',
            'resources/music/wav/*.wav',
            'resources/music/ogg/*.ogg',
            'resources/sound/*.ogg',
            'resources/sprite/*.*',
            'resources/worlds/*.*',
        ],
    }
)
