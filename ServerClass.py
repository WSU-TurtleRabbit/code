import socket
import os
import random
import time

# Dictionary
ADDR = {} # list of robot and their addresses
LAST = {} # list of robot and their last seen time
c = time.localtime()
TIME = time.strftime("%H:%M:%S", c)

class Server:

    def __init__(self):
        self.sock, self.ip, self.port = create_sock()
        self.addr = ADDR["Server"]
        self.broadcast()

    def broadcast(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as bsock:
            bsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            bsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            server_addr = f"{self.ip}, {self.port}".encode()

            while len(ADDR) < 6:
                print("Broadcasting info", server_addr)
                #Broadcasting server Info @broadcasting port
                bsock.sendto(server_addr, ('', 12342))
                data, addr = self.sock.recvfrom(1024)
                robot_id = data.decode()
                print(f"Received RobotID: {id} response from the address : {addr}")
                # Add / update the data recieved 
                ADDR[robot_id] = addr
                LAST[robot_id] = TIME
                #debug check
                print(ADDR)
                print(LAST)

    def ping_all(self):
        msg = b'ping'
        for id in range(6):
            status = False
            s_id = str(id)
            try:
                addr = ADDR[s_id]
                while not status:
                    self.sock.sendto(msg, addr)
                    data, addr = self.sock.recvfrom(1024)
                    time.sleep(2)
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

    def send_message(self, msg, addr):
        self.sock.sendto(msg, addr)
        time.sleep(2)

def create_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = os.popen('hostname -I').read().split(" ")[0]
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
    return sock, ip, port
