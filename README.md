# Low level skills
This is a set of low level skills and utility scripts that are not yet integrated in the code base.

## Goal Keeping
### ball_trajectory.py
This script estimates the trajectory of a moving ball using linear regression based on the last observed ball positions. Furthermore, it determines the direction the ball is moving (based on its x coordinate), the velocity the ball is moving at (based on the traveled distance between two consecutive frames) and the whether or not the ball is going into the goal following its estimated trajectory. If the ball is estimated to go into the goal the script furthermore returns the position at which the ball is going into the goal so the goalie can block it.

This is useful for multiple scenarios. First of all when an adversary player has the ball and kicks it towards our goal we can estimate where the ball is going to go into the goal and we can send this position to the goalie so the goalie can move to that position and block the ball from going into the goal.

Whenever a ball is moving either because it was passed to a robot or when an adversary player has kicked it we want to intersect its trajectory. For this it is not only important to know where the ball is at the current moment, but also where it is going to be at a later time point. Because then we can send a robot to the position to the expected position of the ball at the time it reaches the ball. 

Example of an estimated ball trajectory where the ball is going into the goal:

![Example of the ball trajectory estimation - going into the goal](./images/BallTrajectory_ex1.png)

Example of an estimated ball trajectory where the ball is not going into the goal:

![Example of the ball trajectory estimation - not going into the goal](./images/BallTrajectory_ex2.png)

Note: In the script are a number of parameters that might have to be changed such as the goal width etc.

Work to do:
- The goalie moves more than expected. Check the ball positions and estimated trajectories for the case where the ball is not moving. My assumption is that the ball positions are slightly different from frame to frame even though the ball does not move. This means that the regression model will estimate a trajectory and the goalie will go to that position. 
- Play around with the arguments for go_towards_target (velocity, slow_threshold and stop_threshold). This may help to make the goalie better. 
- When you start the code for the goalie agent and there is no ball on the field it crashed. That is probably because the history of ball position only contains None values. Add something to catch cases where there is no ball. The goalie should just stay in the center of the goal in those cases.

### goalie_agent.py
Goalie agent which defines a goalie that will stay in the center of the goal unless a ball is estimated to go into the goal. If the goal is estimated to go into the goal the goalie will go to that position to block it. The agent code includes the trajectory estimation as well as the command to move to the estimated position of the ball going into the ball. 

### agent_simulator.py
This code includes an example of how a goalie agent can be used.

## coord_trans.py
This script implement the transformation of the coordinate systems (local robot coordinate system vs. field coordinate system).

Check out the explanation of the coordinate system transformation in the [wiki](https://github.com/WSU-TurtleRabbit/WSU-TurtleRabbit.github.io/wiki/SSL-Vision#coordinate-system-transformation).


## turn_to_ball.py
In order to kick the ball or receive a pass the robots kicker must point into the direction of the ball. This script tries to implement this. Based on the current ball position in the robot coordinate system (e.g. (10mm, -300mm)) the script sets an agular velocity. The goal is that the robot should turn in such a way that its kicker is pointing in the direction of the ball. In order to avoid jitter because the robot would constantly try to fix its orientiation when it is not absolutely perfect I have added an epsilon. This defines the offset from the perfect orientation that is considered ok. This epsilon is parameter that can be adapted if necessary.

## aim_to_shoot.py
This function returns the target position for a robot that wants to aim and shoot the ball towards the goal or to another robot (passing the ball).

NEXT STEPS:
1. Move robot to target position (maybe see ball as an obstacle so robot does not run over the ball it wants to shoot when it is going to the target position)
2. Use turn_to_ball function
3. Move slightly (slowly) forward so the kicker is touching the ball
4. Kick

## Get ready to get a ball passed idea
- Agents that receive passes should always keep their kicker oriented towards the ball -> use turn_to_ball.py
- Agents that receive passes should aways check whether the line between them and the ball is collision free -> use CheckLineCollision from path planner
    - if path is obstructed the agents should move so the path is clear
- It does not make sense that all agents move over the entirety of the field. Agents should have their areas on the field. Check Olivers code for game strategy patterns. Keep that in mind for the position of the agents and where they move to get a clear path.
