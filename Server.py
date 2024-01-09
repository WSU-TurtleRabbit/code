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

def checkingIn (): 
        
    while len(addresses)<6:
        data, addr = serverSock.recvfrom(1024) #buffersize is 1024 bytes
        print(data)
        addresses.append(addr)
        print(addresses)
        statusReq()


def getRobotVelocity():
    #getting information from SSL Vision and process them here
    #forms a message
    
    #Vx,Vy,w,runtime
    message = b'1,2,1,2'
    sendMessage(message)

def statusReq():
    
    end_time = time.time() + 1

    while time.time() < end_time:
        msg = b'status check'
        sendMessage(msg)
        data, addr = serverSock.recvfrom(1024) #buffersize is 1024 bytes
        Robotid = int(data.decode())
        print(Robotid)

        if (Robotid <= 6):
            print(time.time()," Robot id :",str(Robotid),"is alive")
            data = ""
            break
        else: 
            print("dead")             


def sendMessage(msg):
    i = 0
    for i in range (len(addresses)):
        
        serverSock.sendto(msg, (addresses[i]))
             
        # except Exception as e:
        #     print(UDP_PORT_NO,"cannot connect")
        i+=1

checkingIn()
statusReq()