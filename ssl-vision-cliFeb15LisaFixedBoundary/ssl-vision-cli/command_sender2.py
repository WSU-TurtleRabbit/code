import numpy as np
from numpy import pi
from numpy.linalg import inv
import socket
import time
from grSim_Packet_pb2 import grSim_Packet

class CommandDispatcher:
    def __init__(self, ip, port, is_simulator=False, send_rate=0.1):
        self.ip = ip
        self.port = port
        self.is_simulator = is_simulator
        self.send_rate = send_rate
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    @staticmethod
    def transformation_matrix(p):
        c = np.cos(p[2])
        s = np.sin(p[2])
        return np.array([
            [c, -s, p[0]],
            [s,  c, p[1]],
            [0,  0,    1]
        ])

    @staticmethod
    def world2robot(w, p):
        trans_matrix = inv(CommandDispatcher.transformation_matrix(p))
        w = np.append(w, 1)  # Convert to homogeneous coordinates
        r = np.dot(trans_matrix, w)[:2]  # Convert back to 2D coordinates
        return r

    def send_command(self, robot_id, W, Vx, Vy, robot_pose=None):
        if robot_pose is not None:
            # Automatically adjust the robot's orientation by subtracting π/2
            adjusted_pose = np.array(robot_pose)
            adjusted_pose[2] -= pi / 2

            # Apply transformation if robot pose is provided
            Vx, Vy = self.world2robot(np.array([Vx, Vy]), adjusted_pose)[:2]

        if self.is_simulator:
            self.send_command_to_grSim(robot_id, W, Vx, Vy)
        else:
            self.send_command_to_physical_robot(W, Vx, Vy)

    def send_command_to_physical_robot(self, W, Vx, Vy):
        message = f"{W},{Vx},{Vy}".encode()
        self.sock.sendto(message, (self.ip, self.port))
        time.sleep(self.send_rate)


    def send_command_to_grSim(self, robot_id, W, Vx, Vy):
        packet = grSim_Packet()
        commands = packet.commands
        commands.timestamp = 0.0
        commands.isteamyellow = False  # Adjust as needed

        command = commands.robot_commands.add()
        command.id = robot_id
        command.kickspeedx = 0.0
        command.kickspeedz = 0.0
        command.veltangent = Vx
        command.velnormal = Vy
        command.velangular = W
        command.spinner = False
        command.wheelsspeed = False

        message = packet.SerializeToString()
        self.sock.sendto(message, (self.ip, self.port))
