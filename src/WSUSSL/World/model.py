# import time #we might want to have our own timer
import numpy as np
from collections import defaultdict
# from multiprocessing import Pipe

class Model:
    def __init__(self,isYellow = False):
        """_summary_
            This function initialises the WorldModel.
            The user will first have to input the team color
            1 char will be recommended
        Param:
            isYellow: is a boolean to identify if our team is yellow or not.
        """
        self.history = list()
        self.frame_data = {}
        self.isYellow = isYellow
        self.camera_data = list()
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
            t_capture: the time that the frame was captured
            t_sent: the time that frame was sent.
            camera_num : number of camera used in app
            ball_position: sets ball's x,y position.
            
        """
        print("updating field detection data ...")
        self.frame_number = detection.frame_number
        self.t_capture = detection.t_capture
        self.t_sent = detection.t_sent
        self.camera_id = detection.camera_id
        
        #counts number of campera
        self.camera_num = len(self.cameras)
        for i in range(self.camera_num) :    
            self.extract_ball_position(detection.balls)
            self.update_team(detection.robots_yellow,detection.robots_blue)
            #updates this camera data
            self.camera_data[f"camera{self.camera_id}"] = {
                "balls" : self.balls,
                "our_robots" : self.our_robots,
                "opponent_robots" : self.opponent_robots
            }
        self.save_data()
        
    
    def save_data(self,average=True,framerate=60,frames_to_save = 5):
        # print(self.camera_data.keys())
        # object_count = defaultdict(int)
        # averaged_camera_data={}
        # # frame_data.append(self.camera_data)
        # for key,data in self.camera_data.values():
        #     averaged_camera_data[key] = {} #init
        #     for camera_key,camera_value in data.items():
        #         averaged_camera_data[key][camera_key] = []
        #         for object_key, object_value in camera_value.items():
        #             object_count[object_key]+=1
        #             if object_count >1:
        #                 averaged_camera_data[key][camera_key][object_key] = np.mean

        #             averaged_camera_data[key][camera_key][object_key]
        # self.frame[self.frame_number] = averaged_camera_data

        self.history.append(self.frame_data)
        if (len(self.history) > frames_to_save):
            self.history.pop(0)
        
    
    def update_geometry(self,geometry):
        """_summary_
            Retrieves geometry data about the field and stores in the world_model.
        Args:
            geometry (data): data about field
        """
        print("updating field geometry data ...")
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
        return
            
    def update_team(self,yellow_team, blue_team):
        
        # Extract robot positions
        self.yellows = self.extract_all_robots_pos(self.yellows, yellow_team)
        self.blues = self.extract_all_robots_pos(self.blues, blue_team)
        
        # Determine team colors
        our_team = self.yellows if self.isYellow else self.blues
        opponent_team = self.blues if self.isYellow else self.yellows

        # Assign robots to our team and opponent team
        self.our_robots = our_team
        self.opponent_robots = opponent_team
         
    def update_robot_status(self, robot_dict, status):
        for robot in status:
            robot_id =  robot.robot_id 
            robot_dict[str(robot_id)] = {
                "is_infrared" :robot.infrared,
                "is_flat_kick" : robot.flat_kick,
                "is_chip_kick" : robot.chip_kick
            }
        return robot_dict
    
    

       
    def extract_all_robots_pos(self,robot_dict,robots):
        """_summary_
            This funtion is used to break down a team's robot id and position, 
            and store them in a new dictionary.
        Returns:
            dictionary : a dictionary of robots 
        """
        for robot in robots:
            #stores robot data into the dictionary
            s = {
                "c":robot.confidence, 
                 "x":robot.x, 
                 "y":robot.y, 
                 "o":robot.orientation, 
                 "px": robot.pixel_x, 
                 "py":robot.pixel_y}
            robot_dict[str(robot.robot_id)] = s
        #sorts the robot list according to it's id
        sorted_robot_dict = {k: robot_dict[k] for k in sorted(robot_dict)}
        return sorted_robot_dict
        
        #print(r)  #debug
    
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

    def get_robot_status(self, robot_id, is_our_team):
        rid = str(robot_id)
        try:
            if is_our_team: # your team
                robot_status = self.our_robots.get(rid)
            else: # enemy team
                robot_status = self.opponent_robots.get(rid)
            robot_is_ir = robot_status["is_infrared"]
            robot_is_flat_kick = robot_status["is_flat_kick"]
            robot_is_chip_kick = robot_status["is_chip_kick"]
            return robot_is_ir, robot_is_flat_kick, robot_is_chip_kick
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
                
