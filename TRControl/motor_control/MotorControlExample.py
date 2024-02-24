# Author: Eren Yilmaz
# Developed for the RAM Robotics club at Western Sydney University
# This is a demonstration of using command_senders.py
# to send both velocity and kick commands to the robot.
# This setup allows agents in the agent simulator/trcontrol
# to send commands to the physical robot in an autonomous
# fashion.

from command_senders import PhysicalRobotCommandSender
import time

def test_kicker(ip, port, move_duration=5, kick_duration=2.5, delay=0.2):
    """
    Test the robot's kicker mechanism.

    Parameters:
    - ip: IP address of the robot.
    - port: Port number for UDP communication.
    - move_duration: Duration (in seconds) to send movement commands before kicking.
    - kick_duration: Duration (in seconds) to send kick commands.
    - delay: Delay (in seconds) between each command.
    """
    physical_sender = PhysicalRobotCommandSender(ip, port)

    # Send movement commands
    end_time = time.time() + move_duration
    while time.time() < end_time:
        physical_sender.send_command(Vw=0, Vx=0, Vy=1, K=0)  # Movement command
        time.sleep(delay)

    # Send kick commands
    end_time = time.time() + kick_duration
    while time.time() < end_time:
        physical_sender.send_command(Vw=0, Vx=0, Vy=1, K=1)  # Kick command
        time.sleep(delay)

# Example usage
if __name__ == "__main__":
    IP_ADDRESS = "172.20.10.13"  # Should match the robot's IP address and MotorControlScript.py
    PORT = 5005  # Should be the same as in MotorControlScript.py
    test_kicker(IP_ADDRESS, PORT)
