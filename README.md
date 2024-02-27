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


### What the agents see

-The agents don't directly see what the client outputs. It is first filtered through the internal python dictionaries in trcontrol.py. These dictionaries are initialised in the main Simulation class in self.detection and self.geometry. 

This is what each agent receives via the "frame" argument:

```python
{'geometry': {}, 'detection': {'ball': {'x': 0, 'y': 0}, 'robots_yellow': {0: {'confidence': 1, 'robot_id': 0, 'x': 1497.5712, 'y': 1120, 'orientation': -3.1415927, 'pixel_x': 1497.5712, 'pixel_y': 1120}, 1: {'confidence': 1, 'robot_id': 1, 'x': 1497.5712, 'y': 5.717139e-12, 'orientation': 3.1415927, 'pixel_x': 1497.5712, 'pixel_y': 5.717139e-12}, 3: {'confidence': 1, 'robot_id': 3, 'x': 547.5712, 'y': -1.8211606e-11, 'orientation': -3.1415927, 'pixel_x': 547.5712, 'pixel_y': -1.8211606e-11}, 4: {'confidence': 1, 'robot_id': 4, 'x': 2497.5713, 'y': -2.955412e-12, 'orientation': 3.1415927, 'pixel_x': 2497.5713, 'pixel_y': -2.955412e-12}, 5: {'confidence': 1, 'robot_id': 5, 'x': 3597.5713, 'y': -1.6777793e-11, 'orientation': -3.1415927, 'pixel_x': 3597.5713, 'pixel_y': -1.6777793e-11}, 2: {'confidence': 1, 'robot_id': 2, 'x': 1497.5712, 'y': -1120, 'orientation': -3.1415927, 'pixel_x': 1497.5712, 'pixel_y': -1120}}, 'robots_blue': {1: {'confidence': 1, 'robot_id': 1, 'x': -1417.4371, 'y': 29.656864, 'orientation': 0.70621175, 'pixel_x': -1417.4371, 'pixel_y': 29.656864}, 2: {'confidence': 1, 'robot_id': 2, 'x': -1440.695, 'y': -1055.0938, 'orientation': 0.70779437, 'pixel_x': -1440.695, 'pixel_y': -1055.0938}, 3: {'confidence': 1, 'robot_id': 3, 'x': -467.43713, 'y': 29.656864, 'orientation': 0.70621175, 'pixel_x': -467.43713, 'pixel_y': 29.656864}, 4: {'confidence': 1, 'robot_id': 4, 'x': -2417.4373, 'y': 29.656864, 'orientation': 0.70621175, 'pixel_x': -2417.4373, 'pixel_y': 29.656864}, 5: {'confidence': 1, 'robot_id': 5, 'x': -3517.4373, 'y': 29.656864, 'orientation': 0.70621175, 'pixel_x': -3517.4373, 'pixel_y': 29.656864}, 0: {'confidence': 1, 'robot_id': 0, 'x': -1415.1483, 'y': 1105.9684, 'orientation': 0.69634324, 'pixel_x': -1415.1483, 'pixel_y': 1105.9684}}}}
```
That is sent to the agents via the main script, trcontrol.py. The agents receive this via this line:
```python
robot_id, vx, vy, vw = agent.act(self.get_data())
```

That is because the get_data() function is sending to the agents the "frame" data as shown above. So within an agent, if you want to access its own id, you access it with "self.id". 

Example of an agent accessing and using frame data:

```python
my_x = frame['detection']['robots_blue'][self.id]['x']
my_y = frame['detection']['robots_blue'][self.id]['y']
my_position = (my_x, my_y)
```

### How agents make decisions, and why we still need to use central control (the formations script)

This is the main engine of the script that sends data to agents, and receives their decisions. Some lines have been omitted for clarity, and the point here is to explain how it works.
The main script in this branch, trcontrol.py, will show all the actual details.

```python
for agent in self.agents:
# Retrieve desired velocities from each agent's act method
	robot_id, vx, vy, vw = agent.act(self.get_data())
```

The above loops through each agent sequentially, sends it the internally filtered frame data via the get_data() method, and each agent returns its desired velocities as well as its robot id.
This works because we sent a "list" of agent objects to the main simulation class, and here we loop through them. On each iteration of the loop, we know which ID we are working with because 
agents return data in this format:

```python
return self.id, self.vx, self.vy, self.vw
```

## Note, this wiki is in rapid progression. It will be further written, formatted and cleared up over the next few days. It is being written now with a sense of urgency just to convey the most important information as quickly as possible



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

In MotorControlScript.py, you must make sure the IP address here reflects the IP address you just found via the terminal command ifconfig:

```python
# Pass the motor_control object to the UDPServer, which sends along to all
    # functions: "servos" (the dictionary comprehension of controller instances), and the 
    # "transport" object, which holds the servo bus map. 
    udp_server = UDPServer("172.20.10.13", 5005, motor_control)
```

In the main script, trcontrol.py, the same IP address must be in this part of the code:

```python
class Simulation():
    def __init__(self, agents):
        self.agents = agents
        for agent in self.agents:
            agent.world2robot_fn = self.world2robot
        self.detection = {"ball": {"x": None, "y": None}, "robots_yellow": {}, "robots_blue": {}}
        self.geometry = {}
        self.history = list()

        self.grSimSender = grSimCommandSender("127.0.0.1", 20011) # For the simulator (change IP if not localhost)
        self.physicalRobotSender1 = PhysicalRobotCommandSender("172.20.10.13", 5005) # IP address for robot 1
```

In the above example, the matching IP address should be in the initialisation of the PhysicalRobotCommandSender class. 

Simply: Make sure the IP address is the same in both places in both scripts.

Then once, you are sure that the IP address is the same in both the trcontrol.py script(the main script) and MotorControlScript.py, you can continue with the next step.

In the terminal, ON THE RASPBERRY PI of the robot execute:
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
  - The above problem has been temporarily fixed by catching the exception of an index error. However, this only solves the issue if the active robot is near another obstacle as long
    as the obstacle is dynamically changing its position. 
  -The still remaining issue is that even when the ball is within the bounding box of an obstacle, the index error exception still commands the robot to execute velocities of zero.
   This means that if an obstacle robot is dribbling the ball, the path planning active robot simply does nothing. There needs to be a more specialised exception to catch both 
   bugs of the path planner. So we need a strategy for when the obstacle robot is dribbling the ball. This report is dervived from a test of sim_path_agent.py vs simple_agent.py.
   So now the path planning robot doesn't usually crash permanently, but is stuck in a confused state until the ball is free once again. There are still other errors from the path
   planner that need to be accounted for though. 
   

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
  
  

  
