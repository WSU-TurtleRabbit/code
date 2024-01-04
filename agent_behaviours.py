# agent_behaviours.py

import math

def go_towards_ball(ball_position, agent_position, speed=1.0):
    delta_x = ball_position[0] - agent_position[0]
    delta_y = ball_position[1] - agent_position[1]
    distance = math.sqrt(dx**2 + dy**2)

    if distance > 0:
        vx = (delta_x / distance) * speed
        vy = (delta_y / distance) * speed
    else:
        vx, vy = 0, 0

    return vx, vy
