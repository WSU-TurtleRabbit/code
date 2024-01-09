# Basic Agent Simulator for Robocup SSL
This is a basic demonstration of an approach to controlling robots in grSim, the official simulator for Robocup SSL. 

## Running the Agent Simulator
To run, first compile the proto files with the command:

```bash
protoc --python_out=. *.proto

This will compile them in the current directory, which is needed for agent_simulator.py to run.

Additionally, you need to have the ssl-vision-cli executable in the same directory. You need to also set the "vision multicast port" on grSim to 10006. 
