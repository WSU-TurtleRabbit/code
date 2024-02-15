from command_sender import CommandDispatcher
import numpy as np
from numpy import pi




#robotDispatcher = CommandDispatcher("172.20.10.14", 5005)
#robot_pose = [0, 0, 0]
#vw = 0
#vx = 1
#vy = 1
#robot_id = 0
#robotDispatcher.send_command(robot_id, vw, vx, vy, robot_pose)

dispatcher_physical = CommandDispatcher("172.20.10.14", 5005)
orientation = pi/4
orientation -= pi/2
robot_pose = np.array([0, 0, orientation])  # Example pose
dispatcher_physical.send_command(0, 0, -0.5, -0.5, robot_pose)
