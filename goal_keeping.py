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
    - The goalie does not stand right at the edge of the field. The goals x coordinte maybe
      needs to be adjusted.
    - The function can be extended to calculate the ball velocity. By doing that we can not 
      only predict where the ball is going to be but also when.
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

GOAL_WIDTH = 1600 #mm
FIELD_WIDTH = 2760 #mm
FIELD_LENGTH = 5040 #mm
TEAM_YELLOW = True

def plot_trajectory_w_goal(trajectory, ball_positions_x, ball_positions_y, intersects_line, intersection_point, direction_info):
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
                            the goal, away from the goal or perpendicular to the goal.
    '''
    # Plot trajectory
    plt.plot([pos[0] for pos in trajectory], [pos[1] for pos in trajectory], label="Trajectory")

    # Plot ball positions
    plt.scatter(ball_positions_x, ball_positions_y, color='orange', label='Ball Positions')

    # Plot the vertical goal line x = -5040/2
    plt.axvline(x=-FIELD_LENGTH/2, color='r', linestyle='--', label="Goal Line")

    # Plot the goal area as a rectangle
    plt.fill_between([-FIELD_LENGTH/2, -FIELD_LENGTH/2 + 200], -GOAL_WIDTH/2, GOAL_WIDTH/2, color='r', alpha=0.1, label="Goal Area")

    # Check if trajectory intercepts the line and display result
    if intersects_line:
        plt.text(+100, -1000, f'Intersects Goal Line at\n{str(intersection_point)}\n{direction_info}', color='r', fontsize=10)  # Adjusted text position
        # Plot intersection point
        if intersection_point is not None:
            plt.scatter(*intersection_point, color='red', label='Intersection Point')
    else:
        plt.text(+100, -1000, 'Does Not Intersect Goal Line', color='g', fontsize=10)  # Adjusted text position

    # Add direction information
    plt.text(-4500, -1500, f'Direction: {direction_info}', color='white', fontsize=10)  # Adjusted text position

    # Plot settings
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Ball Trajectory and Goal Line Intersection')
    plt.legend()
    plt.grid(True)
    plt.xlim(-FIELD_LENGTH/2, FIELD_LENGTH/2)  # Adjusted x range
    plt.ylim(-FIELD_WIDTH/2, FIELD_WIDTH/2)  # Adjusted y range
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
    degree = 2
    poly_features = PolynomialFeatures(degree=degree)
    X_poly = poly_features.fit_transform(np.array(last_five_ball_positions_x).reshape(-1, 1))
    model = LinearRegression()
    model.fit(X_poly, last_five_ball_positions_y)
    
    # Generate trajectory points
    x_values = np.linspace(-FIELD_LENGTH/2, FIELD_LENGTH/2, 20) 
    X_values_poly = poly_features.transform(x_values.reshape(-1, 1))
    y_values = model.predict(X_values_poly)

    # Calculate the direction of the ball movement relative to the goal
    goal_x = -FIELD_LENGTH/2
    goal_y = 0  # Assuming goal is at the center
    ball_position_x = ball_positions_x[-1]  # Current ball position
    ball_position_y = ball_positions_y[-1]
    goal_vector = np.array([goal_x - ball_position_x, goal_y - ball_position_y])  # Vector pointing from ball to goal
    trajectory_vector = np.array([x_values[-1] - ball_position_x, y_values[-1] - ball_position_y])  # Vector pointing along the trajectory
    angle = np.arccos(np.dot(goal_vector, trajectory_vector) / (np.linalg.norm(goal_vector) * np.linalg.norm(trajectory_vector)))
    angle_degrees = np.degrees(angle)

    direction_info = None
    if angle_degrees < 45:
        direction_info = "Moving to the goal"
    elif angle_degrees > 135:
        direction_info = "Moving away from the goal"
    else:
        direction_info = "Moving perpendicular to the goal"

    # x-coordinate of the goal line
    if TEAM_YELLOW:
        goal_line_x = -FIELD_LENGTH/2
    else:
        goal_line_x = -FIELD_LENGTH/2
    
    # y-coordinate of the goal line
    goal_line_y_min = -GOAL_WIDTH / 2
    goal_line_y_max = GOAL_WIDTH / 2
    
    # Find the y-values of the trajectory at the goal line x-coordinate
    trajectory_y_at_goal_line = model.predict(poly_features.transform(np.array([goal_line_x]).reshape(-1, 1)))
    
    # Check if the y-value of the trajectory at the goal line x-coordinate is within the goal line y-range
    intersects_line = goal_line_y_min <= trajectory_y_at_goal_line <= goal_line_y_max
    
    # Calculate intersection point if exists
    intersection_point = None
    if intersects_line:
        intersection_point = (goal_line_x, round(trajectory_y_at_goal_line.item()))

    return list(zip(x_values, y_values)), intersects_line, intersection_point, direction_info

def check_goal_intersection():
    pass

def predict_trajectory_moving(ball_positions_x, ball_positions_y, current_frame_number, num_samples):
    # Predict ball trajectory when a robot is at the ball but has not kicked yet
    pass

def main():
    # Example usage:
    # This is a set of 6 x and y ball positions (on per frame) which in the real case have to be read from SSL vision.
    examples = [
        ("Example 1", np.linspace(0, -3000, 6), np.linspace(-200, -100, 6)),
        ("Example 2", np.linspace(0, -4000, 6), np.linspace(200, 400, 6)),
        ("Example 3", np.linspace(0, -500, 6), np.linspace(-2000, 2000, 6)),
        ("Example 4", np.linspace(0, -3000, 6), np.linspace(-1000, -1500, 6)),
        ("Example 5", np.linspace(-3000, 0, 6), np.linspace(-200, -100, 6)),
    ]

    # Iterate through examples
    for example_name, ball_positions_x, ball_positions_y in examples:
        print("Example:", example_name)

        current_frame_number = 5  # Current frame number
        num_samples = 3 # number of frames to use to estimate the trajectory

        trajectory, intersects_line, intersection_point, direction_info = predict_trajectory(ball_positions_x, ball_positions_y, current_frame_number, num_samples)

        plot_trajectory_w_goal(trajectory, ball_positions_x, ball_positions_y, intersects_line, intersection_point, direction_info)

        

if __name__ == '__main__':
    main()

