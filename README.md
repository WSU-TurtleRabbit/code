# Code

This repo contains the software for our team. This includes the
overall team control, and also the code that translates actions into
motor commands, our motor control.

## [Networking]
### [ServerClass]

Server Class is a class that establish and maintain basic communications with the robots of the team. This includes : 
1. Broadcasting 
2. Receving
3. Sending 

## [PRM]
PRM is a path finder module created by 
It has been slightly modified to be able to integrate with the rest of our codes.

## [Shared]
### [Action]

Action is a predetermind packet that will automatically compile itself.
This packet will then be transfered onto the Robot Client.

### [utils]

Utils is a User Interface that allows you to humanily input the values desired using numbers. After the action has been compiled, you can use the Server.send_action(UI()) to send the action.

## [Team Control]

### [Skills]

#### [base Skill]

Base Skill is a class that initialise any skills that has different state.

Any skills that is created in the future should be having a start, run and finish state.

Via, Base Skill Class, we can then keep them running in a loop without any disruption.

There are several skills avaiable at this point of time : 
1. Go Towards #under development
2. Path Planner Import #under development

## [Skill Control](https://github.com/WSU-TurtleRabbit/code/tree/quali24/src/WSUSSL/skillcontroller)

Skill Control is a software that meant to process any skills that exist within our current module, and forwards to the Server's UDP, then onto the robot.

## [World]
In world, we have a World Model Class and Receiver Class
### [World Model]
World Model consists of all data retrieved from SSL-vision or grSim. see [World Model README] for more information.

### [Receiver]
World Receiver class contains all reciever connection that would be useful for both ssl-vision and grsim.

*Currently working on integrating the command sender to grsim*

## Installation

The module can be installed by using the provided [script](https://github.com/WSU-TurtleRabbit/code/blob/quali24/install.sh):
N.B. read the comments in ```install.sh``` if you encounter anything strange.
 
```bash
chmod 755 install.sh
./install.sh
```

To communicate with grSim, protobuf files need to be compiled into python. A script is provided [here](https://github.com/WSU-TurtleRabbit/code/src/Networking/proto2/setup.sh). It will automatically download the required protobuf files from [grSim](https://github.com/RoboCup-SSL/grSim.git) and compile using `protoc`. Installation of `protoc` will be attempted. However if it fails, `protoc` installation guide can be found [here](https://grpc.io/docs/protoc-installation/).

```bash
cd src/WSUSSL/Networking/proto2/
chmod 755 setup.sh
./setup.sh
```
