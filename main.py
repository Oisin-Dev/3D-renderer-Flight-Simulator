import pygame
import numpy as np
from math import sin, cos

# === CONFIGURATION CONSTANTS ===
WIDTH, HEIGHT = 1900, 1000
FOV = 200  # Focal length for projection
MOVE_SPEED = 0.1
TURN_SPEED = 0.02
LINE_HEIGHT = 20
FONT_NAME = 'Bahnschrift'
FONT_SIZE = 15
TEXT_COLOR = (255, 0, 0)
BG_COLOR = (230, 255, 230)
CUBE_COLOR = (0, 0, 0)
EDGE_CLIP = 5000  # Max projected coordinate before skipping line
CAMERA_START_POS = np.array([0.0, 0.0, -5.0])
CAMERA_START_YAW = 0.0
CAMERA_START_PITCH = 0.0
FPS_CAP = 60

# Setup
#WIDTH, HEIGHT = 1900, 1000  # moved to constants
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption("3D Cube with Camera Controls")
clock = pygame.time.Clock()
pygame.font.init()

texts = [
    "WASD to move",
    "LShift = Down",
    "Space = Up",
    "Use arrow keys to rotate",
    "R, T = Reset rot, pos"
]

x_pos = 0  # X position on the right-hand side
y_pos = 0   # Starting Y position for the first sentence
#line_height = 20  # moved to constants

font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

#text_color = (255, 0, 0)  # moved to constants

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
camera_pos = CAMERA_START_POS.copy()
camera_yaw = CAMERA_START_YAW
camera_pitch = CAMERA_START_PITCH

# Controls
#move_speed = 0.1  # moved to constants
#turn_speed = 0.02  # moved to constants

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

    #fov = 200  # focal length, moved to constants
    x = int(point[0] * (FOV / point[2]) + WIDTH / 2)
    y = int(point[1] * (FOV / point[2]) + HEIGHT / 2)
    return (x, y)

# Main loop
running = True
while running:
    dt = clock.tick(FPS_CAP)
    screen.fill(BG_COLOR)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Camera movement
#    forward = np.array([sin(camera_yaw), 0, cos(camera_yaw)])
#    right = np.array([cos(camera_yaw), 0, -sin(camera_yaw)])
    forward = np.array([sin(camera_yaw), 0, -cos(camera_yaw)])
    right = np.array([cos(camera_yaw), 0, sin(camera_yaw)])

    if keys[pygame.K_w]:
        camera_pos -= forward * MOVE_SPEED
    if keys[pygame.K_s]:
        camera_pos += forward * MOVE_SPEED
    if keys[pygame.K_a]:
        camera_pos -= right * MOVE_SPEED  
    if keys[pygame.K_d]:
        camera_pos += right * MOVE_SPEED
    if keys[pygame.K_LSHIFT]:
        camera_pos[1] += MOVE_SPEED
    if keys[pygame.K_SPACE]:
        camera_pos[1] -= MOVE_SPEED
    if keys[pygame.K_ESCAPE]:
        running = False

    # Camera rotation
    if keys[pygame.K_LEFT]:
        camera_yaw += TURN_SPEED
    if keys[pygame.K_RIGHT]:
        camera_yaw -= TURN_SPEED
    if keys[pygame.K_UP]:
        camera_pitch -= TURN_SPEED
    if keys[pygame.K_DOWN]:
        camera_pitch += TURN_SPEED
    if keys[pygame.K_r]:
        camera_pitch = CAMERA_START_PITCH
        camera_yaw = CAMERA_START_YAW
    if keys[pygame.K_t]:
        camera_pos = CAMERA_START_POS.copy()

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
        if (p1 is None) or (p2 is None):
            continue  # Skip this edge entirely

        if abs(p1[0]) > EDGE_CLIP or abs(p1[1]) > EDGE_CLIP or abs(p2[0]) > EDGE_CLIP or abs(p2[1]) > EDGE_CLIP:
            continue
        
        pygame.draw.line(screen, CUBE_COLOR, p1, p2, 2)

    framerate = int(clock.get_fps())
    pygame.display.set_caption(f"Running at {framerate} fps.")

    for i, text in enumerate(texts):
        text_surface = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surface, (x_pos, y_pos + i * LINE_HEIGHT))

#    instructions = pygame.font.SysFont('Bahnschrift', 30)
#    text_surface = instructions.render(f'WASD = FLBR \n LSHIFT = Down \n Space = Up', False, (255, 0, 0))
#    screen.blit(text_surface, (0,0))
    #pygame.draw.rect(screen, (56, 56, 56), (0,400,WIDTH,500), 0)
    pygame.display.update()

pygame.quit()

