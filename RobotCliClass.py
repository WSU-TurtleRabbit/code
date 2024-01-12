import socket
import os 
import random

SERVER = {
    "IP" : "",
    "PORT" : ""
}


class RobotCli:

    def __init__(self):
        self.id = int(input(id))
        self.b_id = bytes(str(self.id).encode())
        self.sock, self.ip, self.port= self.CreateSock()
        self.Listen()
            # Sends message to server
    
    def sendMessage(self, msg):
        self.sock.sendto(msg,(SERVER["IP"], int(SERVER["PORT"])))
        print(msg," has been sent")



    #classes that are only accessible in this script

    def CreateSock(self):
        #normal socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        #Broadcast channel
        bSOCK = socket.socket(socket.AF_INET, #internet
                            socket.SOCK_DGRAM, #UDP coms
                            socket.IPPROTO_UDP # UDP broadcast
                            )
        bSOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        bSOCK.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        try:
            bSOCK.bind(("",12342))
            print(bSOCK)
        except Exception as e:
            print("Error in binding Broadcast :", type(e))
            print(e)
            exit()

        # locate IP 
        # For this instance, we will be using the os to do that
        #Windows: 
        #Linux : 
        ip = os.popen('hostname -I').read().split(" ")[0]
        binding = True
        while binding:
            try :
                port = random.randint(5000,9000)
                sock.bind((ip,port))
                self.sock = sock
                binding = False
            except Exception as e:
                print("error in binding",e)
                pass
            finally :
                print(ip, port)
        data,addr = bSOCK.recvfrom(1024)
        print(data)
        SERVER["IP"],SERVER["PORT"] = data.decode().split(", ")
        print(SERVER, (SERVER["IP"],SERVER["PORT"]))
        msg = self.b_id
        self.sendMessage(msg)

        return sock, ip, port






    # after finished initialise
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
                    newMsg = "Moving"
                except Exception as e:
                    print(e)
                    exit()

            if(newMsg != ""):    
                self.sendMessage(newMsg)
                
def Move(vx,vy,w,rt):
    print(vx,vy,w,rt)



#Apply to server for ID
def ApplyID(serverAddr):
    id = 0
    while id == 0 : 
        print('hi')

            
    return

Robot = RobotCli()