from WSUSSL.World.proto2 import ssl_vision_wrapper_pb2 as wrapper
from WSUSSL.World.proto2 import grSim_Packet_pb2
from WSUSSL.World.proto2 import grSim_Commands_pb2
from WSUSSL.World.model import Model as wm # in short of world_model

import socket
import time

class Receiver:
    def __init__(self,world_model:wm, ip_addr: str, port: int):
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
        self.model = world_model
        
        # print(self)
        self.connect() # connects to the socket

    def connect(self):
        """ Connect self to vision
        """
        if not isinstance(self.ip_addr, str):
            raise ValueError('IP type should be string type')
        if not isinstance(self.port, int):
            raise ValueError('Port type should be int type')
        
        print(self.ip_addr, self.port)
        self.receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.receive_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        self.receive_sock.bind((self.ip_addr, self.port))
        
        group = '224.5.23.2'
        self.receive_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(group) + socket.inet_aton("0.0.0.0"))
        print("connection to vision established")
        

    def listen_world(self):
        """_summary_
            listens to the UDP broadcast data
        Raises:
            UserWarning: self.recieve_sock doesn't exist
            TypeError: No world Model
        """
        if self.receive_sock is None:
             raise UserWarning('connect() needs to be called before listen()')
        
        if not isinstance(self.model, wm):
            raise TypeError(f'expected world_model, got {self.model.__class__}')
        
        while True: #while it is true, it will always listen and update world model with the data
            data = self.receive()
            self.update_world_model(data)
            
    def receive(self):
        """Receive package and decode."""
        data, _ = self.receive_sock.recvfrom(2048)
        decoded_data = wrapper.SSL_WrapperPacket().FromString(data)
        return decoded_data
    
    
    def update_world_model(self, data):
        """_summary_
            This updates the world model
        Args:
            data: data recieved from ssl-vision
        """

        if data.HasField('detection'):
            self.model.update_detection(data.detection)
            #print(data.detection)

        if data.HasField('geometry'):
            self.model.update_geometry(data.geometry)
            #print(data.geometry)


### SSL-VISION ### 
class ssl_vision_receiver(Receiver):
    
    def __init__(self, world_model:wm, ip_addr="224.5.23.2", port=10006):
        """_summary_
            This class is specifically used for connecting to ssl vision
        Args:
            world_model (Model): the world model from loop
            ip_addr (str, optional): ssl-vision ip address. Defaults to "224.5.23.2".
            port (int, optional): ssl-vision port num. Defaults to 10006.
        """
        super().__init__(world_model, ip_addr, port)
  
    
# class proto2_grsim_py_receiver(Receiver):
#     def __init__(self, ip_addr, port):
#         """WORKING IN PROGRESS
#         This function will be processing data from GR sim
#         Args:
#             ip_addr (str): ip addr of grsim client UDP
#             port (int): port num of grsim client UDP
#         """
#         super().__init__(ip_addr, port)

#     def update_world_model(self, data):
#         """WORKING IN PROGRESS
#             This will be updating world model with environment
#         Args:
#             data: data from GRsim
#         """
#         pass

class grsim_coms(Receiver):
    def __init__(self, world_model:wm, vision_ip_addr = "224.5.23.2", vision_port = 10020, 
                 command_listen_port = 20011, control_port = 10300,
                 blue_status_port = 30011, yellow_status_port = 30012,  
                 blue_control_port = 10301,yellow_control_port = 10302):
        """_summary_
            grSim's initial Communication Configuration set up. 
            This is used to establish connection with GRSIM. 
            If you have changed any values on the GRSIM application
            Please update them correspondingly.
        Args:
            vision_ip_addr (str, optional): vision multicast ip address. Defaults to '224.5.23.2'.
            vision_port (int, optional): vision mulicast port number. Defaults to 10020.
            command_listen_port (int, optional): command listen port. Defaults to 20011.
            control_port (int, optional): Simulation control port. Defaults to 10300.
            blue_status_port (int, optional): Blue Team status send port. Defaults to 30011.
            yellow_status_port (int, optional): Yellow Team Status send port. Defaults to 30012.
            blue_control_port (int, optional): Blue Team control port. Defaults to 10301.
            yellow_control_port (int, optional): Yellow Team control port. Defaults to 10302.
        """
        self.vision_ip_addr = vision_ip_addr
        self.vision_port = vision_port
        super().__init__(world_model,vision_ip_addr,vision_port)    

        self.command_port = command_listen_port
        self.blue_status_port = blue_status_port
        self.yellow_status_port = yellow_status_port
        self.control_port = control_port
        self.blue_control_port = blue_control_port
        self.yellow_control_port = yellow_control_port
        self.init_socks()

    def init_socks(self):
         # Initialize sockets for communication
        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.blue_status_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.yellow_status_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.blue_control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.yellow_control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind sockets to their respective ports
        self.blue_status_socket.bind((self.vision_ip_addr, self.blue_status_port))
        self.yellow_status_socket.bind((self.vision_ip_addr, self.yellow_status_port))
        print(f"{self.blue_status_socket}")
        print(f"{self.yellow_status_socket}")
     
    def receive_status(self):
        data, _ = self.blue_status_socket.recv(1024)
        data = data.decode()
        print(data)
        
    def send(self,port_type,encoded_message):
        """_summary_
            Sends message to grsim.
        Args:
            port_type (str): Which port you want to send to.
            message (bytes): command of grsim
        """
        match port_type:
            case "command":
                port = self.command_port
                #message = grSim_commands()
            case "control":
                port = self.control_port
            case "blue":
                port = self.blue_control_port
                #message = grSim_robot_command()
            case "yellow":
                port = self.yellow_control_port
                #message = grSim_robot_command()

                             
        self.send_sock.sendto(encoded_message, (self.vision_ip_addr, port))

    @staticmethod
    def grSim_robot_command(id, kickspeedx, kickspeedz, veltangent, velnormal,
                            velangular, spinner, wheelspeed, wheel1=0.0, wheel2=0.0, 
                            wheel3=0.0, wheel4=0.0):
        
        return grSim_Commands_pb2.grSim_Robot_Command(
            id, kickspeedx, kickspeedz, veltangent, velnormal, velangular, 
            spinner, wheelspeed, wheel1, wheel2, wheel3, wheel4
        )
    
    @staticmethod
    def grSim_commands(timestamp, isteamyellow, robot_commands):
        return grSim_Commands_pb2.grSim_Commands(
            timestamp, isteamyellow, robot_commands
        )
    
#if __name__ == '__main__':
    #recv = proto2_ssl_vision_py_receiver('127.0.0.1', 50514) #e.g.
    #recv.connect() 
    #recv.update_world_model()
