# Excerpt from original README
Testing the prm path planner from https://github.com/KaleabTessera/PRM-Path-Planning

## Steps of algorithm
1. Generate n random samples called milestones.
2. Check if milestones are collision free.
3. Find k valid neighbours/paths:
   - Link each milestone to k nearest neighbours.
   - Retain collision free links as local paths.
4. Search for shortest path from start to end node using an algoruthm. In this case we are using Dijksta's shortest path algorithm.

## PRM vs RRT (Randomly Expanding Trees)
PRM was choosen since it is probabilistically complete and in a small map like the one given in this problem, sampling is time efficient.

## Problem
"You are given as input the current and target coordinates of a robot, as well as the top left and bottom right points of rectangular obstacles."

# Modifications
Both the PRMController.py code was modified and the old main.py script was replaced with an adapted main_adapted.py script. 
- Changed the code so there is no need for the environment.txt file but the positions can be used directly from SSL vision
- Commented out code for plots and prints
- The shortestPath function now returns the way points and the distance
- The next way point will be used as the new target for the moving robot
- Slightly improved the CheckLinieCollision function
- Check whether the direct path is obstructed if now use the target position as the next target for the robot to go to


