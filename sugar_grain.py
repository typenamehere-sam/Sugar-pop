import pygame as pg
from Box2D.b2 import dynamicBody, polygonShape
from settings import SCALE, HEIGHT

class sugar_grain:
    def __init__(self, world, x, y, friction=0.3):
        """
        Initialize a sugar grain as a small dynamic body in Box2D.
        
        :param world: The Box2D world where the grain will be created.
        :param x: Initial x position in Pygame coordinates.
        :param y: Initial y position in Pygame coordinates.
        """
        # Create the dynamic body in Box2D at the specified position
        self.body = world.CreateDynamicBody(position=(x / SCALE, y / SCALE))

        # Add a small 2x2 polygon fixture to the body
        box_fixture = polygonShape(box=(1 / SCALE, 1 / SCALE))
        self.body.CreateFixture(shape=box_fixture, density=1.0, friction=friction)
        
    def update(self):
        """
        Update method for SugarGrain.
        In this case, Box2D handles the physics, so nothing is needed here.
        """
        pass

    def draw(self, screen):
        """
        Draw the sugar grain on the Pygame screen.
        
        :param screen: The Pygame surface to draw the grain on.
        """
        # Get the position of the grain in Pygame coordinates
        pos = self.body.position
        screen_x = pos.x * SCALE
        screen_y = HEIGHT - pos.y * SCALE
        pg.draw.rect(screen, pg.Color('white'), (screen_x - 1, screen_y - 1, 2, 2))

    def destroy(self, world):
        """
        Remove the sugar grain from the Box2D world.
        
        :param world: The Box2D world to destroy the grain's body from.
        """
        world.DestroyBody(self.body)
