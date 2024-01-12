import socket
import os 
import random


class RobotCli:

    def __init__(self):
        self.id = int(input(id))
        self.b_id = bytes(str(self.id).encode())
        self.sock, self.ip, self.port= CreateSock()
        Listen(self)


def Listen(self):
    while True: 
        data, addr = self.sock.recvfrom(1024) #buffersize is 1024 bytes
        msg = data.decode()
        if (msg == "ping"):
            newMsg = self.b_id
        else : 
            try: 
                vx,vy,w,rt = msg.split(",",3)
                vx = int(vx)
                vy = int(vy)
                w = int(w)
                rt = int(rt)
                self.Move(vx,vy,w,rt)
            except Exception as e:
                print(e)
                exit()

        if(newMsg != ""):    
            self.sock.sentto(newMsg,addr)

                
def Move(vx,vy,w,rt):
    print(vx,vy,w,rt)



def CreateSock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # locate IP 
    # For this instance, we will be using the os to do that
    #Windows: 
    #Linux : 
    IP = os.popen('hostname -I').read().split(" ")[0]
    binding = True
    while binding:
        try :
            PORT = random.randint(5000,9000)
            sock.bind(("",PORT))
            binding = False
        except Exception as e:
            print("error in binding",e)
        finally :
            print(IP, PORT)
    return sock, IP, PORT

Robot = RobotCli()