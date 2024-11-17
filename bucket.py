import pygame as pg
from Box2D.b2 import staticBody, polygonShape
from settings import SCALE, HEIGHT, WIDTH

class Bucket:
    def __init__(self, world, x, y, width, height):
        """
        Initialize the bucket with an open top by creating three separate static bodies 
        for each wall (left, right, bottom).
        
        :param world: The Box2D world.
        :param x: X position of the bucket's center in Pygame coordinates.
        :param y: Y position of the bucket's top in Pygame coordinates.
        :param width: Width of the bucket in pixels.
        :param height: Height of the bucket in pixels.
        """
        self.world = world
        self.width = width / SCALE
        self.height = height / SCALE
        self.count = 0  # Counter for collected sugar grains

        wall_thickness = 0.1  # Thickness of the walls in Box2D units

        # Left wall
        left_wall_position = (x / SCALE - self.width / 2, y / SCALE - self.height / 2)
        self.left_wall = self.world.CreateStaticBody(position=left_wall_position)
        left_wall_shape = polygonShape()
        left_wall_shape.SetAsBox(wall_thickness, self.height / 2)
        self.left_wall.CreateFixture(shape=left_wall_shape, friction=0.5, density=0)

        # Right wall
        right_wall_position = (x / SCALE + self.width / 2, y / SCALE - self.height / 2)
        self.right_wall = self.world.CreateStaticBody(position=right_wall_position)
        right_wall_shape = polygonShape()
        right_wall_shape.SetAsBox(wall_thickness, self.height / 2)
        self.right_wall.CreateFixture(shape=right_wall_shape, friction=0.5, density=0)

        # Bottom wall
        bottom_wall_position = (x / SCALE, y / SCALE - self.height)
        self.bottom_wall = self.world.CreateStaticBody(position=bottom_wall_position)
        bottom_wall_shape = polygonShape()
        bottom_wall_shape.SetAsBox(self.width / 2, wall_thickness)
        self.bottom_wall.CreateFixture(shape=bottom_wall_shape, friction=0.5, density=0)

    def draw(self, screen):
        """
        Draw the bucket with an open top on the Pygame screen.
        """
        # Convert Box2D coordinates to Pygame screen coordinates
        left_x = self.left_wall.position.x * SCALE
        left_y = HEIGHT - self.left_wall.position.y * SCALE
        right_x = self.right_wall.position.x * SCALE
        right_y = HEIGHT - self.right_wall.position.y * SCALE
        bottom_x = self.bottom_wall.position.x * SCALE
        bottom_y = HEIGHT - self.bottom_wall.position.y * SCALE

        half_width = self.width * SCALE / 2
        half_height = self.height * SCALE / 2

        # Define points for the left, right, and bottom edges of the bucket
        left_edge_start = (left_x, left_y - half_height)
        left_edge_end = (left_x, left_y + half_height)
        right_edge_start = (right_x, right_y - half_height)
        right_edge_end = (right_x, right_y + half_height)
        bottom_edge_start = (bottom_x - half_width+1, bottom_y)
        bottom_edge_end = (bottom_x + half_width+1, bottom_y)

        # Draw the bucket edges
        pg.draw.line(screen, (144, 238, 144), left_edge_start, left_edge_end, 2)
        pg.draw.line(screen, (144, 238, 144), right_edge_start, right_edge_end, 2)
        pg.draw.line(screen, (144, 238, 144), bottom_edge_start, bottom_edge_end, 2)

    def count_reset(self):
        self.count = 0
        
    def collect(self, sugar_grain):
        """
        Check if a sugar grain is within the bucket bounds and, if so, increase the bucket's count.
        
        :param sugar_grain: The sugar grain to check.
        """
        grain_pos = sugar_grain.body.position
        bucket_pos = self.left_wall.position  # Use left wall position for bucket reference

        # Check if the grain's position is within the bucket's bounding box
        if (bucket_pos.x <= grain_pos.x <= bucket_pos.x + self.width and
                bucket_pos.y - self.height - 10 <= grain_pos.y <= bucket_pos.y):
            self.count += 1
            return True  # Indicate that the grain was collected

        return False  # Grain not collected

