# from robot_behaviours.py -Eren

# These are a list of behaviours available to the robots.

import math
import numpy as np
from WSUSSL.World.model import Model as wm
from WSUSSL.Shared.action import Action

speed=2

def go_towards_target(world_model:wm, target_position:tuple, robot_position):

    robot_position = world_model.get_robot_position()

    delta_x = target_position[0] - robot_position[0]
    delta_y = target_position[1] - robot_position[1]
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)  #Pythag

    if distance > 800:
        vx = (delta_x / distance) * speed
        vy = (delta_y / distance) * speed
    else:
        vx, vy = 0, 0  # robot is at the target position

    return vx, vy #returns for action

def go_towards_ball(ball_position, robot_position):


    delta_x = ball_position[0] - robot_position[0]
    delta_y = ball_position[1] - robot_position[1]
    distance = math.sqrt(delta_x**2 + delta_y**2)  #Pythag

    if distance > 0:
        vx = (delta_x / distance) * speed
        vy = (delta_y / distance) * speed
    else:
        vx, vy = 0, 0
    return vx, vy




def follow_robot(target_position, robot_position):
    if target_position:
        delta_x = target_position[0] - robot_position[0]
        delta_y = target_position[1] - robot_position[1]
        distance = math.sqrt(delta_x**2 + delta_y**2) #Pythag

        if distance > 0:
            vx = (delta_x / distance) * speed
            vy = (delta_y / distance) * speed
        else:
            vx, vy = 0, 0
    else:
        vx, vy = 0, 0
    return vx, vy




