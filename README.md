# code
Software, including firmware, control algorithms, etc.

## UDP Client Server
We will be using UDP to communicate between SSL-Vision, Computer and RsapberryPi.

The SSL-Vision will be sending Protobuff files to the Computer

The Computer will then convert that data and send to the RaspberryPi.

Finally, The RaspberryPi will be calculating it's own Velocities and move towards desired destination.