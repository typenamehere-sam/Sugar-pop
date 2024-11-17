import pygame as pg
from Box2D.b2 import staticBody
from settings import *

class static_item:
    def __init__(self, world, x1, y1, x2, y2, color='gray', line_width=3, friction=0.3, restitution=0.5):
        """
        Initialize a static line segment in Box2D between two points (x1, y1) and (x2, y2).
        """
        self.color = color  # Color for rendering in Pygame
        self.line_width = line_width
        self.body = world.CreateStaticBody()  # Create a static body in the Box2D world

        # Create an edge fixture (line segment) between two points
        self.body.CreateEdgeFixture(vertices=[(x1 / SCALE, y1 / SCALE), (x2 / SCALE, y2 / SCALE)],
                                    friction=friction, restitution=restitution)

    def draw(self, screen):
        """
        Draw the static line segment on the Pygame screen.
        """
        # Convert Box2D coordinates to Pygame screen coordinates
        start = (self.body.fixtures[0].shape.vertices[0][0] * SCALE, HEIGHT - self.body.fixtures[0].shape.vertices[0][1] * SCALE)
        end = (self.body.fixtures[0].shape.vertices[1][0] * SCALE, HEIGHT - self.body.fixtures[0].shape.vertices[1][1] * SCALE)

        # Draw the line on the Pygame screen
        pg.draw.line(screen, pg.Color(self.color), start, end, self.line_width)
