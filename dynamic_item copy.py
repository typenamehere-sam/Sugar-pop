from Box2D.b2 import chainShape
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
        Add a new vertex and recreate the ChainShape with updated vertices.
        """
        # Convert the y-coordinate to match Box2D's upward Y-axis
        adjusted_y = (HEIGHT - y) / SCALE
        adjusted_x = x / SCALE

        # Add the new vertex with adjusted coordinates
        self.vertices.append((adjusted_x, adjusted_y))

        if len(self.vertices) > 2:
            # Destroy the old fixture
            self.body.DestroyFixture(self.body.fixtures[0]) if self.body.fixtures else None

            # Create a new ChainShape with the updated vertices
            chain = chainShape(vertices=self.vertices)
        
            self.body.CreateFixture(shape=chain, friction=self.friction, restitution=self.restitution)

    def set_color(self, color='blue'):
        self.color = color
        
    def draw(self, screen):
        """
        Draw the ChainShape on the Pygame screen.
        """
        for i in range(len(self.vertices) - 1):
            start = (self.vertices[i][0] * SCALE, HEIGHT - self.vertices[i][1] * SCALE)
            end = (self.vertices[i + 1][0] * SCALE, HEIGHT - self.vertices[i + 1][1] * SCALE)
            pg.draw.line(screen, pg.Color(self.color), start, end, 3)
