#Wireframe rendered cube with camera controls


import pygame
import numpy as np
from math import sin, cos

# Setup
WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Cube with Camera Controls")
clock = pygame.time.Clock()

# Cube vertices
points = [
    np.array([-1, -1, -1]),
    np.array([1, -1, -1]),
    np.array([1, 1, -1]),
    np.array([-1, 1, -1]),
    np.array([-1, -1, 1]),
    np.array([1, -1, 1]),
    np.array([1, 1, 1]),
    np.array([-1, 1, 1])
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Camera setup
camera_pos = np.array([0.0, 0.0, -5.0])
camera_yaw = 0.0
camera_pitch = 0.0

# Controls
move_speed = 0.1
turn_speed = 0.02

def get_camera_rotation_matrix(yaw, pitch):
    cy, sy = cos(yaw), sin(yaw)
    cp, sp = cos(pitch), sin(pitch)

    rot_yaw = np.array([
        [cy, 0, sy],
        [0, 1, 0],
        [-sy, 0, cy]
    ])

    rot_pitch = np.array([
        [1, 0, 0],
        [0, cp, -sp],
        [0, sp, cp]
    ])

    return rot_pitch @ rot_yaw

def project(point):
    if point[2] <= 0:
        return None  # Don't project points behind the camera

    fov = 200  # focal length
    x = int(point[0] * (fov / point[2]) + WIDTH / 2)
    y = int(point[1] * (fov / point[2]) + HEIGHT / 2)
    return (x, y)

# Main loop
running = True
while running:
    dt = clock.tick(60)
    screen.fill((255, 255, 255))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Camera movement
    forward = np.array([sin(camera_yaw), 0, cos(camera_yaw)])
    right = np.array([cos(camera_yaw), 0, -sin(camera_yaw)])

    if keys[pygame.K_w]:
        camera_pos += forward * move_speed
    if keys[pygame.K_s]:
        camera_pos -= forward * move_speed
    if keys[pygame.K_a]:
        camera_pos -= right * move_speed
    if keys[pygame.K_d]:
        camera_pos += right * move_speed
    if keys[pygame.K_q]:
        camera_pos[1] += move_speed
    if keys[pygame.K_e]:
        camera_pos[1] -= move_speed

    # Camera rotation
    if keys[pygame.K_LEFT]:
        camera_yaw -= turn_speed
    if keys[pygame.K_RIGHT]:
        camera_yaw += turn_speed
    if keys[pygame.K_UP]:
        camera_pitch += turn_speed
    if keys[pygame.K_DOWN]:
        camera_pitch -= turn_speed

    # Clamp pitch
    camera_pitch = np.clip(camera_pitch, -np.pi / 2 + 0.01, np.pi / 2 - 0.01)

    # Create camera matrix
    camera_matrix = get_camera_rotation_matrix(camera_yaw, camera_pitch)

    # Transform and project all points
    transformed = []
    for point in points:
        world_point = point
        relative = world_point - camera_pos
        camera_space = camera_matrix @ relative

        proj = project(camera_space)
        transformed.append(proj)

    # Draw cube
    for edge in edges:
        p1 = transformed[edge[0]]
        p2 = transformed[edge[1]]
        if p1 is not None and p2 is not None:
            pygame.draw.line(screen, (0, 0, 0), p1, p2, 2)

    pygame.display.update()

pygame.quit()


