# Imports
import os
import time
import socket
#Importing Robot Class
from RobotClass import Robot

# initialisng the server IP and Port at the start of the script
#SERVERIP = os.popen('hostname -I').read().split(" ")[0]
SERVERIP = "127.0.0.1" #use this when debug on windows
SERVERPORT = 5000 # change this if needed
print("Server IP : ",SERVERIP,"Server Port : ",SERVERPORT)
## declare our serverSocket upon which we will be listening for UDP messages
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# binding the serverSocket with existing server IP and PORT 
serverSock.bind((SERVERIP, SERVERPORT))

def checkIN():
    # Initailise the Robot Objects
    for i in range (6): 
        thisBot = Robot.AddRobot()
        
        end_time = time.time() + 1
        while time.time() < end_time:
            print(time.time())        
            success = Robot.ping(thisBot, SERVERIP, SERVERPORT)

            data, addr = serverSock.recvfrom(1024) #buffersize is 1024 bytes
            if(success):
                print(data,addr, "has been received")
                Robot.bindIPP(thisBot,addr)
                break
            else:
                print(thisBot.id, "is Dead")
                

        ## if the total of Robot Object added = 6
        if (len(Robot.ROBOTLIST)==6):
            print("All Robots have been added thank you")
            Robot.Remove(thisBot)
            
            break
        print(Robot.ROBOTLIST)
        print(Robot.addresses)

checkIN()
def sendMessage():
    print("Please select a Robot to send message to:")
    rID = 7
    while rID > 6: 
        try:
            rID = int(input())
        except ValueError:
            print("please enter an int only within the range of 6")
            rID = 7
    #vx, vy, w, rt = 1,3,4,0.2
    msg = str("1,3,4,0.2").encode()
    print(msg)
    for n in range (5):
    # while time.time() < time.time() + 0.05:
        try:
            i = Robot.ROBOTLIST.index(rID)
            serverSock.sendto(msg,(Robot.addresses[i]))
            s = "Message delivered"
            break
        except AttributeError:
            s = "Cannot find Robot with address"
        except ValueError:
            s = "NO SUCH ROBOT"
        finally:
            print(s)
        print("Trying Again")
        

sendMessage()