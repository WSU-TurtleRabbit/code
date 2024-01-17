
class WorldModel:
    def __init__(self):
        """_summary_
            This function initialises the WorldModel.
            The user will first have to input the team color
            1 char will be recommended
        Args:
            isYellow: is a boolean to identify if our team is yellow or not.
        """

        self.team_color = input('team color : ')
        if(self.team_color == 'y'):
            self.isYellow = True
        else:
            self.isYellow = False
        
        # currently not used, but will be used in the future (maybe)
        self.ball_position = None
        self.our_robots = {} # Dictionary with robot IDs as keys and positions as values
        self.opponent_robots = {} # Similar structure for opponent robots

    def update_detection(self,detection):
        """_summary_
            This function is used to retrieve all "detection" data from ssl-vision-cli (terminal)
        Params:
            frameNum: gets the current frame number.
            ball_position: sets ball's x,y position.
            all_yellow : stores all yellow team robot ID and position.
            all_blue : stores all blue team robot ID and position.
        """
        self.frameNum = detection.frame_number
        #self.ball_data = detection.balls
        self.ball_position =  self.extract_ball_position(detection.balls)
        self.all_yellow = self.extract_all_robots_pos(detection.robots_yellow)
        self.all_blue = self.extract_all_robots_pos(detection.robots_blue)
        #print(self.all_yellow)

    def extract_ball_position(self, balls):
        """_summary_
        This function tries to read ball data from detection.data
        since we will only be working with one ball, we will be keeping it as the following.
        for every ball data encountered, we will store them in the tuple 
        otherwise, if there was no ball data recieved at that frame,
        it will be set as None.

        Params:
            ball: itinerable object
            ball.x: that ball's x coordinates
            ball.y: that ball's y coordinates

        Returns:
            ball_position: returns ball position as a tuple
        """
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
        """_summary_
            This funtion is used to break down a team's robot id and position, 
            and store them in a new dictionary.
        Returns:
            dictionary : a dictionary of robots 
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

        
    # working in progress
    def update_geometry(self,geometry):
        """_summary_
            Retrieves data about the field
        Args:
            geometry (_type_): _description_
        """
        print("Nothing is here, working in progress")

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
