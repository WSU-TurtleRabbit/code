import socket
import os
import sys
import random
import time

c = time.localtime()
TIME = time.strftime("%H:%M:%S", c)

from WSUSSL.Shared.action import Action

class Server:

    def __init__(self,skill_pipe, max_robots=6):
        """_summary_
            UDP side server. 
            The server will broadcast it's address over broadcast
            When the server recieves a client request, the server will then allow user to assign id to robot client
            The server will then sends back id 
        Args:
            max_robots (int): number for maximum robot to be active
        PARAMS : 
            ip (str) : stores ip addresss (used in create sock)
            ss_addr(tuple) : tuple of server send sock address
            rs_addr (tuple) : tuple of server recieve sock address
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
        self.ip = None
        self.ss_addr = None
        self.rs_addr = None
        self.robots = dict()
        self.active = dict()
        self.max_robots = max_robots
        self.gamestate = "ACTIVE"
        self.create_sock() # creates the sockets (UDP, Broadcast)
        self.find_robots() # looks for robots on the net using the 2 sockets
        self.skill_pipe = skill_pipe
        
    def create_sock(self):
        """_summary_
            creates socketes
        Params: 
            sender (socket) : send message to all / individual robots
            receiver (socket) : receive message from all robots
            broadcaster (socket) : broadcasting messages to everything on the net only *NO RECIEVE*
            bind_success (bool): boolean to determine whether the binding process is successful.

            
        Returns:
            _type_: _description_
        """
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.ip = socket.gethostbyname(socket.gethostname()) #windows
        if sys.platform == 'linux':
            self.ip = os.popen('hostname -I').read().strip().split(" ")[0]
        
        self.sender,self.ss_addr = self.bind_sock(self.sender)
        self.receiver,self.rs_addr = self.bind_sock(self.receiver)
        
    def bind_sock(self,sock:socket.socket):
        bind_success = False
        while not bind_success:
            try:
                port = random.randint(5000, 9000)
                addr = (self.ip, port)
                sock.bind(addr)
                bind_success = True
            except Exception as e:
                print(e)
                pass
            finally:
                print("Socket Binded : ", bind_success)
        return sock, addr



    def find_robots(self):
        """_summary_
            This function is triggered after the server sockets are initialised
            This is used to locate the robots and trigger id assignation
        """
        # Set the maximum number of robots you want to discover

        while len(self.robots) < self.max_robots:
            self.broadcast_all(str(self.rs_addr),10,True)
                
                

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
                        
    def listen_udp(self,expire=1):
        """Server listening on UDP

        Args:
            expire (int,optional): timer for setting time out on listen. Default: 1s

        Returns:
            data: if message received from Client (Robot), return it.
        """
        self.receiver.settimeout(expire)
        try:
            data, addr = self.receiver.recvfrom(1024)
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
            
                
    def broadcast_all(self, msg: str,timer=5,countrobots=False):
        """Broadcasting Message to ALL Clients on the network

        Args:
            msg (str): the message that you want to broadcast
            timer(int): the time that you want this broadcast to last for. Default: 5s
        """
        eTime = time.time() + timer
        #message that needs to be broadcasted
        msg = bytes(msg.encode('utf-8'))
        if countrobots:
            while time.time() < eTime and len(self.robots) < self.max_robots:
                self.broadcaster.sendto(msg, ('<broadcast>', 12342))
                print("Broadcasting :", msg)
                self.listen_udp(1)
        else : 
            while time.time()<eTime:
                self.broadcaster.sendto(msg, ('<broadcast>', 12342))
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
        self.sender.sendto(msg, self.robots[str(id)])
        time.sleep(2)
    
    def send_action(self, action: Action):
        # from action object, locate id
        robot_id = str(getattr(action, "id"))
        # From ID obtained, get it's address
        addr = self.robots[robot_id]
        # sends the action to that robot
        self.sender.sendto(action.encode(),addr)
        print(f"{action} has been sent to Robot (ID) : {robot_id}")

    def run(self):
        while True:
            action = self.skill_pipe.recv()
            self.send_action(action)