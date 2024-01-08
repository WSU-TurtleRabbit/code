Motor Control Script

This script converts a desired chassis velocity to individual wheel velocities in the context of the pi3hat and moteus hardware by mjbots. It takes as input, over UDP, the desired angular velocity (radians/sec), and the x,y velocities, and converts them to hertz. It then commands 4 motors to execute those velocities, thus achieving the overall desired velocity of the robot. The kinematic formula used in the script is derived from https://www.youtube.com/watch?v=NcOT9hOsceE&t=190s . If you skip to 3:12, a convenient form of it is displayed, which is what the script uses. 

The 
