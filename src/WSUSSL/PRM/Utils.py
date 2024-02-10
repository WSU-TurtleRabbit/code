import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle


class Utils:
    def __init__(self, x_min = 0, y_min = 0, x_max = 100, y_max = 100):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
    
    def setBoundaries(self, obs, curr, dest, x_margin = 0, y_margin = 0):
        x_min = min(curr[0], dest[0])
        x_max = max(curr[0], dest[0])
        y_min = min(curr[1], dest[1])            
        y_max = max(curr[1], dest[1])            

        for ob in obs:
            x_min = min(x_min, ob.bottomLeft[0])
            x_max = max(x_max, ob.topRight[0])
            y_min = min(y_min, ob.bottomLeft[1])
            y_max = max(y_max, ob.topRight[1])
        
        self.x_min = x_min - x_margin
        self.x_max = x_max + x_margin
        self.y_min = y_min - y_margin
        self.y_max = y_max + y_margin
        
    def getBoundaries(self):
        return self.x_min, self.y_min, self.x_max, self.y_max
    
    def isWall(self, obs):
        x = [item[0] for item in obs.allCords]
        y = [item[1] for item in obs.allCords]
        if(len(np.unique(x)) < 2 or len(np.unique(y)) < 2):
            return True  # Wall
        else:
            return False  # Rectangle

    def drawMap(self, obs, curr, dest):
        fig = plt.figure()
        currentAxis = plt.gca()
                
        # Set predefined limits for the map
        plt.xlim(self.x_min, self.x_max)
        plt.ylim(self.y_min, self.y_max)        
        
        for ob in obs:
            if(self.isWall(ob)):
                x = [item[0] for item in ob.allCords]
                y = [item[1] for item in ob.allCords]
                plt.scatter(x, y, c="red")
                plt.plot(x, y)
            else:
                currentAxis.add_patch(Rectangle(
                    (ob.bottomLeft[0], ob.bottomLeft[1]), ob.width, ob.height, alpha=0.4))

        plt.scatter(curr[0], curr[1], s=200, c='green')
        plt.scatter(dest[0], dest[1], s=200, c='green')
        fig.canvas.draw()
