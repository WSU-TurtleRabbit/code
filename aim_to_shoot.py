import numpy as np
import matplotlib.pyplot as plt

def calculate_robot_position(target, ball, robot_offset):
    '''
        This function returns the target position for a robot. It needs this
        to aim and shoot a ball.
    '''
    # Calculate direction vector from ball to target
    direction = np.array(target) - np.array(ball)
    
    # Normalize direction vector
    direction = direction.astype(float)  # Ensure direction vector is float
    direction /= np.linalg.norm(direction)
    
    # Calculate robot position slightly behind the ball
    robot_position = np.array(ball) - robot_offset * direction
    
    return robot_position

def plot_positions(target, ball, robot):
    plt.plot(target[0], target[1], 'bo', label='Target')
    plt.plot(ball[0], ball[1], 'ro', label='Ball')
    plt.plot(robot[0], robot[1], 'go', label='Robot')
    plt.plot([target[0], ball[0], robot[0]], [target[1], ball[1], robot[1]], '--', color='gray')
    plt.xlabel('X position (mm)')
    plt.ylabel('Y position (mm)')
    plt.title('Target, Ball, and Robot Positions')
    plt.xlim(-5040/2, 5040/2)
    plt.ylim(-2760/2, 2760/2)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)
    plt.legend()
    plt.show()

# GET THIS FROM SSL VISION
target_position = (-300, 100) # goal or other robot receiving a pass
ball_position = (10, -200)

# SET THIS PARAMETER -> THE ROBOT SHOULD BE SLIGHLY BEHIND THE BALL
# IT SHOULD HAVE ENOUGH PLACE TO TURN AROUND ITS OWN AXIS
robot_offset = 100 #mm

# Calculate robot position
robot_position = calculate_robot_position(target_position, ball_position, robot_offset)

# NEXT STEPS:
# 1. Move robot to robot position
# 2. Use turn_to_ball function
# 3. Move slightly (slowly) forward so the kicker is touching the ball
# 4. Kick

# Plot positions
plot_positions(target_position, ball_position, robot_position)

print("Robot position:", robot_position)
