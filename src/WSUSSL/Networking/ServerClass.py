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
        self.sock, self.bsock, self.ip, self.port = create_sock()
        self.find_robots()

    def find_robots(self):
        """_summary_
            This function is triggered after the server is created
            This is used to broadcast and receives feedback from the robots
        Params:
        
        """
        
        server_addr = f"{self.ip}, {self.port}".encode()

        # Set the maximum number of robots you want to discover
        max_robots_to_discover = 1

        while len(ADDR) <= max_robots_to_discover:
            print("Broadcasting info", server_addr)

            # Set the maximum time for broadcasting in seconds
            max_broadcast_time = time.time()+10

            while time.time()< max_broadcast_time:
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
        msg = b'ping'
        for i in range(6):
            status = False
            id = i+1
            s_id = str(id)
            try:
                addr = ADDR[s_id]
                while not status:
                    self.sock.sendto(msg, addr)
                    data, addr = self.sock.recvfrom(1024)
                    info = data.decode()
                    print(info)
                    status = True
                    LAST[s_id] = TIME
            except socket.error as e:
                print(f"Cannot connect Robot {id}: {e}")
                del ADDR[s_id]
                del LAST[s_id]
            except Exception as e:
                print(e)
            finally:
                print(f"Pinged Robot id: {id}, Alive = {status}")

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
        

def create_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    bsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    bsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    bsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    # ip = socket.gethostbyname(socket.gethostname())
    # if sys.platform == 'Linux':
    ip = os.popen('hostname -I').read().strip().split(" ")[0]
    

    binding = True
    while binding:
        try:
            port = random.randint(5000, 9000)
            sock.bind((ip, port))
            binding = False
        except Exception as e:
            print(e)
            pass
        finally:
            ADDR["Server"] = sock.getsockname()
            print(ADDR["Server"])
    return sock, bsock, ip, port

def assign_ID(addr):
    print("Robot Connection Request Received")
    isSetting = True
    while isSetting:
        print("Please enter the designated Robot id")
        print("Current active ones are : ", ADDR)
        try : 
            id = int(input("Please Enter Robot id:"))
            robot_id = str(id)
            if id<= 6 and robot_id not in ADDR.keys():
                isSetting = False
                ADDR[robot_id] = addr
                LAST[robot_id] = TIME
                print(f"New Robot {ADDR[robot_id]} has been added at {LAST[robot_id]}")
                return robot_id 
            else : 
                print("Try another ID")
        except Exception:
            print(Exception)
            
    return None