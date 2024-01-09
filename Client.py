## Run this before the server script

import socket
import time
import numpy as np
import moteus


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

def Move(vx,vy,w,rt):
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
    # give an ending timer
    t_end = time.time()+rt
    # while the time is not at endtime yet,
    while time.time() <t_end:
        print(time.time(), t_end)
        #move according to their own wheel velocity
        print("moving at :",w1,w2,w3,w4)
        
# at this time, the robot will be moved accordingly and should be stopped after the timer is up
# Thus, it will be returned at the main loop        
    

# main function
def main ():
    # suggestion : add init() function ?

    # initialising UDP address and Port number
    # these two has to be the same as the server.py
    UDP_IP_ADDRESS = "127.0.0.1"
    UDP_PORT_NO = 6789

    ## initalising clientsocket for internet and UDP
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ## binding the IP address and UDP port number
    clientSock.bind((UDP_IP_ADDRESS,UDP_PORT_NO))

    while True:
        data, addr = clientSock.recvfrom(1024) #buffersize is 1024 bytes
        
        #make the robot move
        if (data != ""):
            print ("Received: ", data)
            vx,vy,w,rt = Convert(data)
            Move(vx,vy,w,rt)
            # resets the data so it can receive new data afterwards
            data = ""
        

    
main()
