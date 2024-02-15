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
        w = np.append(w, 1)  
        r = np.dot(trans_matrix, w)[:2]  
        return r

    def send_command(self, robot_id, W, Vx, Vy, robot_pose=None):
        if self.is_simulator:
            self.send_command_to_grSim(robot_id, W, Vx, Vy)
        else:
            if robot_pose is not None:
                # Apply transformation if robot pose is provided
                Vx, Vy = self.world2robot(np.array([Vx, Vy]), robot_pose)[:2]
            self.send_command_to_physical_robot(W, Vx, Vy)

    def send_command_to_physical_robot(self, W, Vx, Vy):
        message = f"{W},{Vx},{Vy}".encode()
        self.sock.sendto(message, (self.ip, self.port))
        time.sleep(self.send_rate)

    def send_command_to_grSim(self, robot_id, W, Vx, Vy):
        packet = grSim_Packet()
        commands = packet.commands
        commands.timestamp = 0.0
        commands.isteamyellow = False  # Set this according to your team color

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

# Example usage
#if __name__ == "__main__":
    # For physical robot
    #dispatcher_physical = CommandDispatcher("172.20.10.14", 5005)
    #robot_pose = np.array([0, 0, -pi/2])  # Example pose
    #dispatcher_physical.send_command(0, 0, -1.0, -1, robot_pose)

    # For grSim
    #dispatcher_sim = CommandDispatcher("127.0.0.1", 20011, is_simulator=True)
    #dispatcher_sim.send_command(0, 0, 1.0, 0.5)  # No pose needed for simulator
