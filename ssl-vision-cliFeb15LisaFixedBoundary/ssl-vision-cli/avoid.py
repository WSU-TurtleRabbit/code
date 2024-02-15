from agent import agent
import random

class Avoid(agent):
    pass
    #def act(self, frame):
        #coords = list(frame.values())
        #kd = KDTree(coords)
        #for id in frame.keys():
            #mycoords = frame[id]
            #result = kd.query([mycoords], 2)
            #distances, indices = result
            #selfindex = indices[0][0]
            #neighbor_index = indices[0][1]
            #selfcoords = coords[selfindex]
            #neighbor_coords = coords[neighbor_index]
            #print(mycoords, selfcoords, neighbor_coords)
