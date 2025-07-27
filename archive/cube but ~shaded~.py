import pygame
import numpy as np
from math import sin, cos

WHITE = (255, 255, 255)
WIDTH, HEIGHT = 800, 600

pygame.display.set_caption("3D Cube with Flat Shading")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

scale = 100
circle_pos = [WIDTH / 2, HEIGHT / 2]
angle = 0
rotation_speed = 0.01

# Cube vertices
points = [
    np.array([-1, -1, 1]),
    np.array([1, -1, 1]),
    np.array([1, 1, 1]),
    np.array([-1, 1, 1]),
    np.array([-1, -1, -1]),
    np.array([1, -1, -1]),
    np.array([1, 1, -1]),
    np.array([-1, 1, -1])
]

# Each face is defined by 4 vertex indices
faces = [
    [0, 1, 2, 3],  # Front
    [4, 5, 6, 7],  # Back
    [0, 1, 5, 4],  # Bottom
    [2, 3, 7, 6],  # Top
    [0, 3, 7, 4],  # Left
    [1, 2, 6, 5],  # Right
]

# Projection matrix (just drops z for simple orthographic projection)
projection_matrix = np.array([
    [1, 0, 0],
    [0, 1, 0]
])

# Simple light direction (toward the viewer)
light_dir = np.array([0, 0, -1])
light_dir = light_dir / np.linalg.norm(light_dir)

def project(point):
    projected = projection_matrix @ point
    x = int(projected[0] * scale + circle_pos[0])
    y = int(projected[1] * scale + circle_pos[1])
    return (x, y)

while True:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

    # Define rotation matrices
    rot_z = np.array([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1]
    ])

    rot_y = np.array([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)]
    ])

    rot_x = np.array([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)]
    ])

    # Update angle
    angle += rotation_speed

    # Rotate all points
    transformed_points = []
    for point in points:
        rotated = rot_z @ point
        rotated = rot_y @ rotated
        rotated = rot_x @ rotated
        transformed_points.append(rotated)

    # Draw each face with shading
    for face in faces:
        p0 = transformed_points[face[0]]
        p1 = transformed_points[face[1]]
        p2 = transformed_points[face[2]]

        # Compute normal using cross product
        v1 = p1 - p0
        v2 = p2 - p0
        normal = np.cross(v1, v2)
        norm_length = np.linalg.norm(normal)
        if norm_length == 0:
            continue
        normal = normal / norm_length

        # Backface culling: skip faces facing away
       # if np.dot(normal, np.array([0, 0, -1])) <= 0:
       #     continue

        # Compute brightness from light
        brightness = np.dot(normal, light_dir)
        brightness = max(0, min(1, brightness))  # Clamp
        shade = int(brightness * 255)
        color = (shade, shade, shade)

        # Project face vertices
        face_2d = [project(transformed_points[i]) for i in face]

        pygame.draw.polygon(screen, color, face_2d)

    pygame.display.update()