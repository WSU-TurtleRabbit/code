from WSUSSL.World.proto2 import ssl_vision_wrapper_pb2
from WSUSSL.World.proto2 import grSim_Packet_pb2
from WSUSSL.World.proto2 import grSim_Commands_pb2
from WSUSSL.World.model import Model as wm # in short of world_model

import socket

class proto2_ssl_receiver:
    def __init__(self, ip_addr: str, port: int):
        """
            This is the parent Class for ssl-vision and GRsim
        Args:
            ip_addr (str): address of the software's UDP
            port (int): port number of the software's UDP
        Params:
            sock(socket): the UDP socket that connects to software
            model(world_model):
        """
        self.ip_addr = ip_addr
        self.port = port
        self.sock = None
        #self.model = model
        self.connect() # connects to the socket
        
    def connect(self):
            """Binds the sock with ip and port and configure to UDP multicast."""

            if not isinstance(self.ip_addr, str):
                raise ValueError('IP type should be string type')
            if not isinstance(self.port, int):
                raise ValueError('Port type should be int type')
            
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 128)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
            self.sock.bind((self.ip_addr, self.port))

            host = socket.gethostbyname(socket.gethostname())
            self.sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
            self.sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, 
                    socket.inet_aton(self.ip_addr) + socket.inet_aton(host))
            
    def receive(self):
        """Receive package and decode."""

        data, _ = self.sock.recvfrom(1024)
        decoded_data = ssl_vision_wrapper_pb2.SSL_WrapperPacket().FromString(data)
        return decoded_data
    # def connect(self):
    #     """Connect self to the socket
    #     """
    #     print(self.ip_addr, self.port)
    #     self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     #self.sock.bind((self.ip_addr, self.port))

    def listen(self):
        if self.sock is None:
             raise UserWarning('connect() needs to be called before listen()')
        
        if not isinstance(self.model, wm):
            raise TypeError(f'expected world_model, got {self.model.__class__}')
        
        while True:
            data = self.receive()
            self.update_world_model(data)
    
    def update_world_model(self, data):
        """_summary_
            Function no longer in use. 
            This is just for testing purposes
        """
        raise NotImplementedError

    def set_world_model(self, model:wm):
        self.model = model

class proto2_ssl_vision_py_receiver(proto2_ssl_receiver):
    
    def __init__(self, ip_addr="224.5.23.2", port=10006):
        """_summary_
            This class is specifically used for connecting to ssl vision
        Args:
            ip_addr (str, optional): _description_. Defaults to "224.5.23.2".
            port (int, optional): _description_. Defaults to 10006.
        """
        super().__init__(ip_addr, port)
  
    def update_world_model(self, data):
        """_summary_
            This updates the world model
        Args:
            data: data recieved from ssl-vision
        """

        if data.HasField('detection'):
            self.model.update_detection(data.detection)
            print(data.detection)

        if data.HasField('geometry'):
            self.model.update_geometry(data.geometry)
            print(data.geometry)

class proto2_grsim_py_receiver():
    def __init__(self, ip_addr, port):
        """WORKING IN PROGRESS
        This function will be processing data from GR sim
        Args:
            ip_addr (str): ip addr of grsim client UDP
            port (int): port num of grsim client UDP
        """
        super().__init__(ip_addr, port)

    def update_world_model(self, data):
        """WORKING IN PROGRESS
            This will be updating world model with environment
        Args:
            data: data from GRsim
        """
        pass

class proto2_grsim_py_generator():
    def __init__(self, grsim_ip_addr, grsim_port):
        """Connects to GRsim -> sends message
        Args:
            grsim_ip_addr (str): ip addr of the grsim client UDP
            grsim_port (_type_): port num of the grsim client UDP
        """
        self.grsim_ip_addr = grsim_ip_addr
        self.grsim_port = grsim_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def send(self, message):
        """_summary_
            Sends message to grsim.
        Args:
            message (bytes): command of grsim
        """
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
    
#if __name__ == '__main__':
    #recv = proto2_ssl_vision_py_receiver('127.0.0.1', 50514) #e.g.
    #recv.connect() 
    #recv.update_world_model()
