import numpy as np
from numpy import pi


def turn_to_ball(ball_position, epsilon=0.15):
    '''
        This function returns an agular velocity. The goal is to turn the robot
        in such a way that it is facing the ball with its kicker side.

        input: 
            ball_position: ball position in the robot coordinate systen (e.g. (10mm,50mm))
            epsilon: Threshold for the orientation (orientation does not have to be zero to 
                     consider it correct -> avoids jitter)
    '''
    if ball_position:
        orientation_to_ball = np.arctan2(ball_position[0], ball_position[1])

        if abs(orientation_to_ball) < epsilon:
            # to avoid jitter
            omega = 0
            print("Robot already has correct orientation", omega, orientation_to_ball)
        elif abs(orientation_to_ball) > epsilon and abs(orientation_to_ball) < 4*epsilon:
            omega = -1*np.sign(orientation_to_ball) * 0.5
            print("Robot almost has correct orientation", omega, orientation_to_ball)
        else:
            omega = -1*np.sign(orientation_to_ball)
            print("Robot not in correct orientation", omega, orientation_to_ball)

        return omega

def main():
    ball_position = (-30, 0) # in robot coord. system
    print("\nBall position:", ball_position)
    turn_to_ball(ball_position)

    ball_position = (0, 30) # in robot coord. system
    print("\nBall position:", ball_position)
    turn_to_ball(ball_position)

    ball_position = (0, -30) # in robot coord. system
    print("\nBall position:", ball_position)
    turn_to_ball(ball_position)

    ball_position = (30, 30) # in robot coord. system
    print("\nBall position:", ball_position)
    turn_to_ball(ball_position)

    ball_position = (30, 0) # in robot coord. system
    print("\nBall position:", ball_position)
    turn_to_ball(ball_position)

    ball_position = (5, 40) # in robot coord. system
    print("\nBall position:", ball_position)
    turn_to_ball(ball_position)

    ball_position = (-30, -10) # in robot coord. system
    print("\nBall position:", ball_position)
    turn_to_ball(ball_position)

    ball_position = (-30, -30) # in robot coord. system
    print("\nBall position:", ball_position)
    turn_to_ball(ball_position)


if __name__ == "__main__":
    main()