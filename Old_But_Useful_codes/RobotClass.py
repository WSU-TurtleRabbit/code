import socket
import numpy as np
import ipaddress #use this if we want static manual ip addresses
import random



class Robot : 
    
    ROBOTLIST = list()
    addresses = list()
    #this is the Robot class 
    #Responsible to store and assign default values of the robots
    
    ## function on humanly assigning id
    def InputID():
        maxRobots = 6
        newID = 7
        try:
            while newID > maxRobots : 
                print("enter the Robot's id")
                print("the max Robot ID you can enter is : ",maxRobots)
                newID = int(input())

        except ValueError as e:
            newID = random.randint(1,6)
            print(e)
            print("error, but I have assigned id : ",newID)    
        finally:
            print(newID)
        
        return newID
        

    ## function on assigning ip address and port
    def AddRobot():
        id = Robot.InputID()
        if (id not in Robot.ROBOTLIST):
            Robot.ROBOTLIST.append(id)
            print("RobotADDED : ",Robot.ROBOTLIST)
        else:
            print("robot with ID : ", id, "already exists")
            print("Current Active Robots",Robot.ROBOTLIST)
            exit()
        NewRobot = Robot(id)
        return NewRobot

    
 

    

    # function on assigning value for robot     
    def __init__(self, id):
        self.id = id
        print(self.id,'hi')
        # self.r = 1 #wheel radius
        # self.b = np.array([1,1,1,1]) #wheel beta angle
        # self.d = np.array([1,1,1,1]) #wheel distance from centre
        self.clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



    

    def Remove(thisBot): 
        #locate index of this robot
        # since this is corresponding to it's address
        i = Robot.ROBOTLIST.index(thisBot.id)
        try: 
            #if it has addresses registered, removing its address
            if(thisBot.addr in Robot.addresses):
                Robot.addresses.remove(thisBot.addr)

        except AttributeError: 
            print("this Robot :",thisBot.id,"does not have an address saved")
        
        # removing from the list of robots
        Robot.ROBOTLIST.remove(thisBot.id)
        #removes itself (object) from the Robot class
        del thisBot
        print("Current Robot and addresses : ",Robot.ROBOTLIST, Robot.addresses)

    ### PING ###
    ## inital function on ping
    ## the address of Server will be inputed 
    def ping(self, serverIP, serverPort):
        pingSuccess = False
        str_robotID = str(self.id)
        b_robotID = str_robotID.encode()
        print(b_robotID)
        try:
            self.clientSock.sendto(b_robotID,(serverIP, serverPort))
            print(serverIP,serverPort)
        except ConnectionError :
            print("Cannot Connect to server")
        except Exception as e:
            print(e)
        finally:
            pingSuccess = True
            return pingSuccess

    # uses to bind the IP and PORT of the Robot (May not be needed)    
    def bindIPP(self, addr):
        print(addr)
        self.addr = addr
        #self.clientSock.bind((addr))
        Robot.addresses.append(addr)
        print(Robot.addresses)

        # could be replaced by something else
    
    # TO BE WORKED ON
    def CalWheelVel(self,vx,vy,w):
        '''
        "Modern Robotics: Mechanics, Planning & Control"
        13.2.1
        
        just leaving this here for no particular reason:
        libgen (dot) rs
        '''
        # retrieves the following value from object class
        r = self.r
        d = self.d
        b = self.b

        Vb = np.array([w, vx, vy])
        H = np.array([[-d[0], -d[1], -d[2], -d[3]],
                [np.cos(b[0]), np.cos(b[1]), -np.cos(b[2]), -np.cos(b[3])],
                [np.sin(b[0]), -np.sin(b[1]), -np.sin(b[2]), np.sin(b[3])],
                ])
        
        # [H (transposed) (dot) Vb]/r
        u = (H.T@Vb)/r
        # calculate the different wheel speed
        w1,w2,w3,w4 = u[0],u[1],u[2],u[3] #obtains the wheel value from the array
        return w1,w2,w3,w4





# for i in range (6):
#     Robot.AddRobot()
#     if (len(Robot.ROBOTLIST)==6):
#         print("All Robots have been added thank you")

