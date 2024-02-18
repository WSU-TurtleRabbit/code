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

## How to get started

* The initial setup is for grSim, so you will need to install that on your machine:
  https://github.com/RoboCup-SSL/grSim

  You need to also set the "vision multicast port" on grSim to 10006.

* Clone this repository / branch on your machine:
  we are using the ssl-vision-client as a submodule, so you should use the "--recursive" option when cloning:

With SSH:
```
  git clone --branch quali-video-code-restructured --recursive git@github.com:WSU-TurtleRabbit/code.git
```
Clone with a token instead:
```
git clone --branch quali-video-code-restructured --recursive https://github.com/WSU-TurtleRabbit/code.git
```

  If you already cloned the repo, but not recursively, or for a different branch, then you can fix that with these steps:

```
cd code
git checkout quali-video-code-restructured
git submodule update --init --recursive
```

* Create the `ssl-vision-cli` binary

  This requires node (nodejs and/or npm) and programming language Go to be installed on your machine. Google is your friend.

  If you have that, build the `ssl-vision-cli` binary like this:

```
  cd code/quali-video-code-restructured/ssl-vision-client/cmd/ssl-vision-cli
  go build
```

  This should give you an executable, `ssl-vision-cli` in that directory.

  The executable is also directly available from the ssl-vision-client
  directory and in that case does not need to be build. It will not
  work on every linux version, the above step should work as long as
  you have the required software installed, independent of the linux
  version. If you just download the binary, copy it into your repository, into
  the `code/TRControl/ssl-vision-client/cmd/ssl-vision-cli/` directory.

* Start the simulator, change the vision multicast port to 10006.
  The main TurtleRabbitController is in the subdirectory TRControl, cd into that.
  Start it with `python3 ./trcontrol.py`.

  This should run a demo client.
  
  

  
