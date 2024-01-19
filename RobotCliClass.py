import socket
import os
import random
import time

SERVER = {
    "IP": "",
    "PORT": ""
}

## Class for the Robot Client
class RobotCli:

    ## This func. will be triggered when an object is initiated
    def __init__(self):
        # 1. it will try to assign an ID
        self.id = self.get_robot_id()
        self.stop = False
        print(f"This Robot is now with ID: {self.id}")
        # 2. since the messages has to be sent as byte, we convert it into a string then bytes
        self.b_id = bytes(str(self.id).encode())
        # 3. we create a Socket for sending and receiving on the UDP Server.
        self.sock, self.ip, self.port = self.create_sock()
        # After everything has been set, the robot will start listening continuously
        self.listen()

    def create_sock(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        bsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        bsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        try:
            bsock.bind(("", 12342))
        except Exception as e:
            print("Error in binding Broadcast:", type(e))
            print(e)
            raise  # Raise an exception
        
        #windows
        #ip = socket.gethostbyname(socket.gethostname())
        #raspberrypi
        ip = os.popen("hostname -I").read().strip()

        isbinding = True

        while isbinding:
            try:
                port = random.randint(5000, 9000)
                sock.bind((ip, port))
                self.sock = sock
                isbinding = False
            except Exception as e:
                print("Error in binding:", e)
                pass
            finally:
                print(ip, port)

        data, addr = bsock.recvfrom(1024)
        print(data)
        SERVER["IP"], SERVER["PORT"] = data.decode().split(", ")
        print(SERVER, (SERVER["IP"], SERVER["PORT"]))
        msg = self.b_id
        self.send_message(msg)

        return sock, ip, port

    # func for send message
    # this is useful as it optimise the repetition of this line.
    def send_message(self, msg):
        # the socket will send message to the server address and port
        self.sock.sendto(msg, (SERVER["IP"], int(SERVER["PORT"])))
        # feedback on the client when the message has been sent
        print(f"{msg} has been sent")

    

        
    ## This func. is design to calculate and move the robot accordingly
    def move(self):
        #gets the wheel vel data 
        self.v1 = 0
        self.v2 = 1
        self.v3 = 1
        self.v4 = 0
        while not self.stop:
                #set 4 wheel velocity and start moving
                print(vx, vy, w, rt)


    ## This functions provides a loop for recieving message
    def listen(self):
        # while it is active
        while not self.stop:
            data, addr = self.sock.recvfrom(1024)
            msg = data.decode()

            if msg == "ping":
                new_msg = self.b_id
            else:
                try:
                    # try to check the message 
                    # the robot will be recieving the world and ball dictionary message
                    world, ball = map(int, msg.split(",", 1))
                    # first we wanted to know where the ball and robot is
                    vx, vy, w = self.calculate_velocities(world, ball)

                    # since all velocities are calculated, the ball will now move
                    self.move()
                    #  = map(int, msg.split(",", 3))
                    # self.move(vx, vy, w, rt)
                    # new_msg = "Moving"
                except Exception as e:
                    print(e)
                    raise

            if new_msg != "":
                self.send_message(new_msg)

    @staticmethod
    def get_robot_id():
        id = 0
        while id == 0:
            try:
                id = input("Please Enter Robot ID: ")
                int(id)
            except Exception as e:
                print(e)
                id = 0
            
        return id

    # calculates the velocity for the robot to get to ball.
    def calculate_velocities(self, world, ball):
        """_summary_
        this function calculates the velocities 
        by comparing world data to initial data
        ARGS: 
            world_x = Robot x and y coordinates in the world
        """ 
        print("")   
        # self.x, self.y, self.o

        #Using robtational matrix, adjust how the world precieves the ball
        # and adjust the velocity and position accordingly 
        # generates vx, vy, w.

        # apply rotational matrix
        #

        
    def calculate_wheel_velocities(self,velocity_vector):
        """_summary_
            This function is used to calculate the 4 wheel velocity
            with the [vx, vy, w]
            applies the omniwheel eqn.
        Args: 
            velocity_vector : vector of [vx,vy,w]
        """
        
        # calculate based on omniwheel equations 

        self.w1, self.w2, self.w3, self.w4 =0,0,0,0

# Apply to server for ID # this is not used
def apply_id(server_addr):
        print('do not use this function')


Robot = RobotCli()
