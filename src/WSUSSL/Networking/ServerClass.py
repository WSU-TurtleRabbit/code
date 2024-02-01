import socket
import os
import sys
import random
import time

# Dictionary
ADDR = {} # list of robot and their addresses
LAST = {} # list of robot and their last seen time
c = time.localtime()
TIME = time.strftime("%H:%M:%S", c)

class Server:

    def __init__(self):
        
        self.create_sock() # creates the sockets (UDP, Broadcast)
        self.find_robots() # looks for robots on the net using the 2 sockets
        
    def create_sock(self):
        """_summary_
            creates socketes
        Params: 
            sock(UDP-socket) : send / recives message on the same network
            bsock (socket) : broadcasting messages to everything on the net only *NO RECIEVE*
            
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
            This function is triggered after the server is created
            This is used to broadcast and receives feedback from the robots
        Params:
        
        """
        
        server_addr = str(self.addr).encode("utf-8")

        # Set the maximum number of robots you want to discover
        max_robots_to_discover = 2

        while len(ADDR) < max_robots_to_discover:
            print("Broadcasting info", server_addr)

            # Set the maximum time for broadcasting in seconds
            max_broadcast_time = time.time()+10

            while time.time()< max_broadcast_time and len(ADDR) < max_robots_to_discover:
                # Broadcasting server Info @broadcasting port
                self.bsock.sendto(server_addr, ('<broadcast>', 12342))
                print("Broadcasting")

                try:
                    # Set a timeout for receiving responses
                    self.sock.settimeout(1)
                    data, addr = self.sock.recvfrom(1024)
                    data = data.decode()
                    # triggers id setup
                    robot_id = assign_ID(addr)
                    self.send_message(robot_id,robot_id)
                    # robot_id = str(data.decode())
                    # print(f"Received RobotID: {robot_id} response from the address : {addr}")
                    # # Add/update the received data
                    # ADDR[robot_id] = addr
                    # LAST[robot_id] =TIME
                    # # Debug check
                    # print(ADDR)
                    # print(LAST)
                except socket.timeout:
                    # Ignore timeouts and continue broadcasting
                    pass

    def ping_all(self):
        """_summary_
            This function is used to ping all robots regularly
            This function will use the ADDR dictionary and access them.
        """
        # customised message : ping
        msg = b'ping'
        
        # looks for (6) robots
        for i in range(6):
            # default : false
            status = False
            robot_id = str(id)
            try:
                addr = ADDR[robot_id]
                while not status:
                    self.bsock.sendto(msg, addr)
                    data, addr = self.sock.recvfrom(1024)
                    info = data.decode()
                    print(info)
                    status = True
                    LAST[robot_id] = TIME
            except socket.error as e:
                print(f"Cannot connect Robot {id}: {e}")
                del ADDR[robot_id]
                del LAST[robot_id]
                # find robots again.
            except Exception as e:
                print(e)
            finally:
                print(f"Pinged Robot id: {id}, Alive = {status}")

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
                if addr in ADDR.values():
                    # get robot id
                    i = list(ADDR.values()).index(addr)
                    id = list(ADDR.keys())[i]
                    print(f"message : '{data}' received from Robot: {id} @ {addr} at {TIME}")
                    # update last checkin timer
                    LAST[id] = TIME
                else : 
                    print("New unknown device found")
            except socket.timeout:
                # Ignore timeouts and continue broadcasting
                pass

        
    def send_message(self, msg, id):
        #todo
        msg = bytes(msg.encode('utf-8'))
        self.sock.sendto(msg, ADDR[str(id)])
        time.sleep(2)
    
    def send_action(self, action):
        robot_id = str(getattr(action, "id"))
        addr = ADDR[robot_id]
        self.sock.sendto(action.encode(),addr)
        print("action sent")
        

    
def assign_ID(addr):
    print("Robot Connection Request Received")
    isSetting = True
    while isSetting:
        print("Please enter the designated Robot id")
        print("Current active ones are : ", ADDR.keys())
        try : 
            id = int(input("Please Enter Robot id:"))
            robot_id = str(id)
            if id<= 6 and robot_id not in ADDR.keys():
                isSetting = False
                ADDR[robot_id] = addr
                LAST[robot_id] = TIME
                print(f"New Robot {ADDR[robot_id]} has been added at {LAST[robot_id]}")
                print("Current active ones are : ", ADDR.keys())

                return robot_id 
            else : 
                print("Try another ID")
        except Exception as e:
            print(e)
            
    return None