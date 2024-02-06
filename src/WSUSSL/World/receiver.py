from WSUSSL.World.proto2 import ssl_vision_wrapper_pb2
from WSUSSL.World.proto2 import grSim_Packet_pb2
from WSUSSL.World.proto2 import grSim_Commands_pb2

import socket

class proto2_ssl_vision_py_receiver():
    def __init__(self, ssl_vision_ip_addr="224.5.23.2", ssl_vision_port=10006):
        self.ssl_vision_ip_addr = ssl_vision_ip_addr
        self.ssl_vision_port = ssl_vision_port
        self.ssl_vision_client = None

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind((self.ssl_vision_ip_addr, self.ssl_vision_port))

    def update_world_model(self, model):
        if self.client is None:
            raise UserWarning('call connect() before update_world_model()')
        
        while True:
            data, addr = self.client.recvfrom(1024)
            ssl_vision_wrapper = ssl_vision_wrapper_pb2.SSL_WrapperPacket()
            wrapper = ssl_vision_wrapper.FromString(data)

            if wrapper.HasField('detection'):
                model.update_detection(wrapper.detection)

            if wrapper.HasField('geometry'):
                model.update_detection(data.geometry)

class proto2_grsim_py_receiver():
    def __init__(self, grsim_ip_addr, grsim_port):
        self.grsim_ip_addr = grsim_ip_addr
        self.grsim_port = grsim_port
        self.client = None

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind((self.grsim_ip_addr, self.grsim_port))

    def update_world_model(self, model):
        if self.client is None:
            raise UserWarning('call connect() before update_world_model()')
        
        while True:
            data, addr = self.client.recvfrom(1024)
            
class proto2_grsim_py_generator():
    def __init__(self, grsim_ip_addr, grsim_port):
        self.grsim_ip_addr = grsim_ip_addr
        self.grsim_port = grsim_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def send(self, message):
        self.socket.sendto(message, (self.grsim_ip_addr, self.grsim_port))

    @staticmethod
    def grsim_robot_command(id, kickspeedx, kickspeedz, veltangent, velnormal,
                            velangular, spinner, wheelspeed, wheel1=0.0, wheel2=0.0, 
                            wheel3=0.0, wheel4=0.0):
        
        return grSim_Commands_pb2.grSim_Robot_Command(
            id, kickspeedx, kickspeedz, veltangent, velnormal, velangular, 
            spinner, wheelspeed, wheel1, wheel2, wheel3, wheel4
        )
    
    @staticmethod
    def grim_commands(timestamp, isteamyellow, robot_commands):
        return grSim_Commands_pb2.grSim_Commands(
            timestamp, isteamyellow, robot_commands
        )
    
if __name__ == '__main__':
    recv = proto2_ssl_vision_py_receiver('127.0.0.1', 50514)
    recv.connect()
    # recv.update_world_model()
