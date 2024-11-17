import pygame as pg
import Box2D  # Import Box2D library
from Box2D.b2 import (world, polygonShape, staticBody, dynamicBody)
import sys
from settings import *

class Game:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()

        # Create a Box2D world with gravity
        self.world = world(gravity=(0, -9.8), doSleep=True)

        # Create static floor at the bottom of the screen
        self.floor_body = self.world.CreateStaticBody(
            position=(WIDTH / 2 / SCALE, 10 / SCALE),  # Floor positioned above the bottom
            shapes=polygonShape(box=(WIDTH / 2 / SCALE, 5 / SCALE))  # Floor width/height adjusted for SCALE
        )

        # Create a dynamic box that will fall due to gravity
        self.dynamic_body = self.world.CreateDynamicBody(position=(500 / SCALE, HEIGHT / SCALE))
        box_fixture = self.dynamic_body.CreatePolygonFixture(box=(25 / SCALE, 25 / SCALE), density=1.0, friction=0.3)
        # Apply a constant torque to the dynamic body
#        self.dynamic_body.ApplyTorque(510.0, wake=True)  # Adjust the torque value as needed

        
    def update(self):

        # Calculate time since last frame
        delta_time = self.clock.tick(FPS) / 1000.0  # Convert milliseconds to seconds

        # Cap delta_time to prevent instability from large time steps
        time_step = min(delta_time, MAX_TIME_STEP)

        # Step the physics simulation forward with the calculated time_step
        vel_iters, pos_iters = 6, 2
        self.world.Step(time_step, vel_iters, pos_iters)

        pg.display.set_caption(f'fps: {self.clock.get_fps():.1f}')

    def draw(self):
        # Clear the screen
        self.screen.fill('black')

        # Draw the dynamic box
        for fixture in self.dynamic_body.fixtures:
            shape = fixture.shape
            # Convert Box2D vertices to scaled Pygame coordinates
            vertices = [(self.dynamic_body.transform * v) for v in shape.vertices]
            vertices = [(v[0] * SCALE, HEIGHT - (v[1] * SCALE)) for v in vertices]
            pg.draw.polygon(self.screen, (255, 255, 0), vertices)

        # Draw the floor as a line
        floor_vertices = [(self.floor_body.transform * v) for v in self.floor_body.fixtures[0].shape.vertices]
        floor_vertices = [(v[0] * SCALE, HEIGHT - (v[1] * SCALE)) for v in floor_vertices]
        pg.draw.polygon(self.screen, (255, 0, 0), floor_vertices)

        # Update the display
        pg.display.update()

    def check_events(self):
        # Check for keyboard events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

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
