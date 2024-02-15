import socket
#from grSim_Packet_pb2 import grSim_Packet
import time
import threading



# Class for sending commands to grSim
class grSimCommandSender:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_command(self, robot_id, vx, vy, vw, is_team_yellow=False):
        packet = grSim_Packet()
        commands = packet.commands
        commands.timestamp = 0.0
        commands.isteamyellow = is_team_yellow

        command = commands.robot_commands.add()
        command.id = robot_id
        command.kickspeedx = 0.0
        command.kickspeedz = 0.0
        command.veltangent = vx
        command.velnormal = vy
        command.velangular = vw
        command.spinner = False
        command.wheelsspeed = False

        message = packet.SerializeToString()
        self.sock.sendto(message, (self.ip, self.port))



# Class for sending commands to a physical robot
class PhysicalRobotCommandSender:
    def __init__(self, ip, port, send_rate=0.1):
        self.ip = ip 
        self.port = port 
        self.send_rate = send_rate
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_command(self, W, Vx, Vy):
        message = f"{W},{Vx},{Vy}".encode()
        # Use a thread for messages that aren't blocked
        send_thread = threading.Thread(target=self.threaded_send, args=(message,))
        send_thread.start()

    def threaded_send(self, message):
        self.sock.sendto(message, (self.ip, self.port))
        #time.sleep(self.send_rate)

