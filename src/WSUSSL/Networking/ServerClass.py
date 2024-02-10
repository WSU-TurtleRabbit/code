import socket
import os
import sys
import random
import time

c = time.localtime()
TIME = time.strftime("%H:%M:%S", c)

from WSUSSL.Shared.action import Action

class Server:

    def __init__(self, max_robots=6):
        """_summary_
            UDP side server. 
            The server will broadcast it's address over broadcast
            When the server recieves a client request, the server will then allow user to assign id to robot client
            The server will then sends back id 
        Args:
            max_robots (int): number for maximum robot to be active
        PARAMS : 
            os (str) : stores operating system info (not in use now)
            ip (str) : stores ip addresss (used in create sock)
            port (int) : stores port num (used in create sock)
            addr (tuple) : stores information about the server's address
            robots (dict) : dictionary of robots and it's addresses
            active (dict) : dictionary of all robots last active time.
            max_robots (int) : int to decide on what is the maximum number of robots for the server to look for
            gamestate (str) : the game state. (Can be replaced in the future)
        Functions: 
            0. creating it's own sockets
            1. broadcast to all robots
            2. send custom message to a robot
            3. sends action to a specific robot
            4. recieves feedback message from robots 

        """
        self.os = None
        self.ip = None
        self.port = None
        self.addr = None
        self.robots = dict()
        self.active = dict()
        self.max_robots = max_robots
        self.gamestate = "ACTIVE"
        self.create_sock() # creates the sockets (UDP, Broadcast)
        self.find_robots() # looks for robots on the net using the 2 sockets
        
    def create_sock(self):
        """_summary_
            creates socketes
        Params: 
            sock (socket) : send / recives message on the same network
            bsock (socket) : broadcasting messages to everything on the net only *NO RECIEVE*
            bind_success (bool): boolean to determine whether the binding process is successful.

            
        Returns:
            _type_: _description_
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.bsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        self.ip = socket.gethostbyname(socket.gethostname()) #windows
        if sys.platform == 'linux':
            self.ip = os.popen('hostname -I').read().strip().split(" ")[0]
        

        bind_success = False
        while not bind_success:
            try:
                self.port = random.randint(5000, 9000)
                self.addr = tuple([self.ip, self.port])
                print(self.addr)
                self.sock.bind(self.addr)
                bind_success = True
            except Exception as e:
                print(e)
                pass
            # finally:
            #     print("Socket Binded : ", bind_success)



    def find_robots(self):
        """_summary_
            This function is triggered after the server sockets are initialised
            This is used to locate the robots and trigger id assignation
        Params:
            server (bytes) : encoded message - server address
            data (bytes) : encoded message recieved via UDP
            addr (tuple) : UDP address received (aka the client that sends the message)
        """
        
        server = bytes(str(self.addr).encode('utf-8'))

        # Set the maximum number of robots you want to discover

        while len(self.robots) < self.max_robots:
            print("Broadcasting info", server)

            # Initialise timer.
            max_broadcast_time = time.time()+10
            while time.time()< max_broadcast_time and len(self.robots) < self.max_robots:
                # Broadcasting server Info @broadcasting port
                self.bsock.sendto(server, ('<broadcast>', 12342))
                print("Broadcasting")
                
                self.listen_udp(1)
                

    def assign_ID(self,addr):
        print("Robot Connection Request Received")
        isSetting = True
        while isSetting:
            print("Please enter the designated Robot id")
            print("Currently active : ", self.robots.keys())
            try : 
                id = int(input("Please Enter Robot id:"))
                robot_id = str(id)
                if id<= 6 and robot_id not in self.robots.keys():
                    isSetting = False
                    self.robots[robot_id] = addr
                    self.active[robot_id] = TIME
                    print(f"New Robot {self.robots[robot_id]} has been added at {self.active[robot_id]}")
                    print("Currently active: ", self.robots.keys())
                    self.send_message(robot_id,robot_id)                
                else : 
                    print("Try another ID")
            except Exception as e:
                print(e)
                
    
    def ping_all(self):
        """_summary_
            This function is used to ping all robots regularly
            This function will use the self.robots dictionary and access them.
        """
        # customised message : ping
        msg = b'ping'
        while self.gamestate == "ACTIVE":
            eTime = time.time()+10 # 10s after current time
            for i in range(6):
                robot_id = str(i+1)
                last_active_time = self.active[robot_id]
                print(last_active_time - TIME)
                if last_active_time-TIME >= 5:
                    # check if robot last seen time is larger than 5
                    #sets status = False
                    status = False
                    # starts ping
                    while time.time() < eTime and not status:
                        self.send_message(msg,robot_id)
                        info = self.listen_udp(1)
                        print(info)
                        if info != None:
                            status = True                    
                        print(f"Robot id : {robot_id} is Alive : {status}")

                    if status == True:
                        #updates last seen time
                        self.active[robot_id] = TIME
                        
                    else: #remove robot from list
                        del self.robots[robot_id]
                        del self.active[robot_id]
                        
    def listen_udp(self,expire:int):
        self.sock.settimeout(expire)
        try:
            data, addr = self.sock.recvfrom(1024)
            data = data.decode()
            print(f"message: '{data}' is recieved from {addr}")
            if data == "new":
                self.assign_ID(addr)
                return 
            else:
                if addr in self.robots.values():
                    i = list(self.robots.values()).index(addr)
                    id = list(self.robots.keys())[i]
                    print(f"message received from Robot: {id} @ {addr} at {TIME}")
                    # update last checkin timer
                    self.active[id] = TIME
                    return data
                print(data)
        except socket.timeout:
            return
            
                
    def broadcast_all(self, msg: str):
        eTime = time.time() + 5
        #message that needs to be broadcasted
        msg = bytes(msg.encode('utf-8'))

        while time.time() < eTime:
            self.bsock.sendto(msg, ('<broadcast>', 12342))
            print("Broadcasting :", msg)
            

        
    # Try not to use this 
    def send_message(self, msg:str, id:str):
        """_summary_
            This function sends direct message to a specific robot (id)
        Args:
            msg (str): message string
            id (str): Robot ID in string
        """
        msg = bytes(msg.encode('utf-8'))
        # while not received, repeat 5 times
        self.sock.sendto(msg, self.robots[str(id)])
        time.sleep(2)
    
    def send_action(self, action: Action):
        # from action object, locate id
        robot_id = str(getattr(action, "id"))
        # From ID obtained, get it's address
        addr = self.robots[robot_id]
        # sends the action to that robot
        self.sock.sendto(action.encode(),addr)
        print(f"{action} has been sent to Robot (ID) : {robot_id}")
        
        
