# code

This branch is an attempt to start an initial team behaviour code, with some basic file organisation.

It builds off Eren's code (elsewhere in this repo) for the basic agents, but the idea is to provide a bit more structure and organisation useful for controlling a whole team.

Eventually this should evolve into the more complete team code, with world model etc.

## How to get started

* The initial setup is for grSim, so you will need to install that on your machine:
  https://github.com/RoboCup-SSL/grSim

* Clone this repository / branch on your machine:
  we are using the ssl-vision-client as a submodule, so you should use the "--recursive" option when cloning:

```
  git clone --branch base-team-control --recursive git@github.com:WSU-TurtleRabbit/code.git
```

* Create the `ssl-vision-cli` binary
