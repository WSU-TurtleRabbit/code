# agent_behaviours.py

# These are a list of behaviours available to the agents.

import math
import numpy as np

# def go_towards_target(target_position, agent_position, speed=1):

#     delta_x = target_position[0] - agent_position[0]
#     delta_y = target_position[1] - agent_position[1]
#     distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

#     if distance > 0:
#         vx = (delta_x / distance) * speed
#         vy = (delta_y / distance) * speed
#     else:
#         vx, vy = 0, 0  # Agent is at the target position

#     return vx, vy

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




def follow_agent(target_position, agent_position, speed=1.0):
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

FIELD_LENGTH = 4080 #mm
FIELD_WIDTH = 2600 #mm
SAFE_DISTANCE = 200 #mm

def enforce_field_boundaries(x, y, vx, vy):
    pass

# def enforce_field_boundaries(x, y, vx, vy):
#     """
#         Return vx and vy zero if it is at the field boundary
#     """
#     if x < -FIELD_LENGTH/2 + 2*SAFE_DISTANCE:
#         #keep going but slow down (speed = 0.3)
#         pass
#     if x < -FIELD_LENGTH/2 + SAFE_DISTANCE:
#         # go back to field
#         new_x = -FIELD_LENGTH/2 + 300
#         go_towards_target((new_x, y), (x, y), speed=1)
#     elif x > FIELD_LENGTH/2 - SAFE_DISTANCE:
#         new_x = FIELD_LENGTH/2 - 300
#         go_towards_target((new_x, y), (x, y), speed=1)
    
#     if y < -FIELD_WIDTH/2 + SAFE_DISTANCE:
#         new_y = -FIELD_WIDTH/2 + 300
#         go_towards_target((x, new_y), (x, y), speed=1)
#     elif y > FIELD_WIDTH/2 - SAFE_DISTANCE:
#         new_y = FIELD_WIDTH/2 - 300
#         go_towards_target((x, new_y), (x, y), speed=1)


def go_towards_target(target_position, agent_position, speed=1.3, slow_threshold=600, stop_threshold=80):
    """
    Calculate velocity components to move the agent towards a target position.

    input:
        target_position (tuple): Target position (x, y) in milimeters.
        agent_position (tuple): Current position of the agent (x, y) in milimeters.
        speed (float): Speed of the agent in m/s.
        slow_threshold (float): Distance threshold (in millimeters) for slowing down.
        stop_threshold (float): Distance threshold (in millimeters) for stopping completely.

    output:
        tuple: Velocity components (vx, vy) in m/s.
    """
    delta_x = target_position[0] - agent_position[0]
    delta_y = target_position[1] - agent_position[1]
    distance = math.hypot(delta_x, delta_y)

    if distance > stop_threshold:
        if distance > slow_threshold:
            vx = (delta_x / distance) * speed
            vy = (delta_y / distance) * speed
        else:
            vx = (delta_x / distance) * speed / 4
            vy = (delta_y / distance) * speed / 4
    else:
        vx, vy = 0, 0

    return vx, vy


# example usage:
# follow_agent
#go_to_target(target_position=agent_position, agent_position=active_agent_position, speed=10)
# go to ball
#go_to_target(target_position=ball_position, agent_position=active_agent_position)
# go to specified position
#go_to_target(target_position=target_position, agent_position=active_agent_position)


