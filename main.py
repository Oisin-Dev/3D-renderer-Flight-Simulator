import pygame
import numpy as np
from math import sin, cos

# Setup
WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Cube with Camera Controls")
clock = pygame.time.Clock()

# Cube verticies
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

faces = [
    (0, 1, 2, 3), #BK
    (4, 5, 6, 7), #F
    (0, 4, 5, 1), #BT
    (3, 7, 6, 2), #T
    (0, 3, 7, 4), #L
    (1, 5, 6, 2) #R
]

colours = [
  (255, 0, 0),
  (0, 255, 0),
  (0, 0, 255),
  (255, 255, 0),
  (255, 0, 255)]

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
    dt = clock.tick(30)
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
        camera_yaw += turn_speed
    if keys[pygame.K_RIGHT]:
        camera_yaw -= turn_speed
    if keys[pygame.K_UP]:
        camera_pitch -= turn_speed
    if keys[pygame.K_DOWN]:
        camera_pitch += turn_speed

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
    for face in faces:
      idx0, idx1, idx2, idx3 = face
      p0 = transformed[idx0]
      p1 = transformed[idx1]
      p2 = transformed[idx2]
      p3 = transformed[idx3]

      if None in (p0, p1, p2, p3):
        continue
        
      v0 = camera_matrix @ (points[idx0] - camera_pos)
      v1 = camera_matrix @ (points[idx1] - camera_pos)
      v2 = camera_matrix @ (points[idx2] - camera_pos)
        
      a = v1 - v0
      b = v2 - v0
      normal = np.cross(a,b)
        
      if normal[2] >= 0:
        continue
      
      projected = []
      for idx in [idx0, idx1, idx2, idx3]:
        cam_space = camera_matrix @ (points[idx] - camera_pos)
        if cam_space[2] <= 0:
          break
        f= 200/ cam_space[2]
        x = int(cam_space[0]*f+WIDTH /2)
        y = int(cam_space[1]*f+HEIGHT /2)
        projected.append((x,y))
      else:
        pygame.draw.polygon(screen, colours[idx], projected)

      pygame.display.update()

pygame.quit()
