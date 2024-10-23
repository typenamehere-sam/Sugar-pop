#############################################################
# Module Name: Pygame Starter
# Project: 
# Date: 
# By: Brett W. Huffman
# Description: Change all these items for your implementation
#############################################################

# Remove the PyGame starter text - should be first in this file
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame as pg
import sys
from settings import *


# Main game object
class Game:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        # Create a new game
        pass


    def update(self):
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'fps: {self.clock.get_fps():.1f}')

    def draw(self):
        # Draw to the main Screen
        self.screen.fill('black')
        # Drawn screen to forefront
        pg.display.update()

    def check_events(self):
        # Check for keyboard events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        # Called once to manage whole game
        while True:
            self.check_events()
            self.update()
            self.draw()


def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()