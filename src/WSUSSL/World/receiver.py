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
    
if __name__ == '__main__':
    recv = proto2_ssl_vision_py_receiver('127.0.0.1', 50514)
    recv.connect()
    # recv.update_world_model()
