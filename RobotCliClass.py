import socket
import os
import random
import time

SERVER = {
    "IP": "",
    "PORT": ""
}


class RobotCli:

    def __init__(self):
        self.id = self.get_robot_id()
        print(f"This Robot is now with ID: {self.id}")
        self.b_id = bytes(str(self.id).encode())
        self.sock, self.ip, self.port = self.create_sock()
        self.listen()

    def send_message(self, msg):
        self.sock.sendto(msg, (SERVER["IP"], int(SERVER["PORT"])))
        print(f"{msg} has been sent")

    
    def move(self, vx, vy, w, rt):
        v1,v2,v3,v4 = calculate(vx,vy,w)
        endTime = time.time() + rt
        while time.time() < endTime:
            print(vx, vy, w, rt)

    # Classes that are only accessible in this script

    def create_sock(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        bsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        bsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        try:
            bsock.bind(("", 12342))
        except Exception as e:
            print("Error in binding Broadcast:", type(e))
            print(e)
            raise  # Raise an exception
        
        #ip = ''
        ip = os.popen('hostname -I').read().split(" ")[0]
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

    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            msg = data.decode()

            if msg == "ping":
                new_msg = self.b_id
            else:
                try:
                    vx, vy, w, rt = map(int, msg.split(",", 3))
                    self.move(vx, vy, w, rt)
                    new_msg = "Moving"
                except Exception as e:
                    print(e)
                    raise

            if new_msg != "":
                self.send_message(new_msg)

    @staticmethod
    def get_robot_id():
        while id == 0:
            try:
                id = input("Please Enter Robot ID: ")
                int(id)
            except Exception as e:
                print(e)
                id = 0
            
        return id

def calculate(vx,vy,w):
        #inputing eqn
        v1,v2,v3,v4 = 0,0,0,0
        return v1,v2,v3,v4


# Apply to server for ID
def apply_id(server_addr):
    id = 0
    while id == 0:
        print('hi')


Robot = RobotCli()
