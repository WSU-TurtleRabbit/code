import socket
import os
import random
import ipaddress 
import time
from RobotClass import Robot

# Dictionary
ADDR = {
     
}
LAST = {
     
}
c =  time.localtime()
TIME = time.strftime("%H:%M:%S", c)

class Server(): 

    # #LIST : 
    # robots = list() # Stores RobotIDs 
    # robotsAddr = list() # Stores corresponding Robot Address

    def __init__(self):
        self.sock, self.ip, self.port= CreateSock()
        self.addr = ADDR["Server"]
        self.broadcast() 
        #broadcast message
    
    def broadcast(self):
    # Creating a broadcast message
        bSOCK = socket.socket(socket.AF_INET, #internet
                            socket.SOCK_DGRAM, #UDP coms
                            socket.IPPROTO_UDP # UDP broadcast
                            )
        bSOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        bSOCK.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        serverAddr = str(self.ip+", "+str(self.port)).encode()
        print(ADDR)
        
        
        while len(ADDR) < 4:
            bSOCK.sendto(serverAddr,('',12342))
            print("Broadcasting")
            data, addr = self.sock.recvfrom(1024) #buffersize is 1024 bytes
            # if the server recieves a hi
            print(data, addr)
            RobotID = data.decode()
            ADDR[RobotID]=(addr)
            LAST[RobotID] = TIME
            print(ADDR)
            print(LAST)

            

    def SendMessage(self,msg,addr):
            self.Sock.sendto(msg,addr)
            time.sleep(2)


    def pingAll(self): 
            msg = b'ping'
            timer = 0.5
            id = 1
            for id in range (7):
                status = False
                s_id = str(id)            
                try:
                    addr = ADDR[s_id]
                    while status == False: 
                        self.sock.sendto(msg,addr)
                        data, addr = self.sock.recvfrom(1024) #buffersize is 1024 bytes
                        time.sleep(2)
                        info = data.decode()
                        print(info)
                        status = True
                        LAST [s_id] = TIME
                except ConnectionError : 
                    print("cannot connect Robot : ", id)
                    ADDR[s_id].remove()
                    LAST[s_id].remove()
                    #status = False
                except Exception as e:
                    print (e)
                finally: 
                    print("pinged Robot id :", id, "Alive =", status)
                    

                


def CreateSock():
    # initiate Socket
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
            sock.bind((IP,PORT))
            binding = False
        except Exception as e:
            print(e)
            pass
        finally :
            ADDR["Server"] = sock.getsockname()
            #print(sock.getsockname())
            print(ADDR["Server"])
    return sock, IP, PORT


    
    # def decode message

    # def stop (id, )
    # whenever the 
    
    


    
   
    

        
        


    ## MAIN ###
    # This is the main function of the serverClass
    # When this class first started, it will run the following
    
    # def main() : 



    # if __name__ == "__main__" : 
    #     main()