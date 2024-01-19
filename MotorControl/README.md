## Motor Control Script

This script converts a desired chassis velocity to individual wheel velocities in the context of the pi3hat and moteus hardware by mjbots. It takes as input, over UDP, the desired angular velocity (radians/sec), and the x,y velocities, and converts them to hertz. It then commands 4 motors to execute those velocities, thus achieving the overall desired velocity of the robot. The kinematic formula used in the script is derived from https://www.youtube.com/watch?v=NcOT9hOsceE&t=190s . If you skip to 3:12, a convenient form of it is displayed, which is what the script uses. 

# Running the Motor Control Script

First, connect both the raspberry pi and main computer to the same WiFi network, change the IP address in the script to the raspberry pi's IP. To check the IP, run the following command on the raspberry pi:

```bash
hostname -I
```

SSH the "MotorControlScript.py" file, which is the server side that sits on the raspberry pi, with the following command:

```bash
scp MotorControlScript.py [rpi_username_here]@[rpi_ip_address_here]:~
```
That will update the raspberry pi with MotorControlScript.py in its home directory. At this point, all you need to do is ssh again to the raspberry pi to run the script:

```bash
ssh [rpi_username]@[rpi_ip]
```
Then, once in the terminal of the rpi, run:

```bash
python3 MotorControlScript.py
```
At this point the UDP server on the script will be listening to the client. Run the client on the main computer, and this will allow for remote control.
