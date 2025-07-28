# renderer.py
"""Handles all 3D rendering and projection logic."""
import pygame
import numpy as np
from config import FOV, WIDTH, HEIGHT, EDGE_CLIP, CUBE_COLOR, TEXT_COLOR, BG_COLOR, LINE_HEIGHT

def project(point):
    if point[2] <= 0:
        return None
    x = int(point[0] * (FOV / point[2]) + WIDTH / 2)
    y = int(point[1] * (FOV / point[2]) + HEIGHT / 2)
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