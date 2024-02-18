from collections import defaultdict
import sys
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import numpy as np
from sklearn.neighbors import NearestNeighbors
import shapely.geometry

from .Dijkstra import Graph, dijkstra, to_array
from .Utils import Utils

PLOTTING = False


class PRMController:
    def __init__(self, numOfRandomCoordinates, allObs, current, destination,
                 ):
        self.numOfCoords = numOfRandomCoordinates
        self.coordsList = np.array([])
        self.allObs = allObs
        self.current = np.array(current)
        self.destination = np.array(destination)
        self.graph = Graph()
        self.utils = Utils()
        self.solutionFound = False
        self.min_x = 0
        self.max_x = 100
        self.min_y = 0
        self.max_y = 100
        
    def setBoundaries(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        
    def runPRM(self, initialRandomSeed, saveImage=False):
        seed = initialRandomSeed
        # Keep resampling if no solution found
        N = 0
#        while(not self.solutionFound):
        while (not self.solutionFound and N < 10):
            N += 1
            print("Trying with random seed {}".format(seed))
            np.random.seed(seed)

            # Generate n random samples called milestones
            self.genCoords()

            # Check if milestones are collision free
            self.checkIfCollisonFree()

            # Link each milestone to k nearest neighbours.
            # Retain collision free links as local paths.
            self.findNearestNeighbour()

            # Search for shortest path from start to end node - Using Dijksta's shortest path alg
            pointsToEnd, dist = self.shortestPath()

            seed = np.random.randint(1, 100000)
            self.coordsList = np.array([])
            self.graph = Graph()

        # if(saveImage):
        #     plt.savefig("{}_samples.png".format(self.numOfCoords))
        if PLOTTING:
            plt.plot([self.current[0][0], self.destination[0][0]], [self.current[0][1], self.destination[0][1]], c="red", linewidth=4.0)
            plt.show()

        return pointsToEnd, dist

    def genCoords(self):
        X = np.random.randint(self.x_min, self.x_max, 
                              size=(self.numOfCoords, 1))
        Y = np.random.randint(self.y_min, self.y_max, 
                              size=(self.numOfCoords, 1))
        self.coordsList = np.concatenate((X,Y), axis=1)
        # Adding begin and end points
        self.current = self.current.reshape(1, 2)
        self.destination = self.destination.reshape(1, 2)
        self.coordsList = np.concatenate(
            (self.coordsList, self.current, self.destination), axis=0)

    def checkIfCollisonFree(self):
        collision = False
        self.collisionFreePoints = np.array([])
        for point in self.coordsList:
            collision = self.checkPointCollision(point)
            if(not collision):
                if(self.collisionFreePoints.size == 0):
                    self.collisionFreePoints = point
                else:
                    self.collisionFreePoints = np.vstack(
                        [self.collisionFreePoints, point])
        if PLOTTING:
            self.plotPoints(self.collisionFreePoints)

    def findNearestNeighbour(self, k=5):
        X = self.collisionFreePoints
        knn = NearestNeighbors(n_neighbors=k)
        knn.fit(X)
        distances, indices = knn.kneighbors(X)
        self.collisionFreePaths = np.empty((1, 2), int)

        for i, p in enumerate(X):
            # Ignoring nearest neighbour - nearest neighbour is the point itself
            for j, neighbour in enumerate(X[indices[i][1:]]):
                start_line = p
                end_line = neighbour
                if(not self.checkPointCollision(start_line) and not self.checkPointCollision(end_line)):
                    if(not self.checkLineCollision(start_line, end_line)):
                        self.collisionFreePaths = np.concatenate(
                            (self.collisionFreePaths, p.reshape(1, 2), neighbour.reshape(1, 2)), axis=0)

                        a = str(self.findNodeIndex(p))
                        b = str(self.findNodeIndex(neighbour))
                        self.graph.add_node(a)
                        self.graph.add_edge(a, b, distances[i, j+1])

                        if PLOTTING:
                            x = [p[0], neighbour[0]]
                            y = [p[1], neighbour[1]]
                            plt.plot(x, y)

    def shortestPath(self):
        '''
            This function calculates the way point for the shortest path and returns 
            both those points and the distance to the end node in milimeters.
        '''
        self.startNode = str(self.findNodeIndex(self.current))
        self.endNode = str(self.findNodeIndex(self.destination))

        dist, prev = dijkstra(self.graph, self.startNode)

        pathToEnd = to_array(prev, self.endNode)

        if(len(pathToEnd) > 1):
            self.solutionFound = True
        else:
            return None, None

        if PLOTTING:
            # Plotting shorest path
            pointsToDisplay = [(self.findPointsFromNode(path))
                              for path in pathToEnd]
            
            x = [int(item[0]) for item in pointsToDisplay]
            y = [int(item[1]) for item in pointsToDisplay]
            plt.plot(x, y, c="blue", linewidth=3.5)

        pointsToEnd = [(self.findPointsFromNode(path))
                       for path in pathToEnd]

        # print("The quickest path from {} to {} is: \n {} \n with a distance of {}".format(
        #     self.collisionFreePoints[int(self.startNode)],
        #     self.collisionFreePoints[int(self.endNode)],
        #     " \n ".join(pointsToEnd),
        #     str(dist[self.endNode])
        # )
        # )

        return pointsToEnd, int(dist[self.endNode])

    def checkLineCollision(self, start_line, end_line):
        collision = False
        line = shapely.geometry.LineString([start_line, end_line])
        for obs in self.allObs:
            if(self.utils.isWall(obs)):
                uniqueCords = np.unique(obs.allCords, axis=0)
                wall = shapely.geometry.LineString(
                    uniqueCords)
                if(line.intersection(wall)):
                    collision = True
                    return collision
            else:
                obstacleShape = shapely.geometry.Polygon(
                    obs.allCords)
                if (line.intersects(obstacleShape)):
                    collision = True
                    return collision
        return collision

    def findNodeIndex(self, p):
        return np.where((self.collisionFreePoints == p).all(axis=1))[0][0]

    def findPointsFromNode(self, n):
        return self.collisionFreePoints[int(n)]

    def plotPoints(self, points):
        x = [item[0] for item in points]
        y = [item[1] for item in points]
        plt.scatter(x, y, c="black", s=1)

    def checkCollision(self, obs, point):
        p_x = point[0]
        p_y = point[1]
        if(obs.bottomLeft[0] <= p_x <= obs.bottomRight[0] and obs.bottomLeft[1] <= p_y <= obs.topLeft[1]):
            return True
        else:
            return False

    def checkPointCollision(self, point):
        for obs in self.allObs:
            collision = self.checkCollision(obs, point)
            if(collision):
                return True
        return False
    