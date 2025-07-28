# renderer.py
"""Handles all 3D rendering and projection logic."""
import pygame
import numpy as np
import math
from config import WIDTH, HEIGHT, EDGE_CLIP, CUBE_COLOR, TEXT_COLOR, BG_COLOR, LINE_HEIGHT

# Perspective projection constants
NEAR_PLANE = 0.1
FAR_PLANE = 1000.0
FOV_ANGLE = 90  # degrees

def create_perspective_matrix():
    """Create a standard perspective projection matrix."""
    aspect_ratio = WIDTH / HEIGHT
    fov_rad = math.radians(FOV_ANGLE)
    f = 1.0 / math.tan(fov_rad / 2.0)
    
    return np.array([
        [f/aspect_ratio, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (FAR_PLANE + NEAR_PLANE)/(NEAR_PLANE - FAR_PLANE), (2 * FAR_PLANE * NEAR_PLANE)/(NEAR_PLANE - FAR_PLANE)],
        [0, 0, -1, 0]
    ])

def project(point):
    """Project a 3D point to 2D using homogeneous coordinates."""
    # Near plane clipping
    if point[2] <= NEAR_PLANE:
        return None
    
    # Convert to homogeneous coordinates
    point_homogeneous = np.array([point[0], point[1], point[2], 1.0])
    
    # Apply perspective projection
    perspective_matrix = create_perspective_matrix()
    projected = perspective_matrix @ point_homogeneous
    
    # Perspective divide
    if projected[3] == 0:
        return None
    
    x_ndc = projected[0] / projected[3]
    y_ndc = projected[1] / projected[3]
    
    # Convert from NDC to screen coordinates
    x = int((x_ndc + 1) * WIDTH / 2)
    y = int((1 - y_ndc) * HEIGHT / 2)
    
    return (x, y)

def render_scene(screen, camera, points, edges, font, texts, x_pos, y_pos):
    screen.fill(BG_COLOR)
    camera_matrix = camera.get_rotation_matrix()
    transformed = []
    for point in points:
        world_point = point
        relative = world_point - camera.position
        camera_space = camera_matrix @ relative
        proj = project(camera_space)
        transformed.append(proj)
    for edge in edges:
        p1 = transformed[edge[0]]
        p2 = transformed[edge[1]]
        if (p1 is None) or (p2 is None):
            continue
        if abs(p1[0]) > EDGE_CLIP or abs(p1[1]) > EDGE_CLIP or abs(p2[0]) > EDGE_CLIP or abs(p2[1]) > EDGE_CLIP:
            continue
        pygame.draw.line(screen, CUBE_COLOR, p1, p2, 2)
    for i, text in enumerate(texts):
        text_surface = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surface, (x_pos, y_pos + i * LINE_HEIGHT)) 