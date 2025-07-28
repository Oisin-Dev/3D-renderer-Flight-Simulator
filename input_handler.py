# input_handler.py
"""Handles keyboard (and later mouse) input."""
import pygame

def handle_input():
    keys = pygame.key.get_pressed()
    forward_amt = keys[pygame.K_w] - keys[pygame.K_s]
    right_amt = keys[pygame.K_a] - keys[pygame.K_d]  # Fixed: A=left, D=right
    up_amt = keys[pygame.K_LSHIFT] - keys[pygame.K_SPACE]
    yaw_amt = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]  # Fixed: LEFT=left, RIGHT=right
    pitch_amt = keys[pygame.K_DOWN] - keys[pygame.K_UP]
    should_reset_rot = keys[pygame.K_r]
    should_reset_pos = keys[pygame.K_t]
    should_quit = keys[pygame.K_ESCAPE]
    return (forward_amt, right_amt, up_amt, yaw_amt, pitch_amt, should_reset_rot, should_reset_pos, should_quit) 