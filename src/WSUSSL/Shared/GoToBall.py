# Function created by Darpan
from WSUSSL.World.model import Model as wm
from WSUSSL.Shared.action import Action

def go_to_ball(world_model: wm, robot_id):
    ball_x, ball_y = world_model.get_ball_position()
    robot_coordinates = world_model.get_robot_position(robot_id,True)
    print(robot_coordinates)
    rx = robot_coordinates["x"]
    ry = robot_coordinates["y"]
    ro = robot_coordinates["o"]

    if (ball_x > rx) : 
        # go +
        print("move right")
        vx = 10
        if(ball_y> ry):
            vy = 10
        elif(ball_y < ry):
            vy = -10
        else:
            vy = 0

    elif (ball_x < rx):
        vx = -10
        if(ball_y > ry):
            vy = 10
        elif(ball_y < ry):
            vy = -10
        else:
            vy = 0


    new_action = Action(robot_id,vx,vy,0,0,0)
    print(new_action)
    return new_action

    