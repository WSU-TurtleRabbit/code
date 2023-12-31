import subprocess
import json
import socket
from grSim_Packet_pb2 import grSim_Packet
from random_agent import RandomAgent
from avoid import Avoid

class Simulation():
    def __init__(self, agents):
        self.agents = agents
        self.detection = {"ball": {"x": None, "y": None}, "robots_yellow": {}, "robots_blue": {}}
        self.geometry = {}

    def handle_player_frame(self, data):
        print(data)
        balldata = data["balls"][0]
        self.detection["ball"]["x"] = balldata["x"]
        self.detection["ball"]["y"] = balldata["y"]
        
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
                
                    
    def is_ready(self):
        return (len(self.detection["robots_yellow"]) == 6) and (len(self.detection["robots_blue"]) == 6)

    def get_data(self):
        
        return {"geometry": self.geometry, "detection": self.detection}
        

    
    
    
    
    def handle_field_frame(self, data):
        self.geometry = data






        
    def run(self):
       # Run the SSL-Vision client as a subprocess
        with subprocess.Popen(["./ssl-vision-cli"], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, text=True) as proc:
            for line in iter(proc.stdout.readline, ''):
                try:
                    # Parse the JSON string to a Python dictionary
                    frame_data = json.loads(line.strip())

                    # Handle the frame data
                    self.handle_player_frame(frame_data)
            
                except json.JSONDecodeError as e:
                    
                    frameerror=line.strip()
                    index = frameerror.find('{"frame_number"')
                    frame1 = json.loads(frameerror[:index])
                    frame2 = json.loads(frameerror[index:])
                    self.handle_field_frame(frame1)
                    self.handle_player_frame(frame2)
                if self.is_ready():
                    for agent in self.agents:
                        result = agent.act(self.get_data())
                        self.send_command(*result)

        
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
        
    

agent1 = RandomAgent(1)
agent2 = RandomAgent(2)
sim = Simulation([agent1, agent2])
sim.run()