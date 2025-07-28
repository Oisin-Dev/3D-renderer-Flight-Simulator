import pygame
import numpy as np
from camera import Camera
from config import *
from input_handler import handle_input
from renderer import render_scene
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

# Main loop
running = True
while running:
    dt = clock.tick(FPS_CAP) / 1000.0  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    (forward_amt, right_amt, up_amt, yaw_amt, pitch_amt, should_reset_rot, should_reset_pos, should_quit) = handle_input()
    camera.move(forward_amt, right_amt, up_amt, dt)
    camera.rotate(yaw_amt, pitch_amt, dt)
    if should_reset_rot:
        camera.reset_rotation()
    if should_reset_pos:
        camera.reset_position()
    if should_quit:
        running = False

    render_scene(screen, camera, points, edges, font, texts, x_pos, y_pos)

    framerate = int(clock.get_fps())
    pygame.display.set_caption(f"Running at {framerate} fps.")
    pygame.display.update()

pygame.quit()

