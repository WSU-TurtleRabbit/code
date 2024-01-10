## Importing the socket Python Module
import socket
import time
import os


## Defining the UDP ADDRESS AND PORT NO 
## This has to be the same as the robot.
hostname = socket.gethostname()
# SERVERIP = socket.gethostbyname(hostname)

SERVERIP = os.popen('hostname -I').read().split(" ")[0]
print(f"{SERVERIP=}")
 
print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is:" + SERVERIP) 
SERVERPORT = 5000


## send port, recieving port

## declare our serverSocket upon which we will be listening for UDP messages
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((SERVERIP, SERVERPORT))

#the array to save for ip addresses and ports
addresses = list()
## Arrray to save for RobotID that has been pinged
RobotList = list()

### Checking In ###
# This is a function that first stores the list of robots and it's addresses.
# This has to be run every single time the server starts up
# This has to be run first before the clients (aka the robot "Client.py" Script)
def checkingIn (): 
    # timer 
    timeout = time.time() +10
    
    # if we wanna have a timer to limit the amount of time that it recieves meesage
    #while time.time() < timeout:

    # for debugging, use while true
    while True:
        
        # data, addr are the items that UDP sends, 
        # data being the message in bytes
        # addr being the IP and port 
        data, addr = serverSock.recvfrom(1024) #buffersize is 1024 bytes
        # REF : Client.py - stats check. 
        robotID = int(data.decode())

        # complies into the list if the ID received is not in list
        if ((addr not in addresses) & (robotID not in RobotList)):
            # Compiles addresses and Adds robotID (aka the robot is online)
            addresses.append(addr)
            RobotList.append(robotID)
            # Debug
            print(robotID,RobotList,addresses)
        # if the RobotID already exists
        elif(robotID in RobotList):
            #it will update the new address of the robot
            i = RobotList.index(robotID)
            addresses[i] = addr
            break # *remove after debugging
    # sends a ping message aka status request to double check with the ports    
    statusReq()


def getRobotVelocity():
    #getting information from SSL Vision and process them here
    #forms a message
    
    #Vx,Vy,w,runtime
    message = b'1,2,1,2'
    sendMessage(message)

def statusReq():
    # initialising i, which stands for the index of the list
    i = 0
    # In the following, we would like to loop existing robots within the list to check if they are alive
    # This is called the Ping process
    for i in range (len(RobotList)):
        # initialise timer 
        end_time = time.time() + 0.005
        # loop until the timer is up
        while time.time() < end_time:
            msg = b'status check'
            sendMessage(RobotList[i], msg)
            data, addr = serverSock.recvfrom(1024) #buffersize is 1024 bytes
            Robotid = int(data.decode())
            if(Robotid in RobotList):
                print(time.time()," Robot id :",str(Robotid),"is alive")
                data = ""
                break
            else : # The robot is not responding and it's lost connection 
                #printing Dead at the server
                print("dead")
                # The arraylist then removes the RobotID from the list and IP Address
                RobotList.remove(RobotList[i])
                addresses.remove(addresses[i])
                     
### Sending Messages ### 
# There are 2 different methods of sending messages.

# Which the first one is responsible to send message for 1 client

# Thus, it requires a robotID and the messages that is needed to be sent

def sendMessage(Robot_id, msg):
    # first, it checks if the RobotID is within our server list of robots in checkin
    if(Robot_id in RobotList):
        # then it locates the corresponding address of that Robot
        i = RobotList.index(Robot_id)
        # then we initiate the send message to the specific address
        serverSock.sendto(msg, (addresses[i]))

    # if the robotID doesn't exist in the server list of robot
    # it will report an error immediate and preventing the server to clash in an error
    else:
        print("Robot", Robot_id, "Does not exist")


## The second Method : Broadcasting : 

# In this method, it will be sending messages to all robots
# Thus, it doesn't require any RobotID and it will just do it by itself.

def Broadcast(msg):
    # initialise index number
    i = 0
    # loops all Robot's addresses and send them the message
    for i in range (len(RobotList)):
        print(i, len(RobotList))
        serverSock.sendto(msg, (addresses[i]))
        # time.sleep(10)

           
#running Checkin function
checkingIn()
