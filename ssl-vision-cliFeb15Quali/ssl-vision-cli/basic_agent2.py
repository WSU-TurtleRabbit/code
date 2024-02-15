from agent_behaviours import go_towards_ball, follow_agent
from agent import agent  # Assuming there's an 'Agent' class in 'agent' module
import math
import numpy as np
from prm_planner import PRMPlanning

class BasicAgentGraph(agent):
    def __init__(self, id, world2robot_fn=None):
        super().__init__(id)
        self.world2robot_fn = world2robot_fn

    def act(self, frame):
        # Extract robot and ball positions
        ball_position = np.array([frame['detection']['ball']['x'], frame['detection']['ball']['y']])
        robot_data = frame['detection']['robots_blue'][self.id]
        robot_position = (robot_data['x'], robot_data['y'])

        # Convert ball position from numpy array to tuple
        ball_position_tuple = tuple(ball_position)

        # Extract obstacles positions
        obstacles = []
        for _, yellow_robot in frame['detection']['robots_yellow'].items():
            obstacles.append((yellow_robot['x'], yellow_robot['y']))
        for id, blue_robot in frame['detection']['robots_blue'].items():
            if id != self.id:
                obstacles.append((blue_robot['x'], blue_robot['y']))

        # Initialize PRMPlanning with field dimensions in millimeters
        prm = PRMPlanning(xy_min=(-4000, -3300), xy_max=(4000, 3300))
        graph = prm.populate_graph(obstacles, num_samples=100, radius=500)  # Adjust num_samples and radius as needed
        
        # Find path
        path = prm.find_path(graph, robot_position, ball_position_tuple)
        print("Path:", path)

        # Decide on the velocities based on the path
        # This part needs to be implemented based on how you want to use the path
        vx, vy, vz = 0, 0, 0  # Placeholder for actual velocity calculation
        return self.id, vx, vy, vz

if __name__ == "__main__":
    agent1 = BasicAgentGraph(0)
    test_frame = {'geometry': {}, 'detection': {'ball': {'x': 0, 'y': 0}, 'robots_yellow': {0: {'confidence': 1, 'robot_id': 0, 'x': 1497.5712, 'y': 1120, 'orientation': -3.1415927, 'pixel_x': 1497.5712, 'pixel_y': 1120}, 1: {'confidence': 1, 'robot_id': 1, 'x': 1497.5712, 'y': 5.717139e-12, 'orientation': 3.1415927, 'pixel_x': 1497.5712, 'pixel_y': 5.717139e-12}, 3: {'confidence': 1, 'robot_id': 3, 'x': 547.5712, 'y': -1.8211606e-11, 'orientation': -3.1415927, 'pixel_x': 547.5712, 'pixel_y': -1.8211606e-11}, 4: {'confidence': 1, 'robot_id': 4, 'x': 2497.5713, 'y': -2.955412e-12, 'orientation': 3.1415927, 'pixel_x': 2497.5713, 'pixel_y': -2.955412e-12}, 5: {'confidence': 1, 'robot_id': 5, 'x': 3597.5713, 'y': -1.6777793e-11, 'orientation': -3.1415927, 'pixel_x': 3597.5713, 'pixel_y': -1.6777793e-11}, 2: {'confidence': 1, 'robot_id': 2, 'x': 1497.5712, 'y': -1120, 'orientation': -3.1415927, 'pixel_x': 1497.5712, 'pixel_y': -1120}}, 'robots_blue': {1: {'confidence': 1, 'robot_id': 1, 'x': -1417.4371, 'y': 29.656864, 'orientation': 0.70621175, 'pixel_x': -1417.4371, 'pixel_y': 29.656864}, 2: {'confidence': 1, 'robot_id': 2, 'x': -1440.695, 'y': -1055.0938, 'orientation': 0.70779437, 'pixel_x': -1440.695, 'pixel_y': -1055.0938}, 3: {'confidence': 1, 'robot_id': 3, 'x': -467.43713, 'y': 29.656864, 'orientation': 0.70621175, 'pixel_x': -467.43713, 'pixel_y': 29.656864}, 4: {'confidence': 1, 'robot_id': 4, 'x': -2417.4373, 'y': 29.656864, 'orientation': 0.70621175, 'pixel_x': -2417.4373, 'pixel_y': 29.656864}, 5: {'confidence': 1, 'robot_id': 5, 'x': -3517.4373, 'y': 29.656864, 'orientation': 0.70621175, 'pixel_x': -3517.4373, 'pixel_y': 29.656864}, 0: {'confidence': 1, 'robot_id': 0, 'x': -1415.1483, 'y': 1105.9684, 'orientation': 0.69634324, 'pixel_x': -1415.1483, 'pixel_y': 1105.9684}}}}
    agent1.act(test_frame)