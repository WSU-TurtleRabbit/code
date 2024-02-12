# WSU TurtleRabbit : Code

This repo contains the software for our team. This includes the
overall team control, and also the code that translates actions into
motor commands, our motor control.

## Networking: [Folder](https://github.com/WSU-TurtleRabbit/code/tree/quali24/src/WSUSSL/Networking)
### [ServerClass](https://github.com/WSU-TurtleRabbit/code/blob/quali24/src/WSUSSL/Networking/ServerClass.py)

Server Class is a class that establish and maintain basic communications with the robots of the team. This includes : 
1. Broadcasting 
2. Receving
3. Sending 

## PRM: [Folder](https://github.com/WSU-TurtleRabbit/code/tree/quali24/src/WSUSSL/PRM)
PRM is a path finder module created by 
It has been slightly modified to be able to integrate with the rest of our codes.

## Shared: [Folder](https://github.com/WSU-TurtleRabbit/code/tree/quali24/src/WSUSSL/Shared)

Contains action and utils python files. This is shared between Robot Client and Server.

### [Action](https://github.com/WSU-TurtleRabbit/code/blob/quali24/src/WSUSSL/Shared/action.py)

Action is a predetermind packet that will automatically compile itself.
This packet will then be transfered onto the Robot Client.

### [utils](https://github.com/WSU-TurtleRabbit/code/blob/quali24/src/WSUSSL/Shared/utils.py)

Utils is a User Interface that allows you to humanily input the values desired using numbers. 
After the action has been compiled, you can use the Server.send_action(UI()) to send the action.

## [Team Control](https://github.com/WSU-TurtleRabbit/code/tree/quali24/src/WSUSSL/TeamControl)

This is where we organise robot behaviours and assigning skills.

### [Skills](https://github.com/WSU-TurtleRabbit/code/tree/quali24/src/WSUSSL/TeamControl/Skills)

This is where we put our skills in, also where we retrieves it.
A Template can be found : [sample skills](https://github.com/WSU-TurtleRabbit/code/blob/quali24/src/WSUSSL/TeamControl/Skills/sampleskill.py)

#### [base Skill](https://github.com/WSU-TurtleRabbit/code/blob/quali24/src/WSUSSL/TeamControl/Skills/baseskill.py)

Base Skill is a class that initialise any skills that has different state.

Any skills that is created in the future should be having a start, run and finish state.

Via, Base Skill Class, we can then keep them running in a loop without any disruption.

There are several skills avaiable at this point of time : 
1. Go Towards #under development
2. Path Planner Import #under development

### [Skill Control](https://github.com/WSU-TurtleRabbit/code/tree/quali24/src/WSUSSL/skillcontroller)

Skill Control is a software that meant to process any skills that exist within our current module, 
and forwards to the Server's UDP, then onto the robot.

## World : [Folder](https://github.com/WSU-TurtleRabbit/code/blob/quali24/src/WSUSSL/World)

In world, we have a World Model Class and Receiver Class

### [World Model](https://github.com/WSU-TurtleRabbit/code/blob/quali24/src/WSUSSL/World/model.py)

World Model consists of all data retrieved from SSL-vision or grSim. 
see [PROTO README](https://github.com/WSU-TurtleRabbit/code/blob/quali24/src/WSUSSL/World/proto2/README.md) for more information.

### [Receiver](https://github.com/WSU-TurtleRabbit/code/blob/quali24/src/WSUSSL/World/receiver.py)
World Receiver class contains all reciever connection that would be useful for both ssl-vision and grsim.

*Currently working on integrating the command sender to grsim*

## Installation

The module can be installed by using the provided [script](https://github.com/WSU-TurtleRabbit/code/blob/quali24/install.sh):
N.B. read the comments in ```install.sh``` if you encounter anything strange.
 
```bash
chmod 755 install.sh
./install.sh
```

To communicate with grSim, protobuf files need to be compiled into python. Protobuf files can be found in [grSim](https://github.com/RoboCup-SSL/grSim.git) and compile using `protoc`. A `protoc` installation guide can be found [here](https://grpc.io/docs/protoc-installation/).
