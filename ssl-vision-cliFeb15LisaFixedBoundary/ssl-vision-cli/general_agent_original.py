# general_agent_original.py
from agent_behaviours import go_towards_target
from agent import agent
import numpy as np
from numpy import pi

class GeneralAgent(agent):
    def __init__(self, id, world2robot_fn=None):
        super().__init__(id)
        self.world2robot_fn = world2robot_fn
        self.target_position = None  # Initialize with no target

    def set_target(self, target_position):
        self.target_position = np.array(target_position)

    def act(self, frame):
        if self.target_position is not None:
            robot_data = frame["detection"]["robots_blue"][self.id]
            print("Target position: ", self.target_position)

            if robot_data and self.world2robot_fn:
                orientation = robot_data['orientation'] - pi/2
                robot_pose = np.array([robot_data['x'], robot_data['y'], orientation])
                # Convert target position to robot's coordinate system
                target_robot = self.world2robot_fn(self.target_position, robot_pose)

                # Use a behavior function to calculate velocities towards the target
                agent_position = np.array([0, 0])
                self.vx, self.vy = go_towards_target(target_robot, agent_position)

                self.vz = 0  # Assuming no rotation for simplicity
                return self.id, self.vx, self.vy, self.vz
            else:
                return self.id, 0, 0, 0  # No robot data or transformation function available
        else:
            return self.id, 0, 0, 0  # No target set
