## Importing the socket Python Module
import socket
import time


## Defining the UDP ADDRESS AND PORT NO 
## This has to be the same as the robot.
UDP_IP_ADDRESS = "127.0.1.1" 
UDP_PORT_NO = 9000 

## send port, recieving port

## declare our serverSocket upon which we will be listening for UDP messages
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS,UDP_PORT_NO))

addresses = list()
RobotList = list()

def checkingIn (): 
    timeout = time.time() +10
    #while time.time() < timeout:
    while True:
        data, addr = serverSock.recvfrom(1024) #buffersize is 1024 bytes
        robotID = int(data.decode())
        if ((addr not in addresses) & (robotID not in RobotList)):
            addresses.append(addr)
            RobotList.append(robotID)
            print(robotID,RobotList,addresses)
        elif(robotID in RobotList):
            i = RobotList.index(robotID)
            addresses[i] = addr
            break
        
    statusReq()


def getRobotVelocity():
    #getting information from SSL Vision and process them here
    #forms a message
    
    #Vx,Vy,w,runtime
    message = b'1,2,1,2'
    sendMessage(message)

def statusReq():
    i = 0
    for i in range (len(RobotList)):
        end_time = time.time() + 0.005

        while time.time() < end_time:
            msg = b'status check'
            sendMessage(RobotList[i], msg)
            data, addr = serverSock.recvfrom(1024) #buffersize is 1024 bytes
            Robotid = int(data.decode())
            if(Robotid in RobotList):
                print(time.time()," Robot id :",str(Robotid),"is alive")
                data = ""
                break
            else : 
                print("dead")
                RobotList.remove(RobotList[i])
                addresses.remove(addresses[i])
                     
def sendMessage(Robot_id, msg):
    if(Robot_id in RobotList):
        i = RobotList.index(Robot_id)
        serverSock.sendto(msg, (addresses[i]))
    else:
        print("Robot", Robot_id, "Does not exist")


def Broadcast(msg):
    i = 0
    for i in range (len(RobotList)):
        print(i, len(RobotList))
        serverSock.sendto(msg, (addresses[i]))
        time.sleep(10)

           

checkingIn()
