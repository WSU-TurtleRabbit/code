# basic_agent.py
from agent_behaviours import go_towards_ball
from agent import agent

class BasicAgent(agent):
    def __init__(self, id):
        super().__init__(id)

    def act(self, frame):
        if "ball" in frame["detection"]:
            ball_x = frame['detection']['ball']['x']
            ball_y = frame['detection']['ball']['y']
            ball_position = (ball_x, ball_y)
        else:
            ball_position = None
        
        my_x = frame['detection']['robots_blue'][self.id]['x']
        my_y = frame['detection']['robots_blue'][self.id]['y']
        my_position = (my_x, my_y)

        self.vx, self.vy = go_towards_ball(ball_position, my_position)

        self.vz = 0 

        return self.id, self.vx, self.vy, self.vz
