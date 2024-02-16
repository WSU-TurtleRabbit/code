from agent import agent
from prm import PRMController, Obstacle, Utils
import numpy as np
from agent_behaviours import go_towards_target
from ast import literal_eval
import time
import random
from numpy import pi

# change to robot ids that are currently on the field
ACTIVE_ROBOT_IDS = [6, 1, 2, 3, 4]

class PathGeneralAgent(agent):
    def __init__(self, id, world2robot_fn=None):
        super().__init__(id)
        self.target_position = None  # This will be updated with the target position.
        self.waypoints = None
        self.world2robot_fn = world2robot_fn

    def set_target(self, target_position):
        self.target_position = target_position



    def act(self, frame):
        self.vx, self.vy, self.vw = 0, 0, 0
        if self.target_position is None or self.target_position[0] is None:
            return self.id, 0, 0, 0  
        print("Target position: ", self.target_position)

        # PARAMETERS
        FIELD_WIDTH = 2760 #mm
        FIELD_LENGTH = 5040 #mm
        my_x = frame['detection']['robots_blue'][self.id]['x']
        my_y = frame['detection']['robots_blue'][self.id]['y']
        active_robot_position = (my_x, my_y)
        print("Active position", active_robot_position)
        # Initialize an empty list
        other_robots = []

        # Loop through all the robots except for the current one (self.id)
        for robot_id, robot in frame['detection']['robots_blue'].items():
            if robot_id not in ACTIVE_ROBOT_IDS:
                # ignore invalid robot ids (ghost shells)
                continue
            if robot_id != self.id:
                # Append the robot's position as a small list to the other_robots list
                other_robots.append([robot['x'], robot['y']])

        numSamples = 7 #default: 47
        buffer = 250 #mm # dimension of the obstacles will be a square of the size 2*buffer x 2*buffer



        # Set obstacles
        allObs = []
        for obs in other_robots:
            topLeft = [obs[0]-buffer, obs[1]+buffer] # top left corner of the obstacle bounding box
            bottomRight = [obs[0]+buffer, obs[1]-buffer] # bottom right corner of the obstacle bounding box
            obs = Obstacle(topLeft, bottomRight)
            #obs.printFullCords()
            allObs.append(obs)

        # sets the field dimensions so it knows in which area to sample the milestones
        utils = Utils(x_min=-FIELD_LENGTH/2,y_min=-FIELD_WIDTH/2,x_max=FIELD_LENGTH/2,y_max=FIELD_WIDTH/2)
        x_min, y_min, x_max, y_max = utils.getBoundaries()
    
        #utils.drawMap(allObs, active_robot_position, self.target_position)

        # run path planner code
        prm = PRMController(numSamples, allObs, active_robot_position, self.target_position)

        # check whether the direct path from the current position to the target is obstructed
        if not (prm.checkLineCollision(active_robot_position, self.target_position)):
            new_target_point = self.target_position
            self.waypoints = None

            # # JUST TO COMPARE REMOVE LATER
            # prm.setBoundaries(x_min, y_min, x_max, y_max)
            # # Initial random seed to try
            # initialRandomSeed = 0
            # # pointsToEnd, dist = prm.runPRM(initialRandomSeed) # distance not used yet
            # pointsToEnd, _ = prm.runPRM(initialRandomSeed)

            # print("Use direct path")
        elif self.waypoints == None or prm.checkLineCollision(active_robot_position, self.waypoints[1]):
            prm.setBoundaries(x_min, y_min, x_max, y_max)
            # Initial random seed to try
            initialRandomSeed = 0 # random.randint(0, 10000)

            # pointsToEnd, dist = prm.runPRM(initialRandomSeed) # distance not used yet
            pointsToEnd, dist = prm.runPRM(initialRandomSeed, saveImage=False)
            if dist == None:
                pointsToEnd = [active_robot_position, self.target_position]
                print('no path found, go direct')
            self.waypoints = pointsToEnd.copy()

            # pointsToEnd[0] = current position, pointsToEnd[1] = next target position as input for go_to_target function
            new_target_point = pointsToEnd[1]
        else:
            new_target_point = self.waypoints[1]
            xdiff = new_target_point[0] - active_robot_position[0]
            ydiff = new_target_point[1] - active_robot_position[1]
            if (xdiff * xdiff) + (ydiff * ydiff) < 2500:
                del self.waypoints[1]

        print(new_target_point)
        print(type(new_target_point))

        print("new target: ", new_target_point)

        # Now we will send the new target point to the world2robot function
        # to convert the target point to one in the robot's local coordinate
        # system. 


        trans_target_position = np.array(new_target_point)

        
        if trans_target_position is not None:
            robot_data = frame["detection"]["robots_blue"][self.id]

            if robot_data and self.world2robot_fn:
                orientation = robot_data['orientation'] - pi/2
                robot_pose = np.array([robot_data['x'], robot_data['y'], orientation])
                # Convert target position to robot's coordinate system
                target_robot = self.world2robot_fn(trans_target_position, robot_pose)

                # Use a behavior function to calculate velocities towards the target
                agent_position = np.array([0, 0])
                self.vx, self.vy = go_towards_target(target_robot, agent_position)

                self.vw = 0  # Assuming no rotation for simplicity
                return self.id, self.vx, self.vy, self.vw
            else:
                return self.id, 0, 0, 0  
        else:
            return self.id, 0, 0, 0  



