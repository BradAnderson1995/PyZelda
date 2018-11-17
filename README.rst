PyZelda
#######

About
=====
Remake of The Legend of Zelda: Link's Awakening built on top of a custom engine
I wrote in Python.

PyZelda is written in Python 2.7 as I had not yet switched to Python 3 when I
wrote it. It is  unfinished, but contains a large portion of the overworld, as
well as many functional signs and text boxes, and some enemies. PyZelda was
mainly intended as an example game to test and demonstrate my Python game
engine and was never intended to be a full remake. You're free to do whatever
you want with PyZelda, and I'm no longer actively developing it.

I used PyGame for my windowing and rendering, and PyAudio for sound and music.
I didn't use PyGame's sound modules because I had issues with them.

Installation
============
You may have to install PyGame for Python 2 for your distribution before
installing PyZelda because PyGame has some dependencies that cannot be
installed through a standard python setup.

PyZelda on Windows doesn't seem to work at this time and I haven't gotten
around to getting it to work yet. I'll probably do that at some point in the
future, but for now it's best to run it on Linux. If you want to try getting it
to work on Windows, more power to you.



Using git
---------
.. code-block:: bash

    $ git clone https://github.com/branderson/PyZelda
    $ cd PyZelda

    # To install (requires setuptools)
    $ python2 setup.py install
    $ PyZelda

    # To run from source (requires pygame and pyaudio to be installed):
    $ python2 src/main.py
