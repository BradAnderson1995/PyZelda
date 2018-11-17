import os
import logging
import pygame
from zelda import engine
from zelda import FONT_DIR

LOG = logging.getLogger(__name__)


class HUD(engine.CoordinateSurface):
    def __init__(self, screen_size):
        engine.CoordinateSurface.__init__(self, pygame.Rect((0, 0), (screen_size[0], screen_size[1]/8)), (160, 16))


class TextBox(engine.CoordinateSurface):
    def __init__(self, text, screen_size, coordinate_size, justify='center'):
        self.scale = (
            screen_size[0] / coordinate_size[0],
            screen_size[1] / (coordinate_size[1] + 16)
        )
        self.width = 144 * self.scale[0]
        self.height = 40 * self.scale[1]
        engine.CoordinateSurface.__init__(self, pygame.Rect((0, 0), (self.width, self.height)), (144, 40))
        self.fill((0, 0, 0, 255))
        self.resource_manager = engine.ResourceManager()
        self.resource_manager.add_font(
            'game_text',
            os.path.join(FONT_DIR, 'zeldadxt.ttf'),
            int(self.scale[1]*12)
        )
        self.text = str(text)
        self.text_speed = 5
        self.frame_counter = 0
        self.next_letter = False
        self.justify = justify
        self.lines = []
        self.current_line = 0
        self.current_letter = 0
        self.waiting = False
        self.scrolling = False
        self.scroll_frame = 0
        self.finished = False
        self.rendered_letters = []
        self.line_starts = []
        self.letter_spacing = 8 * self.scale[0]

        line = ''
        for char in self.text:
            if char != '\\':
                line += char
            else:
                self.lines.append(line)
                line = ''
        self.lines.append(line)
        if self.justify == 'center':
            for line in self.lines:
                letters = len(line)
                line_start = self.width/2 - (letters/2)*self.letter_spacing
                self.line_starts.append(line_start)
        elif self.justify == 'left':
            for i in xrange(0, len(self.lines)):
                self.line_starts.append(8*self.scale[0])

    def update_text(self):
        self.frame_counter += 1
        if self.frame_counter >= self.text_speed:
            self.next_letter = True
        if not self.finished and not self.waiting and not self.scrolling:
            if self.next_letter:
                self.rendered_letters.append(
                    self.resource_manager.fonts['game_text'].render
                    (
                        self.lines[self.current_line][self.current_letter],
                        False,
                        (255, 255, 139, 255)
                    )
                )
                self.current_letter += 1
                self.draw_letters()
                if self.current_letter == len(self.lines[self.current_line]):
                    self.current_letter = 0
                    self.current_line += 1
                    if self.current_line % 2 == 0:
                        self.waiting = True
                    if self.current_line == len(self.lines):
                        self.finished = True
                    if self.current_line > 1 and not self.waiting:
                        self.scrolling = True
                self.frame_counter = 0
                self.next_letter = False
        elif not self.finished and self.waiting:
            pass
            # TODO: Flash the down arrow
        if self.scrolling and self.next_letter:
            self.scroll_up()
            self.frame_counter = 0
            self.next_letter = False

    def draw_letters(self):
        # Draw all of the letters up to the current point
        self.fill((0, 0, 0, 255))
        if self.current_line >= 1:
            line = 0
            draw_line = 0
            letters = len(self.lines[self.current_line-1]) + self.current_letter
            letter = 0
            for i in xrange(0, letters):
                try:
                    self.blit(self.rendered_letters[i],
                              (self.line_starts[self.current_line-1+line] + letter*self.letter_spacing, 6*self.scale[0]+16*self.scale[0]*draw_line))
                except IndexError:
                    LOG.error('Error blitting letters: %s %s',
                              self.current_line, self.current_line - 1 + line)
                letter += 1
                if i == len(self.lines[self.current_line-1]) - 1:
                    draw_line = 1
                    line += 1
                    letter = 0
        elif self.current_line == 0:
            for i in xrange(0, self.current_letter):
                self.blit(self.rendered_letters[i], (self.line_starts[0] + i*self.letter_spacing, 6*self.scale[0]))

    def scroll_up(self):
        # TODO: Scroll text up and delete previous line
        # Scrolls up in two increments, deleting previous line on first increment
        if self.scroll_frame == 0:
            # Deletes line no longer visible
            length = len(self.lines[self.current_line-2])
            for i in xrange(0, length):
                self.rendered_letters.pop(0)
        # Scroll up two increments
        if self.scroll_frame < 6 and self.scroll_frame % 2 == 0:
            scroll_surface = self.copy()
            self.fill((0, 0, 0, 255))
            self.blit(scroll_surface, (0, -8 * self.scale[1]))
            self.scroll_frame += 1
        else:
            self.waiting = False
            self.scrolling = False
            self.scroll_frame = 0
