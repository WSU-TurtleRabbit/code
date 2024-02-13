import time #we might want to have our own timer
from multiprocessing import Pipe

class Model:
    def __init__(self,isYellow = False):
        """_summary_
            This function initialises the WorldModel.
            The user will first have to input the team color
            1 char will be recommended
        Param:
            isYellow: is a boolean to identify if our team is yellow or not.
        """
        # identifying whether using GRsim or SSLvision

        # self.team_color = input('team color : ')
        # if(self.team_color == 'y'):
        #     self.isYellow = True
        # else:
        #     self.isYellow = False

        self.isYellow = isYellow
        self.cameras = list()
        # currently not used, but will be used in the future (maybe)
        self.balls = None
        self.yellows = {}
        self.blues = {}
        self.our_robots = {} # Dictionary with robot IDs as keys and positions as values
        self.opponent_robots = {} # Similar structure for opponent robots
    
    def update_detection(self,detection):
        """_summary_
            This function is used to retrieve all "detection" data from ssl-vision-cli (terminal)
        Args: 
            detection: data about frames, robots and balls
        Params:
            frameNum: gets the current frame number.
            ball_position: sets ball's x,y position.
            all_yellow : stores all yellow team robot ID and position.
            all_blue : stores all blue team robot ID and position.
        """
        print("updating field detection data ...")
        self.frame_number = detection.frame_number
        self.t_capture = detection.t_capture
        self.t_sent = detection.t_sent
        self.count_camera(detection.camera_id)
        self.camera_num = len(self.cameras)
        self.extract_ball_position(detection.balls)
        self.update_team(detection.robots_yellow,detection.robots_blue)
        self.print_to_file()
        print(self.get_robot_position(2,True))
        
    def count_camera(self,cameraid):
        self.c_camera = str(cameraid)
        if cameraid not in self.cameras:
            self.cameras.append(cameraid)
        
            
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

        __REMARKS__
            This function only works with one ball on field
        """
        self.balls = {}
        i = 0
        # if the field has at least 1 ball
        for ball in balls:
            i +=1
            # updates this module's ball position
            #ball_position = (ball.x, ball.y)
            self.balls[str(i)] = {"c":ball.confidence,"x":ball.x,"y":ball.y,"px":ball.pixel_x,"py":ball.pixel_y}
           # print(self.listofballs)
            
        #return self.ball_position
    
    def update_team(self,yellow_team, blue_team):
        self.yellows = self.extract_all_robots_pos(self.yellows,yellow_team)
        self.blues = self.extract_all_robots_pos(self.blues,blue_team)
        if self.isYellow:
            self.our_robots = self.yellows
            self.opponent_robots = self.blues
        else:
            self.our_robots = self.blues
            self.opponent_robots = self.yellows
        print("us: ",self.our_robots)
        print("enemy : ",self.opponent_robots)
    
    def extract_all_robots_pos(self,robotlist,robots):
        """_summary_
            This funtion is used to break down a team's robot id and position, 
            and store them in a new dictionary.
        Returns:
            dictionary : a dictionary of robots 
        """
        for robot in robots:
            s = {"c":robot.confidence, "x":robot.x, "y":robot.y, "o":robot.orientation, "px": robot.pixel_x, "py":robot.pixel_y}
            robotlist[str(robot.robot_id)] = s
        sorted_robotlist = {k: robotlist[k] for k in sorted(robotlist)}
        return sorted_robotlist
        
        #print(r)

    
        
    # working in progress
    def update_geometry(self,geometry):
        """_summary_
            Retrieves data about the field
        Args:
            geometry (data): data about field
        """
        #print("updating field geometry data ...")
        field = geometry.field
        self.field_length = field.field_length
        self.field_width = field.field_width
        self.goal_width = field.goal_width
        self.goal_depth = field.goal_depth
        self.boundary_width = field.boundary_width
        #fieldlines and data
        self.lines = {}
        self.arc = {}
        self.extract_field_lines(field.field_lines)
        self.extract_field_arc(field.field_arcs)
        
    def extract_field_lines(self, lines):
        for line in lines:
            name = line.name
            p1 = (line.p1.x, line.p1.y)
            p2 = (line.p2.x, line.p2.y)
            self.lines[name]={"p1":p1, "p2": p2,"thickness":line.thickness}
        #print(self.lines)
    
    def extract_field_arc(self,arcs):
        for arc in arcs:
            center = (arc.center.x, arc.center.y)
            self.arc[arc.name] = {"center":center,"radius":arc.radius,"a":(arc.a1,arc.a2),"thickness":arc.thickness} 
        #print(self.arc)

    def get_ball_position(self):
        """_summary_
            This functions retrieves the ball x and y values
            If there are more than 1 ball on the field, 
            it will return the first ball only
            
            Usage : (use "_" to ignore the data that you don't need )
            e.g. 
                1. gets all 3 data
                ball,ball_x,ball_y = model.get_ball_position()
                2. gets ball's x and y data
                _,ball_x,ball_y = model.get_ball_position()
                3. gets ball's dictionary only 
                ball,_,_ = model.get_ball_position()
        Returns:
            1. Dictionary (returns everything available)
            2. ball x position
            3. ball y position
        """
        ball_x = self.balls["1"]["x"]
        ball_y = self.balls["1"]["y"]
        return self.balls, ball_x, ball_y

    def get_robot_position(self, robot_id, is_our_team):
        """
        Get the position of a specific robot.
        :param robot_id: Identifier for the robot.
        :param is_our_team: Boolean indicating if the robot is on our team.
        :return: Position of the robot or None if not found.
        """
        rid = str(robot_id)
        try:
            if is_our_team: # your team
                robot_data = self.our_robots.get(rid)
            else: # enemy team
                robot_data = self.opponent_robots.get(rid)
            robot_x = robot_data["x"]
            robot_y = robot_data["y"]
            robot_o = robot_data["o"]
            print(f"Robot: {robot_id} is found at {robot_x}, {robot_y} ")
            return robot_x,robot_y,robot_o
        except TypeError as te:
            print(f"{te}, Robot Not Found")
            pass
    # Additional methods can be added here to provide more functionality
    # like calculating distances between objects, checking for collisions, etc.
    def print_to_file(self):
        """prints 2 Team robot data and ball position to file
        """
        # Open a file for writing
        with open("world_model_output.txt", "w") as file:
            team_color = "Yellow" if self.isYellow else "Blue"
            enemy_color = "Blue" if self.isYellow else "Yellow"
            
            file.write(f"Team TurtleRabbit is color: {team_color}\n")

            # Iterate over the items and write them to the file
            for robot_id in self.our_robots:
                robot = self.our_robots[robot_id]
                file.write(f"robot id : {robot_id}\n x:{robot['x']}\n y: {robot['y']}\n o: {robot['o']}\n")
            
            file.write(f"Team Enemy is color: {enemy_color}\n")
            for robot_id in self.opponent_robots:
                robot = self.opponent_robots[robot_id]
                file.write(f"robot id : {robot_id}\n x:{robot['x']}\n y: {robot['y']}\n o: {robot['o']}\n")
            #num_ball = len(self.balls)
            file.write(f"Balls On Field : {len(self.balls)}\n")
            for ball in self.balls:
                file.write(f"ball:{ball}\n Ball_pos: ({self.balls[str(ball)]['x']}, {self.balls[str(ball)]['y']})\n")
                