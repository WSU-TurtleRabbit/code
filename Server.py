## Importing the socket Python Module
import socket


def getMessage():
    #getting information from SSL Vision and process them here
    #forms a message
    
    #Vx,Vy,w,timeout
    message = "1,2,1,0.5"
    return message

def main():


    ## Defining the UDP ADDRESS AND PORT NO 
    ## This has to be the same as the robot.
    UDP_IP_ADDRESS = "127.0.0.1" 
    UDP_PORT_NO = 6789 


    msg = getMessage()
    ## declare our serverSocket upon which we will be listening for UDP messages

    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    serverSock.sendto(msg, (UDP_IP_ADDRESS, UDP_PORT_NO))



