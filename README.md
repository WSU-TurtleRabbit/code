# Code

This repo contains the software for our team. This includes the
overall team control, and also the code that translates actions into
motor commands, our motor control.

## [TeamControl](https://github.com/WSU-TurtleRabbit/code/tree/quali24/src/WSUSSL/TeamControl)

TeamControl is a centralised software intended to run on a machine
next to the field, and communicate with all other SSL systems and our
robots.


## [MotorControl](https://github.com/WSU-TurtleRabbit/code/tree/quali24/MotorControl)

This module is intended to be run on a raspi, on each robot, to
receive and translate actions into motor commands.

## Installation

The module can be installed by using the provided [script](https://github.com/WSU-TurtleRabbit/code/blob/quali24/install.sh):
N.B. read the comments in ```install.sh``` if you encounter anything strange.
 
```bash
chmod 755 install.sh
./install.sh
```

