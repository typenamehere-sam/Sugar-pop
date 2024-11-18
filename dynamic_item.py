#############################################################
# Module Name: Sugar Pop Dynamic Item Module
# Project: Sugar Pop Program
# Date: Nov 17, 2024
# By: Brett W. Huffman
# Description: The dynamic item implementation of the sugar pop game
#############################################################

from Box2D.b2 import edgeShape
from settings import *

class dynamic_item:
    def __init__(self, world, color='red', friction=0.3, restitution=0.5):
        self.color = color
        self.world = world
        self.body = self.world.CreateStaticBody()
        self.friction = friction
        self.restitution = restitution
        self.vertices = []  # Store vertices as they are added

    def add_vertex(self, x, y):
        """
        Add a new vertex and create an EdgeFixture between the last vertex and the new one.
        """
        # Convert the y-coordinate to match Box2D's upward Y-axis
        adjusted_y = (HEIGHT - y) / SCALE
        adjusted_x = x / SCALE

        # Add the new vertex with adjusted coordinates
        new_vertex = (adjusted_x, adjusted_y)
        
        if self.vertices:
            # Create an edge fixture between the last vertex and the new vertex
            edge = edgeShape(vertices=[self.vertices[-1], new_vertex])
            self.body.CreateFixture(shape=edge, friction=self.friction, restitution=self.restitution)
        
        # Add the new vertex to the list
        self.vertices.append(new_vertex)

    def set_color(self, color='blue'):
        self.color = color
        
    def draw(self, screen):
        """
        Draw the chain shape (edges) on the Pygame screen.
        """
        for i in range(len(self.vertices) - 1):
            start = (self.vertices[i][0] * SCALE, HEIGHT - self.vertices[i][1] * SCALE)
            end = (self.vertices[i + 1][0] * SCALE, HEIGHT - self.vertices[i + 1][1] * SCALE)
            pg.draw.line(screen, pg.Color(self.color), start, end, 3)

    def delete(self):
        """
        Delete the dynamic item by destroying its Box2D body and clearing its vertices.
        """
        if self.body:
            self.world.DestroyBody(self.body)  # Destroy the Box2D body
            self.body = None  # Set the body to None to avoid reuse
        self.vertices = []  # Clear the vertices list