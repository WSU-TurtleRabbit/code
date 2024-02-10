from WSUSSL.TeamControl.Skills.baseskill import BaseSkill
from WSUSSL.Shared.action import Action
from WSUSSL.World.model import Model as wm
import math
import numpy as np


class GoTowards(BaseSkill):
    def __init__(self, world_model:wm,robot_id):
        """_summary_
            This function will compile rotate and go to point function
            and send it to the robot.
        Args:
            world_model (wm): world model that is created and constantly updated
            robot_id (int): the robot that you want to move
        Params: 
            state : start, run, finish
        """
        super().__init__(world_model)
        self.add_state('start', self.start_action)
        self.add_state('run', self.run_action)
        self.add_state('finish', self.finish_action)
        self.start_state = 'start'
        self.final_state = 'finish'
        self.robot_id=robot_id
        self.counter = 0

    def start_action(self):
        """_summary_
            1st we need ball position and robot position that we want. 
            We can get them from the world model
        Returns:
            _type_: _description_
        """
        print("Start action")
        #self.counter = 0
        print("getting data")
        # getting robot data 
        #robot_id = int(input("Enter a robot that you want to move"))
        robot_position = self.world_model.get_robot_position(self.robot_id, True)
        #if we want to go towards ball
        ball_position = self.world_model.get_ball_position()
        # now we have the data, we can now run the commands
        self.transition_to('run')
        return ball_position, robot_position


    def run_action(self,ball_position,robot_position):
        print("Go Towards the target position: Run action")
        w = turn_to_ball(ball_position)
        vx,vy = go_towards(ball_position, robot_position)
        new_action = Action(self.robot_id,vx,vy,w,0,0,0)
        self.transition_to('finish')
        return new_action
        
        
    def finish_action(self):
        print("Go Towards: Finish action")
        return Action(self.robot_id,0,0,0,0,0)        


def turn_to_ball(ball_position, epsilon = 0.15):
    """_summary_
        This function returns an agular velocity. The goal is to turn the robot
        in such a way that it is facing the ball with its kicker side.
        -Lisa
    Args:
        ball_position (tuple): ball x and y coordinates from world module
        epsilon (float, optional): Threshold for orientation. Defaults to 0.15.
        (Orientation does not have to be zero.)

    Returns:
        w(omega)(float): the angular velocity of the robot 
    """
    orientation_to_ball = np.arctan2(ball_position[0], ball_position[1])

    if abs(orientation_to_ball) < epsilon:
        # to avoid jitter
        w = 0
        print("Robot already has correct orientation", w, orientation_to_ball)
    elif abs(orientation_to_ball) > epsilon and abs(orientation_to_ball) < 4*epsilon:
        w = -1*np.sign(orientation_to_ball) * 0.5
        print("Robot almost has correct orientation", w, orientation_to_ball)
    else:
        w = -1*np.sign(orientation_to_ball)
        print("Robot not in correct orientation", w, orientation_to_ball)

    return w

def go_towards(target_position:tuple, robot_position):
    speed = 5

    delta_x = target_position[0] - robot_position[0]
    delta_y = target_position[1] - robot_position[1]
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)  #Pythag

    if distance > 800:
        vx = (delta_x / distance) * speed
        vy = (delta_y / distance) * speed
    else:
        vx, vy = 0, 0  # robot is at the target position

    return vx, vy #returns for action
