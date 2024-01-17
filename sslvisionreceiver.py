import sslclient
import os
from WorldModel import world_model as w

serverip = os.popen('hostname -I').read().split(" ")[0]
ip = "224.5.23.2"
c = sslclient.client(ip, port=10006)

# Bind connection to port and IP for UDP Multicast
c.connect()

while True:
    #received decoded package
    data = c.receive()
    
    #if data.HasField('geometry'):
        #print("geometry : ",data.geometry)
        #w.update_geometry
    
    if data.HasField('detection'):
        print("detection : ", data.detection)
        w.update_detection(data.detection)
        print(w.get_robot_position(0,True))
    