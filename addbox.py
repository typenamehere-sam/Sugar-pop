import pygame as pg
import Box2D  # Import Box2D library
from Box2D.b2 import (world, polygonShape, staticBody, dynamicBody)
import sys
from settings import *
import random

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

        # Create static floor at the bottom of the screen
        self.floor_body = self.world.CreateStaticBody(
            position=(WIDTH / 2 / SCALE, 10 / SCALE),  # Floor positioned above the bottom
            shapes=polygonShape(box=(WIDTH / 2 / SCALE, 5 / SCALE))  # Floor width/height adjusted for SCALE
        )

        self.blocks = []
        
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
        
        # Check for blocks to remove, but only every 60 frames
        if self.iter == 60:
            self.iter = 0
            for block in self.blocks[:]:  # Use a copy of the list to avoid modifying while iterating
                if block.position.y * SCALE < 0:
                    self.remove_block(block)

        pg.display.set_caption(f'fps: {self.clock.get_fps():.1f}')

    def add_block(self, x, y):
        """Add a new dynamic block at a specified (x, y) location."""
        dynamic_body = self.world.CreateDynamicBody(position=(x, y))
        box_fixture = dynamic_body.CreatePolygonFixture(box=(25 / SCALE, 25 / SCALE), density=1.0, friction=0.3)
        dynamic_body.angularVelocity = random.randint(-20, 20)  # Initial spin
        self.blocks.append(dynamic_body)
        
    def remove_block(self, block):
        """Remove a block from the world and the blocks list."""
        self.world.DestroyBody(block)
        self.blocks.remove(block)

    def draw_hud(self):
        """Draw the HUD displaying the number of blocks."""
        # Prepare the text surface
        text_surface = self.font.render(f'{len(self.blocks)}', True, (255, 255, 255))
        # Draw the text surface on the screen
        self.screen.blit(text_surface, (10, 10))  # Position at top-left corner

    def draw(self):
        # Clear the screen
        self.screen.fill('black')

        # Draw each block in the list
        for block in self.blocks:
            for fixture in block.fixtures:
                shape = fixture.shape
                vertices = [(block.transform * v) for v in shape.vertices]
                vertices = [(v[0] * SCALE, HEIGHT - (v[1] * SCALE)) for v in vertices]
                pg.draw.polygon(self.screen, (255, 255, 0), vertices)

        # Draw the floor as a line
        floor_vertices = [(self.floor_body.transform * v) for v in self.floor_body.fixtures[0].shape.vertices]
        floor_vertices = [(v[0] * SCALE, HEIGHT - (v[1] * SCALE)) for v in floor_vertices]
        pg.draw.polygon(self.screen, (255, 0, 0), floor_vertices)


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
                # Get mouse position and add a new block at that location
                mouse_x, mouse_y = pg.mouse.get_pos()
                # Convert Pygame coordinates to Box2D coordinates
                box2d_x, box2d_y = mouse_x / SCALE, (HEIGHT - mouse_y) / SCALE
                self.add_block(box2d_x, box2d_y)
                
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
