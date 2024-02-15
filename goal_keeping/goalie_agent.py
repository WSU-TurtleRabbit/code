# general_agent.py
from agent_behaviours import go_towards_target
from agent import agent
import numpy as np
from numpy import pi
from ball_trajectory import predict_trajectory, goal_intersection

'''
    The goalie will stay in the center of the goal unless a ball is 
    estimated to go into the goal. If the goal is estimated to go into 
    the goal the goalie will go to that position to block it. 
'''

class GoalieAgent(agent):
    def __init__(self, id, world2robot_fn=None):
        super().__init__(id)
        self.world2robot_fn = world2robot_fn
        self.default_position = np.array([-1200, 0]) # center of the goal
        self.target_position = self.default_position

    def set_target(self, target_position):
        #target_position = super().check_boundary(self, target_position)
        # does not set ball position as target
        pass

    def act(self, frame):
        if self.target_position is not None:
            robot_data = frame["detection"]["robots_blue"][self.id]
            history = frame["history"] # history of ball positions

            trajectory, direction_info, trajectory_y_at_goal_line, velocity = predict_trajectory(history, 5)
            # check whether the estimated ball trajectory intersects with the goal line
            #if trajectory_y_at_goal_line and direction_info == "Moving towards the goal":
            if trajectory_y_at_goal_line:
                intersects_line, intersection_point = goal_intersection(trajectory_y_at_goal_line)
                if intersects_line:
                    # goalie moves to the estimated ball position at the goalie line
                    print(f"Ball goes into goal at position {intersection_point}")
                    self.target_position = np.array(intersection_point)
                else:
                    # goalie moves to the center of the goal
                    self.target_position = self.default_position
                    print("Ball does not go into goal")
            else:
                # goalie moves to the center of the goal
                self.target_position = self.default_position
                print("Ball does not go into goal")

            if robot_data and self.world2robot_fn:
                robot_pose = np.array([robot_data['x'], robot_data['y'], robot_data['orientation'] - pi/2])
                # Convert target position to robot's coordinate system
                target_robot = self.world2robot_fn(self.target_position, robot_pose)

                # Use a behavior function to calculate velocities towards the target
                agent_position = np.array([0, 0]) # agent position in local robot coord. system
                self.vx, self.vy = go_towards_target(target_robot, agent_position, speed=1.3, slow_threshold=100)

                self.vw = 0  # Assuming no rotation for simplicity
                return self.id, self.vx, self.vy, self.vw
            else:
                return self.id, 0, 0, 0  # No robot data or transformation function available
        else:
            return self.id, 0, 0, 0  # No target set
