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

# Cube face definitions (each face is defined by 4 vertices)
# Vertices are in clockwise order when viewed from outside the face
faces = [
    [0, 1, 2, 3],  # Front face (z = -1)
    [4, 5, 6, 7],  # Back face (z = 1)
    [0, 4, 7, 3],  # Left face (x = -1)
    [1, 5, 6, 2],  # Right face (x = 1)
    [3, 2, 6, 7],  # Top face (y = 1)
    [0, 1, 5, 4],  # Bottom face (y = -1)
]

# Face normals (pointing outward from each face)
face_normals = [
    np.array([0, 0, 1]),   # Front face normal
    np.array([0, 0, -1]),  # Back face normal
    np.array([1, 0, 0]),   # Left face normal
    np.array([-1, 0, 0]),  # Right face normal
    np.array([0, -1, 0]),  # Top face normal
    np.array([0, 1, 0]),   # Bottom face normal
]

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

def is_face_visible(face_normal, camera_direction):
    """Check if a face is visible to the camera."""
    # If dot product is positive, face is facing toward camera
    return np.dot(face_normal, camera_direction) > 0.175

def calculate_face_depth(face_vertices, transformed_points):
    """Calculate the average depth of a face for sorting."""
    depths = []
    for vertex_index in face_vertices:
        if transformed_points[vertex_index] is not None:
            # Use the original 3D point's Z coordinate for depth
            depths.append(transformed_points[vertex_index][2])
    return np.mean(depths) if depths else float('inf')

def render_scene(screen, camera, points, edges, font, texts, x_pos, y_pos):
    screen.fill(BG_COLOR)
    camera_matrix = camera.get_rotation_matrix()
    
    # Calculate camera direction as vector from camera to object center
    object_center = np.array([0.0, 0.0, 0.0])
    camera_direction = object_center - camera.position
    camera_direction = camera_direction / np.linalg.norm(camera_direction)
    
    # Transform all points
    transformed = []
    original_points_3d = []  # Keep original 3D points for depth calculation
    for point in points:
        world_point = point
        relative = world_point - camera.position
        camera_space = camera_matrix @ relative
        original_points_3d.append(camera_space)  # Store for depth calculation
        proj = project(camera_space)
        transformed.append(proj)
    
    # Prepare faces for rendering with depth sorting
    visible_faces = []
    for face_index, face_vertices in enumerate(faces):
        if is_face_visible(face_normals[face_index], camera_direction):
            # Check if all vertices are valid
            face_2d = []
            valid_face = True
            for vertex_index in face_vertices:
                if transformed[vertex_index] is None:
                    valid_face = False
                    break
                face_2d.append(transformed[vertex_index])
            
            if valid_face:
                # Calculate depth for sorting
                depth = calculate_face_depth(face_vertices, original_points_3d)
                visible_faces.append((face_2d, depth, face_index))
    
    # Sort faces by depth (back to front for proper rendering)
    visible_faces.sort(key=lambda x: x[1], reverse=True)
    
    # Render faces
    for face_2d, depth, face_index in visible_faces:
        # For now, use wireframe rendering of faces
        # Later this can be easily changed to filled polygons
        pygame.draw.polygon(screen, CUBE_COLOR, face_2d, 2)
    
    # Render UI text
    for i, text in enumerate(texts):
        text_surface = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surface, (x_pos, y_pos + i * LINE_HEIGHT))