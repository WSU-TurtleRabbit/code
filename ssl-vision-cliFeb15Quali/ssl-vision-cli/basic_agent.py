from agent import agent
import math

class BasicAgent(agent):
    def __init__(self, id):
        super().__init__(id)

    def act(self, frame):
        target_x, target_y = self.get_target(frame)
        my_x, my_y = self.get_my_position(frame)
        obstacle_detected, obstacle_pos, dist_to_obstacle = self.detect_obstacle_in_path((my_x, my_y), frame)

        if obstacle_detected:
            self.vx, self.vy, self.vz = self.steer_away_from_obstacle((my_x, my_y), obstacle_pos)
        else:
            self.vx, self.vy = self.go_towards_target((target_x, target_y), (my_x, my_y))
            self.vz = 0

        return self.id, self.vx, self.vy, self.vz

    def get_target(self, frame):
        if "ball" in frame["detection"]:
            return frame['detection']['ball']['x'], frame['detection']['ball']['y']
        return 0, 0

    def get_my_position(self, frame):
        return frame['detection']['robots_blue'][self.id]['x'], frame['detection']['robots_blue'][self.id]['y']

    def go_towards_target(self, target_pos, my_pos):
        tx, ty = target_pos
        mx, my = my_pos
        vx = (tx - mx) * 0.0005
        vy = (ty - my) * 0.0005
        return vx, vy

    def detect_obstacle_in_path(self, my_pos, frame, detection_range=240):
        mx, my = my_pos
        for robot in frame['detection']['robots_blue'].values():
            if robot['robot_id'] != self.id:
                ox, oy = robot['x'], robot['y']
                dist = math.sqrt((mx - ox)**2 + (my - oy)**2)
                if dist < detection_range:
                    return True, (ox, oy), dist
        return False, None, None

    def steer_away_from_obstacle(self, my_pos, obstacle_pos):
        mx, my = my_pos
        ox, oy = obstacle_pos
        steer_angle = math.atan2(oy - my, ox - mx) + math.pi / 2

        vx = math.cos(steer_angle) * 30
        vy = math.sin(steer_angle) * 30
        vz = 0
        return vx, vy, vz
