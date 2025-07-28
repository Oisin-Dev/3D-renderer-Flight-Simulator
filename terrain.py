# terrain.py
"""Handles terrain generation and collision detection."""
import numpy as np

class Terrain:
    def __init__(self, size=100, height=10):
        """
        Initialize a simple flat terrain.
        
        Args:
            size: Size of the terrain plane (width and length)
            height: Y-coordinate of the terrain surface
        """
        self.size = size
        self.height = height
        self.vertices = []
        self.faces = []
        self.generate_flat_terrain()
    
    def generate_flat_terrain(self):
        """Generate a simple flat terrain plane."""
        # Create a grid of vertices
        half_size = self.size / 2
        grid_size = 10  # Reduced from 20 to 10 for better performance
        cell_size = self.size / grid_size
        
        # Generate vertices
        for z in range(grid_size + 1):
            for x in range(grid_size + 1):
                # Calculate world coordinates
                world_x = (x * cell_size) - half_size
                world_z = (z * cell_size) - half_size
                world_y = self.height
                
                self.vertices.append(np.array([world_x, world_y, world_z]))
        
        # Generate faces (quads)
        for z in range(grid_size):
            for x in range(grid_size):
                # Calculate vertex indices for this quad
                v0 = z * (grid_size + 1) + x
                v1 = z * (grid_size + 1) + x + 1
                v2 = (z + 1) * (grid_size + 1) + x + 1
                v3 = (z + 1) * (grid_size + 1) + x
                
                # Add the quad as two triangles
                self.faces.append([v0, v1, v2])  # First triangle
                self.faces.append([v0, v2, v3])  # Second triangle
    
    def get_vertices(self):
        """Get terrain vertices."""
        return self.vertices
    
    def get_faces(self):
        """Get terrain faces."""
        return self.faces
    
    def check_collision(self, position):
        """
        Check if a position collides with the terrain.
        
        Args:
            position: 3D position to check (numpy array)
        
        Returns:
            bool: True if collision detected
        """
        # Simple collision: check if below terrain height
        return position[1] <= self.height
    
    def get_terrain_height_at(self, x, z):
        """
        Get the terrain height at a given X,Z position.
        
        Args:
            x, z: X and Z coordinates
        
        Returns:
            float: Terrain height at that position
        """
        # For flat terrain, always return the same height
        return self.height