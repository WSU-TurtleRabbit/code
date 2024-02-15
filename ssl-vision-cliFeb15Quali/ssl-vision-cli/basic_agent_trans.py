# basic_agent.py
from agent_behaviours import go_towards_ball
from agent_behaviours import follow_agent
from agent import agent
import math
import numpy as np
from numpy import pi

class BasicAgentTrans(agent):
    def __init__(self, id, world2robot_fn=None):
        super().__init__(id)
        # Store the transformation function
        self.world2robot_fn = world2robot_fn

    def act(self, frame):
        if "ball" in frame["detection"]:
            ball_position = np.array([frame['detection']['ball']['x'], frame['detection']['ball']['y']])
            robot_data = frame["detection"]["robots_blue"][self.id]
            
            if robot_data and self.world2robot_fn:
                orientation = robot_data['orientation']
                orientation -= pi/2
                robot_pose = np.array([robot_data['x'], robot_data['y'], orientation])
                # Use the transformation function to get the ball's position in robot's coordinate system
                target_robot = self.world2robot_fn(ball_position, robot_pose)
                print()
                print("Target robot: ")
                print(target_robot)
                print()
                
                # Calculate the direction vector and normalize it
                magnitude = math.sqrt(target_robot[0]**2 + target_robot[1]**2)
                if magnitude > 0:
                    self.vx = target_robot[0]/magnitude
                    self.vy = target_robot[1]/magnitude
                else:
                    self.vx, self.vy = 0, 0  # Ball is at the robot's position
                
                self.vz = 0  # Assuming no rotation for simplicity
                
                return self.id, self.vx, self.vy, self.vz
            else:
                return self.id, 0, 0, 0  # No ball data or transformation function available
        else:
            return self.id, 0, 0, 0  # No ball 