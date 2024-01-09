# agent_simulator.py


import subprocess
import json
import socket
from grSim_Packet_pb2 import grSim_Packet
from random_agent import RandomAgent
from basic_agent import BasicAgent
import time

class Simulation():
    def __init__(self, agents):
        self.agents = agents
        self.detection = {"ball": {"x": None, "y": None}, "robots_yellow": {}, "robots_blue": {}}
        self.geometry = {}


    # This function updates the internal model of the simulation
    # with 'detection' data (live coordinates of all players and the ball)
    # 
    def handle_player_frame(self, data):
        print(data)
        if "balls" in data:
            balldata = data["balls"][0]
            self.detection["ball"]["x"] = balldata["x"]
            self.detection["ball"]["y"] = balldata["y"]
            print()
            print("balls")
            print(balldata)
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
        return (len(self.detection["robots_yellow"]) == 6) and (len(self.detection["robots_blue"]) == 6)
    

    # Function for agents to retrieve the game state
    def get_data(self):
        
        return {"geometry": self.geometry, "detection": self.detection}
        

    
    
    
    # Function to update the internal model with "geometry" data:
    # the static field dimension data
    def handle_field_frame(self, data):
        self.geometry = data






    # This is the main function that will read lines from the ssl-vision-client
    # in a loop. It will parse the JSON output data, split it according to 
    # "detection" and "geometry" data, and send it to their respective
    # "handling" functions.
    def run(self):
       # Run the SSL-Vision client as a subprocess
        with subprocess.Popen(["./ssl-vision-cli"], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, text=True) as p:
            for line in iter(p.stdout.readline, ''):
                start_time = time.time()
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
                # Check if all robot data is in dictionaries
                if self.is_ready():
                    # Loop through the agents
                    for agent in self.agents:
                        # Retrieve desired velocities from each agent's act method
                        result = agent.act(self.get_data())
                        # Send desired velocities to send_command function
                        self.send_command(*result)
                        end_time = time.time()
                        print(start_time, end_time)

                

        
    def send_command(self, robot_id, vx, vy, vw):
        packet = grSim_Packet()
        packet.commands.timestamp = 0.0
        packet.commands.isteamyellow = False

        command = packet.commands.robot_commands.add()
        command.id = robot_id
        command.kickspeedx = 0.0
        command.kickspeedz = 0.0
        command.veltangent = vx
        command.velnormal = vy
        command.velangular = vw

        # Setting the required fields
        command.spinner = False  
        command.wheelsspeed = False  

        message = packet.SerializeToString()

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message, ('127.0.0.1', 20011))
        
    

agent1 = BasicAgent(5)
agent2 = RandomAgent(4)
agent3 = BasicAgent(1)
agent4 = BasicAgent(2)
agent5 = BasicAgent(6)
agent6 = BasicAgent(7)
sim = Simulation([agent1, agent2, agent3])
sim.run()