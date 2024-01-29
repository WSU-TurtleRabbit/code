# agent_behaviours.py

import math
import numpy as np

def go_towards_ball(ball_position, agent_position, speed=10.0):
    if ball_position:

        delta_x = ball_position[0] - agent_position[0]
        delta_y = ball_position[1] - agent_position[1]
        distance = math.sqrt(delta_x**2 + delta_y**2)

        if distance > 0:
            vx = (delta_x / distance) * speed
            vy = (delta_y / distance) * speed
        else:
            vx, vy = 0, 0
    else:
        vx, vy = 0, 0
    return vx, vy

def darpan_go_to_ball(ball_position, agent_position, time_to_ball=5):
    if ball_position:
        delta_x = ball_position[0] - agent_position[0] # In Darpan's formula, this is (Xb-Xr)
        delta_y = ball_position[1] - agent_position[1] # Yb-Yr
        length = math.sqrt(delta_x**2 + delta_y**2)

        theta = np.arctan(delta_y/delta_x)

        vx = (length*np.cos(theta)) / time_to_ball
        vy = (length*np.sin(theta)) / time_to_ball
        vz = 0

        return vx, vy, vz




def follow_agent(target_position, agent_position, speed=10.0):
    if target_position:
        delta_x = target_position[0] - agent_position[0]
        delta_y = target_position[1] - agent_position[1]
        distance = math.sqrt(delta_x**2 + delta_y**2)

        if distance > 0:
            vx = (delta_x / distance) * speed
            vy = (delta_y / distance) * speed
        else:
            vx, vy = 0, 0
    else:
        vx, vy = 0, 0
    return vx, vy





