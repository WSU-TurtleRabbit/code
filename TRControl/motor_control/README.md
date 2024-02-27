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
For the robot to be ready to receive commands from the trcontrol.py on the main computer, you need to run MotorControlScript.py on the robot, and wait until you see that it confirms that it is
"listening to UDP packets".

The IP address in the UDPServer class in MotorControlScript.py must match the IP and port that is initialised in the Simulation class on trcontrol.py(the main script). As long as the port and IP numbers
match both in trcontrol.py and MotorControlScript.py, it will be able to receive commands.

### More detailed instructions for running the code on the robot
You can do this manually or remotely via SSH.

Manual Method:
For the manual method, plug in the robot's raspberry pi to a monitor via HDMI, plug in a USB mouse and USB keyboard. For this situation, it is fine to use the battery for power, so remember to switch
the robot on via the switch.

You must first check the IP address of the robot. In the terminal, execute:
```
ifconfig
```
This should bring up something like:
```
    wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
            inet 172.20.10.13  netmask 255.255.255.0  broadcast 192.168.1.255
```

The IP address is the one next to "inet". An alternative command would be:
```
hostname -I
```

Then once, you are sure that the IP address is the same in both the trcontrol.py script(the main script) and MotorControlScript.py, you can continue with the next step.

In the terminal, execute:
```
python3 MotorControlScript.py
```

That should work as it is in the main directory usually. At this point, if the robot prints "listening to UDP commands" on the console, you can unplug everything and keep it switched on.
At this point it will be controlled by the main script trcontrol.py. The main script uses module "command_senders.py" to send commands. There is an example script of how an architecture can 
use command_senders.py to send commands to the physical robot with MotorControlScript.py running on the robot, inside the motor control folder. 

This wiki is a work in progress. If there are issues following in instructions, let me know those specific issues so that I can include clearer instructions for them

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
  git clone --branch base-team-control --recursive git@github.com:WSU-TurtleRabbit/code.git
```
Clone with a token instead:
```
git clone --branch base-team-control --recursive https://github.com/WSU-TurtleRabbit/code.git
```

  If you already cloned the repo, but not recursively, or for a different branch, then you can fix that with these steps:

```
cd code
git checkout base-team-control-restructured
git submodule update --init --recursive
```

* Create the `ssl-vision-cli` binary

  This requires node (nodejs and/or npm) and programming language Go to be installed on your machine. Google is your friend.

  If you have that, build the `ssl-vision-cli` binary like this:

```
  cd code/base-team-control/ssl-vision-client/cmd/ssl-vision-cli
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
  
  

  