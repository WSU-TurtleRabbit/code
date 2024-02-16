# README
## Motor Control

## Agents
Explain what agents are

List of agents and what they do:
- **goalie_agent**: Goalie will stay in the center of the field unless the ball is estimated to go into the goal (based on linear regression using the last observed ball positions) then it is will go to the estimated position of where the ball goes into the goal and block it.
- **general_agent**: GeneralAgent will chase the ball on the field, while adhering to field boundaries. It is mainly a demonstration of an agent template for the physical field. It uses the world2robot function to dynamically chase any arbitrary point (such as a robot moving robot shell).
- **path_general_agent**: PathGeneralAgent is a path planner agent. It uses the PRMController class to dynamically path-plan on the field. It will chase an arbitrary point that can be dynamic while avoiding dynamic obstacles.
- **sim_path_agent**: Class name being SimulationAgent, this agent will path-plan using the same PRMController to path-plan, but only in the simulator (grSim).
- **simple_agent**: SimpleAgent is a basic template for an agent that can chase any dynamic coordinate in the simulator. It will not avoid obstacles, but can adhere to field boundaries if setup accordingly. 
- ...

## Running the code on the robot
Steps what needs to be done to use the robot

## ...

## Current issues
- General issues:
  - When the robot is too close to the edge of the field its position does not get updated and it keeps going outside the field because it remembers its last position and thus thinks it is still in the field.
- Goalie:
  - Goalie agent does not work at the moment when you start it when there is no ball on the field.
  - Goalie seems to estimate trajectories even when the ball is not moving possibly because the ball position is still not exactly the same in each frame even when the ball is not moving. This may be why the goalie keeps moving all the time.
- Path Planner:
  - When the target position (milestone) is too close to an obstacle the check collision function deletes the target position from the list of waypoints. Hence it crashes. 

## Open tasks
- Finetune speed, slow_threshold and stop_threshold of all agents
- Implement kicker
- Implement aiming and shooting a ball
- Implement braking
- ...
