import pygame as pg
import Box2D  # Import Box2D library
from Box2D.b2 import (world, polygonShape, staticBody, dynamicBody)
import sys
from settings import *
import random
import static_item
import dynamic_item
import sugar_grain
import bucket

class Game:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.iter = 0
        
        # Initialize font for HUD
        self.font = pg.font.SysFont(None, 36)  # Default font, size 36

        # Create a Box2D world with gravity
        self.world = world(gravity=(0, -9.8), doSleep=True)
        self.statics = []
        self.sugar_grains = []
        self.drawing_lines = []
        self.mouse_down = False
        self.current_line = None
        self.bucket = bucket.Bucket(self.world, BUCKET_X, BUCKET_Y, 20, 40)
        self.build_statics()
        self.new_level()

    def new_level(self):
        self.level_grain_dropping = False
        pg.time.set_timer(START_FLOW, 5 * 1000) # 5 second

    def build_statics(self):
#        lstatic = static_item.static_item(self.world, WIDTH // 2, 10, 50, 4, 'red')
        # Floor
        lstatic = static_item.static_item(self.world, 0, 0, WIDTH, 0, 'red', 5)
        self.statics.append(lstatic)
        # Left Wall
        lstatic = static_item.static_item(self.world, 0, 0, 0, HEIGHT, 'red')
        self.statics.append(lstatic)
        # Right Wall
        lstatic = static_item.static_item(self.world, WIDTH, 0, WIDTH, HEIGHT, 'red')
        self.statics.append(lstatic)
        # Ceiling
        lstatic = static_item.static_item(self.world, 0, HEIGHT, WIDTH, HEIGHT, 'red')
        self.statics.append(lstatic)
        
    def update(self):
        # Keep a overall iterator
        self.iter += 1
        
        # Calculate time since last frame
        delta_time = self.clock.tick(FPS) / 1000.0  # Convert milliseconds to seconds

        # Cap delta_time to prevent instability from large time steps
        time_step = min(delta_time, MAX_TIME_STEP)

        # Step the physics simulation forward with the calculated time_step
        vel_iters, pos_iters = 6, 2
        self.world.Step(time_step, vel_iters, pos_iters)
        
        # Update our game counter
        if self.iter == 60:
            self.iter = 0
            # for block in self.blocks[:]:  # Use a copy of the list to avoid modifying while iterating
            #     if block.position.y * SCALE < 0:
            #         self.remove_block(block)

        pg.display.set_caption(f'fps: {self.clock.get_fps():.1f}')
        
        # Drop sugar if needed
        if self.level_grain_dropping == True and self.iter % 20 == 0:
            # Create new sugar to drop
            new_sugar = sugar_grain.sugar_grain(self.world, LEVEL_START_POS[0], LEVEL_START_POS[1], 0.1)
            self.sugar_grains.append(new_sugar)
            # Check if its time to stop
            if len(self.sugar_grains) >= NUMBER_OF_GRAINS:
                self.level_grain_dropping = False

            # Calculate buckets count by counting 
            # each grains position
            self.bucket.count_reset()
            for grain in self.sugar_grains:
                self.bucket.collect(grain)
            
    def draw_hud(self):
        """Draw the HUD displaying the number of grains."""
        # Prepare the text surface
        text_surface = self.font.render(f'{NUMBER_OF_GRAINS-len(self.sugar_grains)} / {self.bucket.count}', True, (255, 255, 255))
        # Draw the text surface on the screen
        self.screen.blit(text_surface, (10, 10))  # Position at top-left corner

    def draw(self):
        # Clear the screen
        self.screen.fill('black')

        self.bucket.draw(self.screen)

        # Draw each block in the list
        for grain in self.sugar_grains:
            grain.draw(self.screen)

        # Draw the current dynamic line
        if self.current_line != None:
            self.current_line.draw(self.screen)
            
        for line in self.drawing_lines:
            line.draw(self.screen)
            
        for static in self.statics:
            static.draw(self.screen)

        # Draw the heads-up display
        self.draw_hud()
        
        # Update the display
        pg.display.update()

    def check_events(self):
        # Check for keyboard events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_down = True
                # Get mouse position and add a new block at that location
                mouse_x, mouse_y = pg.mouse.get_pos()
                self.current_line = dynamic_item.dynamic_item(self.world, 'blue')
                self.current_line.add_vertex(mouse_x, mouse_y)
                
            elif event.type == pg.MOUSEBUTTONUP:
                self.mouse_down = False
#                self.current_line.color('blue')
                self.drawing_lines.append(self.current_line)
                self.current_line = None
                
            elif event.type == pg.MOUSEMOTION and self.mouse_down:
                # Get mouse position
                mouse_x, mouse_y = pg.mouse.get_pos()
                if mouse_x == 0 or mouse_x == WIDTH or mouse_y == 0 or mouse_y == HEIGHT:
                    self.mouse_down = False
                if self.current_line != None and self.iter % 10 == 0:
                    self.current_line.add_vertex(mouse_x, mouse_y)

            elif event.type == START_FLOW:
                self.level_grain_dropping = True
                # Disable the timer after the first trigger
                pg.time.set_timer(START_FLOW, 0)
                
    def run(self):
        # Run the game loop
        while True:
            self.check_events()
            self.update()
            self.draw()

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()
