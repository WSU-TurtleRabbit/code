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
TIME =  time.localtime()
class Server(): 

    # #LIST : 
    # robots = list() # Stores RobotIDs 
    # robotsAddr = list() # Stores corresponding Robot Address

    def __init__(self):
        self.sock, self.ip, self.port= CreateSock()
        self.addr = ADDR["Server"] 
        #broadcast message
    

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
                    while time.time() < time.time() + timer: 
                        self.Sock.sendto(msg,addr)
                        data, addr = self.sock.recvfrom(1024) #buffersize is 1024 bytes
                        time.sleep(2)
                        info = data.decode()
                        print(info)
                        status = True
                        LAST [s_id] = time.strftime("%H:%M:%S", TIME)
                except ConnectionError : 
                    print("cannot connect Robot : ", id)
                    ADDR[s_id].remove()
                    LAST[s_id].remove()
                    status = False
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
            sock.bind(("",PORT))
            binding = False
        except Exception as e:
            print(e)
        finally :
            ADDR["Server"] = (IP, PORT)
            print(IP, PORT)
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