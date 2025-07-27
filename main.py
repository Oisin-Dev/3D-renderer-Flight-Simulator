import pygame
import numpy as np
from camera import Camera
from config import *
from input_handler import handle_input
from math import sin, cos

# === CONFIGURATION CONSTANTS ===
# (moved to config.py)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.font.init()

texts = [
    "WASD to move",
    "LShift = Down",
    "Space = Up",
    "Use arrow keys to rotate",
    "R, T = Reset rot, pos"
]

x_pos = 0
y_pos = 0
font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

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
camera = Camera()

def project(point):
    if point[2] <= 0:
        return None
    x = int(point[0] * (FOV / point[2]) + WIDTH / 2)
    y = int(point[1] * (FOV / point[2]) + HEIGHT / 2)
    return (x, y)

# Main loop
running = True
while running:
    dt = clock.tick(FPS_CAP) / 1000.0  # Delta time in seconds
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Use input handler
    (forward_amt, right_amt, up_amt, yaw_amt, pitch_amt, should_reset_rot, should_reset_pos, should_quit) = handle_input()
    camera.move(forward_amt, right_amt, up_amt, dt)
    camera.rotate(yaw_amt, pitch_amt, dt)
    if should_reset_rot:
        camera.reset_rotation()
    if should_reset_pos:
        camera.reset_position()
    if should_quit:
        running = False

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

    framerate = int(clock.get_fps())
    pygame.display.set_caption(f"Running at {framerate} fps.")

    for i, text in enumerate(texts):
        text_surface = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surface, (x_pos, y_pos + i * LINE_HEIGHT))

    pygame.display.update()

pygame.quit()

