# agent_simulator.py
import subprocess
import json
import socket
import numpy as np
from numpy import pi
from numpy.linalg import inv
import time

from grSim.grSim_Packet_pb2 import grSim_Packet
from random_agent import RandomAgent
from basic_agent import BasicAgent
from basic_agent_trans import BasicAgentTrans
from general_agent import GeneralAgent
from command_senders import grSimCommandSender, PhysicalRobotCommandSender
from sim_path_agent import SimulationAgent




class Simulation():
    def __init__(self, agents):
        self.agents = agents
        for agent in self.agents:
            agent.world2robot_fn = self.world2robot
        self.detection = {"ball": {"x": None, "y": None}, "robots_yellow": {}, "robots_blue": {}}
        self.geometry = {}
        self.grSimSender = grSimCommandSender("127.0.0.1", 20011)
        self.physicalRobotSender = PhysicalRobotCommandSender("172.20.10.14", 5005)


    @staticmethod
    def transformation_matrix(p):
        c = np.cos(p[2])  # Cosine of orientation
        s = np.sin(p[2])  # Sine of orientation
        return np.array([
            [c, -s, p[0]],
            [s,  c, p[1]],
            [0,  0,  1]
        ])
    

    
    @staticmethod
    def world2robot(w, p):
        trans_matrix = np.linalg.inv(Simulation.transformation_matrix(p))
        w = np.append(w, 1)  
        r = np.dot(trans_matrix, w)[:2]  
        return r




    # Main loop for receiving data from ssl-vision-client. Can be swapped for a UDP
    # server. 
    def receive_data(self):
        with subprocess.Popen(["./ssl-vision-client/cmd/ssl-vision-cli/ssl-vision-cli"], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, text=True) as p:
            for line in iter(p.stdout.readline, ''):
                self.process_data(line)


    def process_data(self, line):
        try:
            # Parse the JSON string to a Python dictionary
            frame_data = json.loads(line.strip())

            # Handle the frame data
            self.handle_player_frame(frame_data)
            
        except json.JSONDecodeError as e:
            # Splitting of the JSON into "detection" and "geometry" happens here
            frameerror=line.strip()
            index = frameerror.find('{"frame_number"')
            frame1 = json.loads(frameerror[:index])
            frame2 = json.loads(frameerror[index:])
            self.handle_field_frame(frame1)
            self.handle_player_frame(frame2)
            # print(frame2)
            # Check if all robot data is in dictionaries

        if self.is_ready():
            # Loop through the agents
            for agent in self.agents:
                ball_position = [self.detection["ball"]["x"], self.detection["ball"]["y"]]
                if isinstance(agent, GeneralAgent) or isinstance(agent, SimulationAgent):
                    # Set the agent's target to the ball's position
                    agent.set_target(ball_position)
                # Retrieve desired velocities from each agent's act method
                robot_id, vx, vy, vw = agent.act(self.get_data())
                # Send desired velocities to send_command function

                self.grSimSender.send_command(robot_id, vx, vy, vw, is_team_yellow=False)


                #self.physicalRobotSender.send_command(vw, vx, vy)

                # print(f"Real robot velocities: {vw}, {vx}, {vy}")




    # This function updates the internal model of the simulation
    # with 'detection' data (live coordinates of all players and the ball)
    # 
    def handle_player_frame(self, data):
        #print(data)
        if "balls" in data and data["balls"]:
            first_ball = data["balls"][0]  
            self.detection["ball"]["x"] = first_ball.get("x", 0)  
            self.detection["ball"]["y"] = first_ball.get("y", 0) 
            #print("Ball data:", first_ball)
        if "robots_yellow" in data:
            yellow_players = data["robots_yellow"]
            for yellow_player in yellow_players:
                robot_id = yellow_player["robot_id"]
                self.detection["robots_yellow"][robot_id] = yellow_player
                
                
        if "robots_blue" in data:
            blue_players = data["robots_blue"]
            for blue_player in blue_players:
                robot_id = blue_player["robot_id"]
                self.detection["robots_blue"][robot_id] = blue_player

    # Function returns true if the dictionaries of robot IDs have been filled with
    # 6 players on each team
    def is_ready(self):
        return (len(self.detection["robots_yellow"]) >= 6) and (len(self.detection["robots_blue"]) >= 6)
    

    # Function for agents to retrieve the game state
    def get_data(self):
        
        return {"geometry": self.geometry, "detection": self.detection}
        


    
    
    # Function to update the internal model with "geometry" data:
    # the static field dimension data
    def handle_field_frame(self, data):
        self.geometry = data






    # This function will simply run the receive_data function (which is the main loop)
    def run(self):
        self.receive_data()
        print("The simulation has ended or has been interrupted")

                

        
    





basic_agent = SimulationAgent(5)



sim = Simulation([basic_agent])
sim.run()
