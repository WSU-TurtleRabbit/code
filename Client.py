## Run this before the server script

import socket
import time
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
    # calculate the different wheel speed
    w1,w2,w3,w4 = 0,1,1,2 #some calculation 
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
            data = ""
        

    
main()
