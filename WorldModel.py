
class WorldModel:
    def __init__(self):
        """
        init : setting the team color as your own team and some other default values
        """

        self.team_color = input('team color : ')
        if(self.team_color == 'y'):
            self.isYellow = True
        else:
            self.isYellow = False
        
        self.ball_position = None
        self.our_robots = {} # Dictionary with robot IDs as keys and positions as values
        self.opponent_robots = {} # Similar structure for opponent robots

    def update_detection(self,detection):
        self.frameNum = detection.frame_number
        #self.ball_data = detection.balls
        self.ball_position =  self.extract_ball_position(detection.balls)
        self.all_yellow = self.extract_all_robots_pos(detection.robots_yellow)
        self.all_blue = self.extract_all_robots_pos(detection.robots_blue)
        #print(self.all_yellow)
        # change into receiving x y z data etc only

    def extract_ball_position(self, balls):
        try:
            for ball in balls:
                ball_position = (ball.x, ball.y)
               # print("ball : ",ball_position)
        except Exception as e :
            print(e)
            ball_position = None
            #fix this ?
        finally: 
            return ball_position
    
    def extract_all_robots_pos(self,robots):
        """
        break down the all robot positions and store them in a dictionary.
        """
        r = {}
        for robot in robots:
            s = {}
            s["x"] = robot.x 
            s["y"] = robot.y
            s["o"] = robot.orientation
            r[str(robot.robot_id)] = s
        print(r)
        return r

        

    def update_geometry(self,geometry):
        print()

    def update_ball_position(self, position):
        """
        Update the position of the ball.
        :param position: A tuple (x, y) representing the ball's position.
        """
        self.ball_position = position

    def update_robot_position(self, robot_id, position, is_our_team):
        """
        Update the position of a robot.
        :param robot_id: Identifier for the robot.
        :param position: A tuple (x, y) representing the robot's position.
        :param is_our_team: Boolean indicating if the robot is on our team.
        """
        if is_our_team:
            self.our_robots[robot_id] = position
        else:
            self.opponent_robots[robot_id] = position

    def get_ball_position(self):
        """
        Return the current position of the ball.
        """
        return self.ball_position

    def get_robot_position(self, robot_id, is_our_team):
        """
        Get the position of a specific robot.
        :param robot_id: Identifier for the robot.
        :param is_our_team: Boolean indicating if the robot is on our team.
        :return: Position of the robot or None if not found.
        """
        rid = str(robot_id)
        if is_our_team: # your team
            if(self.isYellow):
            # return information
                return self.all_yellow.get(rid)
            else : 
                return self.all_blue.get(rid)
        else: # enemy team
            if(self.isYellow): #
            # return information
                return self.all_blue.get(rid)
            else : 
                return self.all_yellow.get(rid)

    # Additional methods can be added here to provide more functionality
    # like calculating distances between objects, checking for collisions, etc.

    # Example usage:
world_model = WorldModel()
# world_model.update_ball_position((100, 150))
# world_model.update_robot_position(1, (50, 100), True) # Our team's robot
# world_model.update_robot_position(3, (200, 250), False) # Opponent's robot