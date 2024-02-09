import numpy as np
from classes import PRMController, Obstacle, Utils

'''
    Modifications from original code:
    - Removed args parser
    - Removed the need for the environment.txt file
    - commented out code for plots and print statements
    TODO:
    - Integrate the path planner into existing code
    - Exchange example values for positions with real data
    - use new_target_point and pass it to the go_to_target function
    - the function also returns the distance - this is not used yet but might 
      be useful for deciding with robot should go to the ball
'''

# PARAMETERS
FIELD_WIDTH = 2760 #mm
FIELD_LENGTH = 5040 #mm

def main():
    numSamples = 20 #default: 47
    buffer = 250 #mm # dimension of the obstacles will be a square of the size 2*buffer x 2*buffer

    # CHANGE THAT SO IT IS READ FROM SSL VISION
    active_robot_position = [-1500,1120]    # position of the robot that is supposed to move
    target_position = [1000,-300]

    other_robots = [[-1499, 0],
                    [-549, 1100],
                    [-2499, -250],
                    [199, 800]]

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
    
    utils.drawMap(allObs, active_robot_position, target_position)

    # run path planner code
    prm = PRMController(numSamples, allObs, active_robot_position, target_position)

    # check whether the direct path from the current position to the target is obstructed
    if not (prm.checkLineCollision(active_robot_position, target_position)):
        new_target_point = target_position

        # # JUST TO COMPARE REMOVE LATER
        # prm.setBoundaries(x_min, y_min, x_max, y_max)
        # # Initial random seed to try
        # initialRandomSeed = 0
        # # pointsToEnd, dist = prm.runPRM(initialRandomSeed) # distance not used yet
        # pointsToEnd, _ = prm.runPRM(initialRandomSeed)

        # print("Use direct path")
    else:
        prm.setBoundaries(x_min, y_min, x_max, y_max)
        # Initial random seed to try
        initialRandomSeed = 0
        # pointsToEnd, dist = prm.runPRM(initialRandomSeed) # distance not used yet
        pointsToEnd, _ = prm.runPRM(initialRandomSeed)

        # pointsToEnd[0] = current position, pointsToEnd[1] = next target position as input for go_to_target function
        new_target_point = pointsToEnd[1]

    print(new_target_point)

if __name__ == '__main__':
    main()
