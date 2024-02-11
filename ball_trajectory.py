import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

'''
    Current limitations/things to work on:
    - We do not need all of the plotting for the actualy use case. This was just to check
      the results
    - Passing the x and y coordinates of the ball to the script is more complicated than
      in the example here. The positions and the frame number must be read in from SLL vision.
      The frame rates might not start at 0 so taking the 6th entry of the coordinate set might
      not be the correct frame.
    - We have to change the GOAL_WIDTH to the actual goal width
    - The goalie line is the line on which the goalie is supposed to move
    - The script calculates the ball velocity but it is not used yet.
    - We might need to change the team yellow etc. setting. It is just a variable to remember
      that we need to decide which goal is ours.

    Using that script:
    - When the ball intersects with the goal line and the ball is moving towards the ball give
      the goalie the coordinates of the intersection points so it can move to that position to
      block the ball
    - The estimated trajectory can be used for other things. For example when any robot moves
      to a moving ball it should go to the estimates position rather than the current position.
      Because when the robot reaches the position the ball has already moved on. 
'''

# PARAMETERS
GOAL_WIDTH = 1600 #mm
FIELD_WIDTH = 2760 #mm
FIELD_LENGTH = 5040 #mm
ROBOT_RADIUS = 90 #mm -> Check that value
BALL_RADIUS = 21.35 #mm
FRAME_RATE = 60 #Hz
TEAM_YELLOW = True
GOALIE_LINE = -FIELD_LENGTH/2 + 100 #mm #On the other lide of the field if we are the other team
GOALIE_LINE = -FIELD_LENGTH/2 + 100 if TEAM_YELLOW else FIELD_LENGTH/2 - 100

def plot_trajectory_w_goal(trajectory, ball_positions_x, ball_positions_y, intersects_line, intersection_point, direction_info, velocity):
    '''
        This function plots the trajectory, the goal field and whether there is an 
        intersection or not and the direction of the ball movement. All coodinates
        are in the field coordinate system and have the unit milimeters.

        input:
            trajectory: set of x and y values for the estimated trajectory
            ball_positions_x: x values of the observed ball positions
            ball_positions_y: y values of the observed ball positions
            intersects_line: bool value providing information whether the ball trajectory
                             passes through the goal line
            intersection_point: point (x,y) where the ball intersection with the goal line.
            direction_info: String with information whether the ball is moving towards 
                            our goal, away from our goal or perpendicular to our goal.
            velocity: velocity of the ball in mm/s
        output:
            None
    '''
    # Plot trajectory
    plt.plot([pos[0] for pos in trajectory], [pos[1] for pos in trajectory], label="Trajectory")

    # Plot ball positions
    plt.scatter(ball_positions_x[:-1], ball_positions_y[:-1], color='gray', label='Previous Ball Positions')
    plt.scatter(ball_positions_x[-1], ball_positions_y[-1], color='orange', label='Current Ball Position')

    # Plot the vertical goal line x = -5040/2
    plt.axvline(x=GOALIE_LINE, color='r', linestyle='--', label="Goalie Line")

    # Plot the goal area as a rectangle
    plt.fill_between([-FIELD_LENGTH/2, -FIELD_LENGTH/2 + 200], -GOAL_WIDTH/2, GOAL_WIDTH/2, color='r', alpha=0.1, label="Goal Area")

    # Check if trajectory intercepts the line and display result
    if intersects_line:
        plt.text(-100, -1200, f'Intersects Goalie Line at {str(intersection_point)}\n{direction_info}\nvelocity: {round(velocity)/1000}m/s', color='r', fontsize=10)  # Adjusted text position
        # Plot intersection point
        if intersection_point is not None:
            plt.scatter(*intersection_point, color='red', label='Intersection Point')
    else:
        plt.text(-100, -1200, f'Does Not Intersect Goalie Line\n{direction_info}\nvelocity: {round(velocity)/1000}m/s', color='g', fontsize=10)  # Adjusted text position

    # Plot settings
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Ball Trajectory and Goal Line Intersection')
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.xlim(-FIELD_LENGTH/2, FIELD_LENGTH/2) 
    plt.ylim(-FIELD_WIDTH/2, FIELD_WIDTH/2) 
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def predict_trajectory(ball_positions_x, ball_positions_y, current_frame_number, num_samples):
    '''
        This function takes are input a list of ball positions and uses the last 5 ball positions
        to fit a ball trajectory by applying a linear regression model. We then check whether this
        trajectory intercepts the goal line. If it does we send this information and the interception
        point to the goalie so the goalie can block the ball.

        input:
            ball_positions_x: x coordinates (in world coordinate system) of the detected ball
            ball_positions_y: y coordinates (in world coordinate system) of the detected ball
            current_frame_number: current frame number
            num_samples: number of samples that should be used to estimate the trajectory
        output:
            trajectory_y_at_goal_line: y value where the estimated trajectory intersects
                                       the goal line.
            direction_info: String with information whether the ball is moving towards 
                            our goal, away from our goal or perpendicular to our goal.
    '''
    # Ensure we have at least two points to fit a line
    if len(ball_positions_x) < 2:
        return None, None, None, None, None

    # Extract the last 5 frames' ball positions if available, otherwise use all positions
    if current_frame_number <= num_samples:
        last_five_ball_positions_x = ball_positions_x[:current_frame_number]
        last_five_ball_positions_y = ball_positions_y[:current_frame_number]
    else:
        last_five_ball_positions_x = ball_positions_x[current_frame_number - num_samples:current_frame_number]
        last_five_ball_positions_y = ball_positions_y[current_frame_number - num_samples:current_frame_number]

    # Fit polynomial regression to the last frames' ball positions
    model = LinearRegression()
    model.fit(np.array(last_five_ball_positions_x).reshape(-1, 1), last_five_ball_positions_y)


    # Generate trajectory points
    x_values = np.linspace(-FIELD_LENGTH/2, FIELD_LENGTH/2, 20) 
    y_values = model.predict(x_values.reshape(-1, 1))

    current_ball_position_x = ball_positions_x[-1]  # Current ball position

    if TEAM_YELLOW:
        if current_ball_position_x > last_five_ball_positions_x[-1]:  # If current x-coordinate is greater than the previous one
            direction_info = "Moving away from the goal"
        elif current_ball_position_x < last_five_ball_positions_x[-1]:  # If current x-coordinate is smaller than the previous one
            direction_info = "Moving towards the goal"
        else:
            direction_info = "Moving perpendicular to the goal/ not moving"
    else:
        if current_ball_position_x < last_five_ball_positions_x[-1]:  # If current x-coordinate is greater than the previous one
            direction_info = "Moving away from the goal"
        elif current_ball_position_x > last_five_ball_positions_x[-1]:  # If current x-coordinate is smaller than the previous one
            direction_info = "Moving towards the goal"
        else:
            direction_info = "Moving perpendicular to the goal/ not moving"
    
    # Find the y-values of the trajectory at the goal line x-coordinate
    trajectory_y_at_goal_line = model.predict(np.array([GOALIE_LINE]).reshape(-1, 1))


    # Calculate velocity
    num_positions = len(ball_positions_x)
    if num_positions >= 2:
        # Calculate the change in position between the last two positions
        delta_x = ball_positions_x[-1] - ball_positions_x[-2]
        delta_y = ball_positions_y[-1] - ball_positions_y[-2]

        # Calculate time elapsed between the last two frames
        time_elapsed = 1 / FRAME_RATE  # In seconds

        # Calculate velocity components
        velocity_x = delta_x / time_elapsed
        velocity_y = delta_y / time_elapsed

        # Calculate magnitude of velocity
        velocity = np.sqrt(velocity_x ** 2 + velocity_y ** 2)
    else:
        velocity = None

    return list(zip(x_values, y_values)), direction_info, trajectory_y_at_goal_line, velocity


def goal_intersection(trajectory_y_at_goal_line):
    '''
        This function checks whether the estimates ball trajectory goal through the goal 
        and whether the ball is moving towards the goal at all.

        input:
            trajectory_y_at_goal_line: y value where the estimated trajectory intersects
                                       the goal line.
        output:
            intersects_line: bool value providing information whether the ball trajectory
                             passes through the goal line
            intersection_point: point (x,y) where the ball intersection with the goal line.
    '''
    # Check if the y-value of the trajectory at the goal line x-coordinate is within the goal line y-range
    intersects_line = -GOAL_WIDTH / 2 <= trajectory_y_at_goal_line <= GOAL_WIDTH / 2
    
    # Calculate intersection point if exists
    intersection_point = None
    if intersects_line:
        intersection_point = (GOALIE_LINE, round(trajectory_y_at_goal_line.item()))

    return intersects_line, intersection_point


def main():
    # Example usage:
    # This is a set of x and y ball positions (on per frame) which in the real case have to be read from SSL vision.
    examples = [
        ("Example 1", np.linspace(2000, -300, 6), np.linspace(-200, -100, 6)),
        ("Example 2", np.linspace(2300, -400, 6), np.linspace(200, 400, 6)),
        ("Example 3", np.linspace(1000, -500, 6), np.linspace(-1200, 1200, 6)),
        ("Example 4", np.linspace(100, -100, 6), np.linspace(-1000, -1300, 6)),
        ("Example 5", np.linspace(-300, 0, 6), np.linspace(-200, -100, 6)),
    ]

    # Iterate through examples
    for example_name, ball_positions_x, ball_positions_y in examples:
        print("Example:", example_name)

        current_frame_number = 5  # Current frame number
        num_samples = 3 # number of frames to use to estimate the trajectory

        # estimate the trajectory of the moving ball
        trajectory, direction_info, trajectory_y_at_goal_line, velocity = predict_trajectory(ball_positions_x, ball_positions_y, current_frame_number, num_samples)
        # check whether the estimated ball trajectory intersects with the goal line
        intersects_line, intersection_point = goal_intersection(trajectory_y_at_goal_line)

        plot_trajectory_w_goal(trajectory, ball_positions_x, ball_positions_y, intersects_line, intersection_point, direction_info, velocity)

    # Next step: make the goalie acts based on the fact whether the estimated ball trajectory intersects the ball line

if __name__ == '__main__':
    main()

