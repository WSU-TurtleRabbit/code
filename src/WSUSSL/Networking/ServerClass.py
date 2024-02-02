import socket
import os
import sys
import random
import time

c = time.localtime()
TIME = time.strftime("%H:%M:%S", c)

from WSUSSL.Shared.action import Action

class Server:

    def __init__(self, max_robots:int ):
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
        
        # ip = socket.gethostbyname(socket.gethostname())
        # if sys.platform == 'Linux':
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
        
        server = str(self.addr)

        # Set the maximum number of robots you want to discover

        while len(self.robots) < self.max_robots:
            print("Broadcasting info", server)

            # Initialise timer.
            max_broadcast_time = time.time()+10
            while time.time()< max_broadcast_time and len(self.robots) < self.max_robots:
                # Broadcasting server Info @broadcasting port
                self.bsock.sendto(server, ('<broadcast>', 12342))
                print("Broadcasting")
                try:
                    # Set a timeout for receiving responses
                    self.sock.settimeout(1)
                    # waits for 1 seconds response time. 
                    data, addr = self.sock.recvfrom(1024)
                    # if there's anything received, decode it.
                    data = data.decode()
                    print(data)
                    # triggers id setup
                    self.assign_ID(addr)
                except socket.timeout:
                    # Ignore timeouts and continue broadcasting
                    pass

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
        
        # looks for (6) robots
        for i in range(6):
            # default : false
            status = False
            robot_id = str(i+1)
            try:
                addr = self.robots[robot_id]
                while not status:
                    # sending using broadcast
                    self.bsock.sendto(msg, addr)
                    # receiving using UDP port
                    data, addr = self.sock.recvfrom(1024)
                    info = data.decode()
                    print(info)
                    status = True
                    self.active[robot_id] = TIME
            except socket.error as e:
                print(f"Cannot connect Robot {robot_id}: {e}")
                del self.robots[robot_id]
                del self.active[robot_id]
                # find robots again.
            except Exception as e:
                print(e)
            finally:
                print(f"Pinged Robot id: {robot_id}, Alive = {status}")

    def broadcast_all(self, msg: str):
        endT = time.time() + 5
        all_received = False # bool for all robots being able to recieve the broadcast
        
        #message that needs to be broadcasted
        msg = bytes(msg.encode('utf-8'))

        while time.time() < endT:
            self.bsock.sendto(msg, ('<broadcast>', 12342))
            print("Broadcasting :", msg)
            
            # will try to boradcast and listen for feedback
            try:
                # Set a timeout for receiving responses
                self.sock.settimeout(1)
                data, addr = self.sock.recvfrom(1024)
                data = data.decode()
                print(data)
                #checks for who is sending the message
                if addr in self.robots.values():
                    # get robot id
                    i = list(self.robots.values()).index(addr)
                    id = list(self.robots.keys())[i]
                    print(f"message : '{data}' received from Robot: {id} @ {addr} at {TIME}")
                    # update last checkin timer
                    self.active[id] = TIME
                else :  #this means that device doesn't exist in our log 
                    print("New unknown device found")
                    # enable user input ? 
                    add = input("1. add 2. ignore")
                    #if add then assign new id and save it
                    if (add == "1"):
                        self.assign_ID(addr)
                    else:
                        print("ignored")

            except socket.timeout:
                # Ignore timeouts and continue broadcasting
                pass

        
    def send_message(self, msg, id):
        #todo
        msg = bytes(msg.encode('utf-8'))
        self.sock.sendto(msg, self.robots[str(id)])
        time.sleep(2)
    
    def send_action(self, action: Action):
        # from action object, locate id
        robot_id = str(getattr(action, "id"))
        # get the addresses of robot from server.robot dictionary
        addr = self.robots[robot_id]
        self.sock.sendto(action.encode(),addr)
        print("action sent")
        
