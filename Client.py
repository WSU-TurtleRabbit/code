## Run this before the server script

import socket
import time
import numpy as np
import moteus
import random


## Function to conver the data obtained from the server to 4 separate values
def Convert(data):
    data = data.decode()
    print(data, "\n", type(data))
    vx, vy, w, rt = 0,0,0,0
    ## we use try so we can see if we get any error over here
    try:
        ## using .split method to split the 4 different values
        vx,vy,w,rt = data.split(',')
        vx = int(vx)
        vy = int(vy)
        w = int(w)
        rt = int(rt)
    except:
        ## prints the following message if any error has occured
        print ("error in spliting string values")
    finally:
        ## after it finished, the 4 values will be printed and returned to the main function
        print("New Values : ",vx, vy, w, rt)
        print(type(rt))
        return vx,vy,w,rt 

def Cal(vx,vy,w):
    '''
    "Modern Robotics: Mechanics, Planning & Control"
    13.2.1
    
    just leaving this here for no particular reason:
    libgen (dot) rs
    '''
    # placehoder values
    r = 1  #radius
    b = np.array([1,1,1,1]) #different angl values
    d = np.array([1,1,1,1]) #different wheel values
    
    Vb = np.array([w, vx, vy])
    H = np.array([[-d[0], -d[1], -d[2], -d[3]],
            [np.cos(b[0]), np.cos(b[1]), -np.cos(b[2]), -np.cos(b[3])],
            [np.sin(b[0]), -np.sin(b[1]), -np.sin(b[2]), np.sin(b[3])],
            ])
    
    # [H (transposed) (dot) Vb]/r
    u = (H.T@Vb)/r
    # calculate the different wheel speed
    w1,w2,w3,w4 = u[0],u[1],u[2],u[3] #some calculation 
    return w1,w2,w3,w4
    
    
def Move(w1,w2,w3,w4):
 # potentially: replace with moteus code to get them moving according to their own wheel velocity
        print("moving at :",w1,w2,w3,w4)
        
    

# main function
def main ():
    # suggestion : add init() function ?
    Robot_id = random.randint(1,6)
    str_Robot_id = str(Robot_id)
    byteRID = str_Robot_id.encode()
    print(Robot_id)
    print(byteRID)
    
    # initialising UDP address and Port number

    #Randomising UDP IP and Port num
    UDP_IP_ADDRESS = "127.0.0." + str(random.randint(1,9))
    UDP_PORT_NO = random.randint(6000,6100)

    ## initalising clientsocket for internet and UDP
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ## binding the IP address and UDP port number
    clientSock.bind((UDP_IP_ADDRESS,UDP_PORT_NO))
    serverIP = "127.0.1.1" 
    serverPort = 9000 

    clientSock.sendto(byteRID,(serverIP,serverPort))

    while True:
        data, addr = clientSock.recvfrom(1024) #buffersize is 1024 bytes
        data = data.decode()
        print(data)
        #make the robot move
        if (data == 'status check'):
            clientSock.sendto(byteRID, (addr))
            data = ''
            

        elif (data != ""):
            # debug message recived
            print ("Received: ", data)
            vx,vy,w,rt = Convert(data)
            t_end = time.time()+rt
            while time.time() <t_end:
                w1,w2,w3,w4 = Cal(vx,vy,w)
                Move(w1,w2,w3,w4)
                time.sleep(rt)
        

        

            
            #windows debug
            # data = str(input())
            # if (data == "exit"):
            #     clientSock.close()
            #     exit()
    
main()
