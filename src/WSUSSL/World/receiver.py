import sslclient
from WSUSSL.World.model import Model as wm

ssl_vision_ip = "224.5.23.2" #ip connected to ssl-vision
c = sslclient.client(ssl_vision_ip, port=10006) # connect to ssl-vision
c.connect()

while wm.state == "UPDATE":
    #received decoded pyackage
    data = c.receive()
    
    # if we wanted to get the data about the field (whitelines)
    if data.HasField('geometry'):
        #print("geometry : ",data.geometry)
        wm.update_geometry(data.geometry)
    
    # if we want to know about the robots and ball data
    if data.HasField('detection'):
        #print("detection : ", data.detection) #debug
        # updates the world model with received information
        wm.update_detection(data.detection)
        # example if you want to get the robot position
        #print(w.get_robot_position(0,True))
