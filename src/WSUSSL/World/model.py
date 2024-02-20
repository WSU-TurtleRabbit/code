# import time #we might want to have our own timer
import numpy as np
from collections import defaultdict
from multiprocessing import Pipe

class Model:
    def __init__(self,isYellow = False, max_camera=4):
        """_summary_
            This function initialises the WorldModel.
        Param:
            isYellow: is a boolean to identify if our team is YELLOW. Default : BLUE
        """
        self.max_camera = max_camera
        self.isYellow = isYellow
        self.frame_number = 0
        self.frame_count = 0
        self.updated=False

        # currently not used, but will be used in the future (maybe)
        self.balls = {}
        self.yellows = {}
        self.blues = {}
        self.our_robots = {} # Dictionary with robot IDs as keys and positions as values
        self.opponent_robots = {} # Similar structure for opponent robots
        self.yellow_history = list()
        self.blue_history = list()
        self.ball_history = list()
        self.history = list()
        
        
   
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
        #("updating field detection data ...")'
        #print(detection)
        self.set_frame(detection.frame_number)
        self.t_capture = detection.t_capture
        self.t_sent = detection.t_sent
        self.camera_id = detection.camera_id      
        self.extract_ball_position(detection.balls)
        self.update_team(detection.robots_yellow,detection.robots_blue)
        self.update_data()
        
        
    def set_frame(self,frame_number):
        #print(self.frame_number,frame_number)
        if(self.frame_number!=frame_number):
            self.frame_number = frame_number
            self.newFrame = True
        else:
            self.newFrame = False

        
    
    def update_data(self, frames_to_save=5):
        """_summary_
            WORKING IN PROGRESS
        Args:
            average (bool, optional): _description_. Defaults to True.
            framerate (int, optional): _description_. Defaults to 60.
            frames_to_save (int, optional): _description_. Defaults to 5.
        """
        # self.ball_history,self.blue_history,self.yellow_history
        
          
        if self.frame_count >frames_to_save:
            average_blue = self.average(self.blue_history)
            average_yellow = self.average(self.yellow_history)
            average_ball = self.average(self.ball_history)
            if len(self.history) <frames_to_save:
                self.history.append((average_blue,average_yellow,average_ball))
                print(len(self.history))
            else: 
                self.history.pop(0)
            self.blue_history = []
            self.yellow_history = []
            self.ball_history = []
            self.frame_count = 0
            self.updated = True
        
        if self.newFrame or self.frame_count==0: 
            self.blue_history.append(self.blues)
            self.yellow_history.append(self.yellows)
            self.ball_history.append(self.balls)
            self.frame_count +=1
        elif not self.newFrame:
            #update the last history
            self.blue_history[-1] = self.blues
            self.yellow_history[-1] = self.yellows
            self.ball_history[-1] = self.balls
            self.updated = False
            
    def average(self,robotlist):
        averaged_robots,x,y,o,px,py = {},[],[],[],[],[]
        try:
            for i in range(6):
                print(i)
                for data in robotlist:
                    robotdict = dict(data)
                    robot_ids = list(robotdict.keys())
                    #print(robotlist)
                    robot_id = robot_ids[i]
                    x.append(robotdict[robot_id].get("x"))
                    y.append(robotdict[robot_id].get("y"))
                    o.append(robotdict[robot_id].get("o"))
                    px.append(robotdict[robot_id].get("px"))
                    py.append(robotdict[robot_id].get("py"))
                ax,ay,ao,apx,apy = np.array(x),np.array(y),np.array(o),np.array(px),np.array(py)
                averaged = {
                    "x" : round(np.mean(ax,axis=0),4),
                    "y" : round(np.mean(ay,axis=0),4),
                    "o" : round(np.mean(ao,axis=0),4),
                    "px": round(np.mean(apx,axis=0),4),
                    "py": round(np.mean(apy,axis=0),4)
                }
                averaged_robots[robot_id] = averaged
                print (f"average of robot:{averaged_robots}")
            return averaged_robots
        except Exception as e:
            print(e)
        
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
            robot_dict[robot_id] = {
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
                "c":  round(robot.confidence,2), 
                 "x": round(robot.x,4), 
                 "y": round(robot.y,4), 
                 "o": round(robot.orientation,4), 
                 "px": round(robot.pixel_x,4), 
                 "py": round(robot.pixel_y,4)}
            robot_dict[robot.robot_id] = s
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
        
        # if the field has at least 1 ball
        for i, ball in enumerate(balls):
            # updates this module's ball position
            #ball_position = (ball.x, ball.y)
            self.balls[str(i)] = {
                "c":round(ball.confidence,2),
                "x":round(ball.x,4),
                "y":round(ball.y,4),
                "px":round(ball.pixel_x,4),
                "py":round(ball.pixel_y,4)
            }
           # print(self.listofballs)
            
        #return self.ball_position
    
    #ball linear regression
    
        
    def extract_field_lines(self, lines):
        for line in lines:
            name = line.name
            p1 = (line.p1.x, line.p1.y)
            p2 = (line.p2.x, line.p2.y)
            self.lines[name]={
                "p1":p1, 
                "p2": p2,
                "thickness":line.thickness
            }
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
        #rid = str(robot_id)
        try:
            if is_our_team: # your team
                robot_data = self.our_robots.get(robot_id)
            else: # enemy team
                robot_data = self.opponent_robots.get(robot_id)
            robot_x = robot_data["x"]
            robot_y = robot_data["y"]
            robot_o = robot_data["o"]
            print(f"Robot: {robot_id} is found at {robot_x}, {robot_y} ")
            return robot_x,robot_y,robot_o
        except TypeError as te:
            print(f"{te}, Robot Not Found")
            pass

    def get_robot_status(self, robot_id, is_our_team):
       # rid = str(robot_id)
        try:
            if is_our_team: # your team
                robot_status = self.our_robots.get(robot_id)
            else: # enemy team
                robot_status = self.opponent_robots.get(robot_id)
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
                
