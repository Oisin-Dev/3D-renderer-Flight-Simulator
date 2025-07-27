# camera.py
"""Handles camera and player movement logic."""
import numpy as np
from config import MOVE_SPEED, TURN_SPEED, CAMERA_START_POS, CAMERA_START_YAW, CAMERA_START_PITCH
from math import sin, cos

class Camera:
    def __init__(self, position=None, yaw=None, pitch=None):
        self.position = np.array(position if position is not None else CAMERA_START_POS, dtype=float)
        self.yaw = yaw if yaw is not None else CAMERA_START_YAW
        self.pitch = pitch if pitch is not None else CAMERA_START_PITCH

    def get_rotation_matrix(self):
        cy, sy = cos(self.yaw), sin(self.yaw)
        cp, sp = cos(self.pitch), sin(self.pitch)

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

    def move(self, forward_amt, right_amt, up_amt, dt):
        # Calculate forward and right vectors based on current yaw
        forward = np.array([sin(self.yaw), 0, -cos(self.yaw)])
        right = np.array([cos(self.yaw), 0, sin(self.yaw)])
        self.position += (-forward * forward_amt + right * right_amt) * MOVE_SPEED * dt
        self.position[1] += up_amt * MOVE_SPEED * dt

    def rotate(self, yaw_amt, pitch_amt, dt):
        self.yaw += yaw_amt * TURN_SPEED * dt
        self.pitch += pitch_amt * TURN_SPEED * dt
        # Clamp pitch
        self.pitch = np.clip(self.pitch, -np.pi / 2 + 0.01, np.pi / 2 - 0.01)

    def reset_rotation(self):
        self.yaw = CAMERA_START_YAW
        self.pitch = CAMERA_START_PITCH

    def reset_position(self):
        self.position = np.array(CAMERA_START_POS, dtype=float) 