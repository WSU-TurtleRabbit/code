import sslclient
#import os
import threading
import time
import logging

from WorldModel import world_model as w

game_state = "ACTIVE"

def update_world_model():
    #serverip = os.popen('hostname -I').read().split(" ")[0]
    ip = "224.5.23.2" #ip connected to ssl-vision
    c = sslclient.client(ip, port=10006) # connect to ssl-vision

    # Bind connection to port and IP for UDP Multicast
    c.connect()

    while game_state != "STOP":
        #received decoded package
        data = c.receive()
        
        # if we wanted to get the data about the field (whitelines)
        # if data.HasField('geometry'):
        #     print("geometry : ",data.geometry)
        #     #w.update_geometry
        
        # if we want to know about the robots and ball data
        if data.HasField('detection'):
            #print("detection : ", data.detection) #debug
            # updates the world model with received information
            w.update_detection(data.detection)
            # example if you want to get the robot position
            #print(w.get_robot_position(0,True))
        
def action():
    while game_state != "STOP":
        try:
            command = input("what do u want to do: ")
            if command == "robot":
                print(w.get_robot_position(0,True))
            elif command == "exit": 
                game_state == "STOP"
        except Exception as e:
            print(e)

if __name__ == "__main__":
    u = threading.Thread(target= update_world_model)
    a = threading.Thread(target= action)

    u.start()
    a.start()

    a.join()
    u.join()
    print("END")