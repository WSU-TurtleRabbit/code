# agent_behaviours.py

# These are a list of behaviours available to the agents.

import math
import numpy as np

def go_towards_target(target_position, agent_position, speed=0.2):

    delta_x = target_position[0] - agent_position[0]
    delta_y = target_position[1] - agent_position[1]
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

    if distance > 0:
        vx = (delta_x / distance) * speed
        vy = (delta_y / distance) * speed
    else:
        vx, vy = 0, 0  # Agent is at the target position

    return vx, vy

def go_towards_ball(ball_position, agent_position, speed=1):


    delta_x = ball_position[0] - agent_position[0]
    delta_y = ball_position[1] - agent_position[1]
    distance = math.sqrt(delta_x**2 + delta_y**2)

    if distance > 0:
        vx = (delta_x / distance) * speed
        vy = (delta_y / distance) * speed
    else:
        vx, vy = 0, 0
    return vx, vy




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





