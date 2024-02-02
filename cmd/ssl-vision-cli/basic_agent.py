# basic_agent.py
from agent_behaviours import go_towards_ball
from agent_behaviours import darpan_go_to_ball
from agent_behaviours import follow_robot
from agent import agent
import math


class BasicAgent(agent):
    def __init__(self, id):
        super().__init__(id)
        # Desired orientation angle in radians 
        self.desired_orientation = math.pi / 2
        self.constant_angular_velocity = 1


    def act(self, frame):
        print()
        print("agentframe")
        print(f"self.detection is: {frame}")
        print("agentframe")

        # Get the current orientation of the robot
        current_orientation = frame['detection']['robots_blue'][self.id]['orientation']
        
        # Calculate the difference in orientation
        orientation_difference = self.desired_orientation - current_orientation
        
        # Adjust the orientation difference if it's beyond the -pi to pi range
        if orientation_difference > math.pi:
            orientation_difference -= 2 * math.pi
        elif orientation_difference < -math.pi:
            orientation_difference += 2 * math.pi

        # Apply the constant angular velocity based on the sign of the difference
        if abs(orientation_difference) > 0.1:  # Add some threshold to prevent oscillation
            self.vz = self.constant_angular_velocity * (-1 if orientation_difference < 0 else 1)
        else:
            self.vz = 0 





        if "ball" in frame["detection"]:
            ball_x = frame['detection']['ball']['x']
            ball_y = frame['detection']['ball']['y']
            ball_position = (ball_x, ball_y)
        else:
            ball_position = None
        

        target = 3
        if frame['detection']['robots_yellow'][target]['x']:
            target_x = frame['detection']['robots_yellow'][target]['x']
            target_y = frame['detection']['robots_yellow'][target]['y']
            target_position = (target_x, target_y)
        else:
            target_position = None

        my_x = frame['detection']['robots_blue'][self.id]['x']
        my_y = frame['detection']['robots_blue'][self.id]['y']
        my_position = (my_x, my_y)


        self.vx, self.vy = follow_robot(target_position, my_position)


        return self.id, self.vx, self.vy, self.vz
